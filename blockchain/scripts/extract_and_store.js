const fs = require('fs');
const { ethers } = require('hardhat');
const redis = require('redis');
const path = require('path');

const redisHost = process.env.REDIS_HOST || 'localhost';
const redisPort = parseInt(process.env.REDIS_PORT, 10) || 6379;

// REDIS CLIENT
let redisClient = redis.createClient({
  socket: {
    host: redisHost,
    port: redisPort,
  }
});

// ENSURE REDIS CONNECTION
const ensureRedisConnection = async () => {
  if (!redisClient.isOpen) {
      console.log('Reconnecting to Redis...');
      try {
        await redisClient.connect();
      } catch (err) {
          console.error('Error connecting to Redis:', err);
      }
  }
};

// PROCESSING OF DATA AND SAVING IN THE BLOCKCHAIN
const processBinaryData = async (key, buffer, contract) => {
  console.log('Processing binary data for key:', key);
  
  try {

    const dataBytes = Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer);

    const tx = await contract.storeData(key, dataBytes); //CALL storeData TO SAVED THE DATA (CONTRACT)
    const receipt = await tx.wait();

    if (receipt.status !== 1) {
      throw new Error(`Transaction failed for key ${key}`);
    }
    console.info('Transaction confirmed');

    // CALL getData TO RETRIEVE THE STORED DATA (CONTRACT)
    const storedData = await contract.getData(key);
    //const decodedValue = ethers.utils.toUtf8String(storedData);
    console.debug(`Data retrieved from blockchain for key ${key}:`, storedData);

  } catch (error) {
    console.error(`Error storing or retrieving data in blockchain for key ${key}:`, error.message);
    if (error.receipt) {
      console.error(`Transaction receipt: ${JSON.stringify(error.receipt)}`);
    }
    if (error.transaction) {
      console.error(`Transaction details: ${JSON.stringify(error.transaction)}`);
    }
  }
};

// DELETE A KEY FROM REDIS
const deleteKeyFromRedis = async (key) => {
  try {
    await redisClient.del(key);
    console.log(`Key ${key} deleted from Redis.`);
  } catch (err) {
    console.error('Error deleting key from Redis:', err);
  }
};

// READ DATA FROM REDIS
const extractAndStore = async () => {
  try {
    await ensureRedisConnection();
    
    // CONNECTION TO THE NODE
    const provider = new ethers.providers.JsonRpcProvider("http://hardhatnode_host:8545");
    const deployer = provider.getSigner();
  
    const { contractAddress } = JSON.parse(fs.readFileSync(path.resolve(__dirname, '../deployments.json'), 'utf8'));

    const abi = [
      "function storeData(string calldata key, bytes calldata value) external",
      "function getData(string calldata key) external view returns (bytes memory)"
    ];

    const contract = new ethers.Contract(contractAddress, abi, deployer);

    // GET ALL THE DATA FROM REDIS (KEYS)
    const keys = await redisClient.keys('*');

    if (keys.length === 0) {
      console.log('No data found in Redis.');
      return;
    }
    console.log('Keys found in Redis:', keys);
    
    // PROCESSED THE NEW KEYS
    for (const key of keys) {
      try {
        const buffer = await redisClient.get(key, { buffer: true });
        
        if (buffer) {
          await processBinaryData(key, buffer, contract);
          await deleteKeyFromRedis(key); // DELETE THE KEY FROM REDIS AFTER PROCESSING
        } else {
          console.error(`No binary data found for key: ${key}`);
        }
      } catch (err) {
        console.error('Error processing key:', key, err);
      }
      
    }
  } catch (err) {
    console.error('Error during extraction and storage:', err);
  }
};

// EXECUTE AND VERIFY EVERY 10 SECONDS
setInterval(extractAndStore, 10000);

// HANDLE ERROR
redisClient.on('error', (err) => {
  console.error('Redis error:', err);
});
