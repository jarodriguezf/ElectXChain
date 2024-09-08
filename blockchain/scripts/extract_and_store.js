const fs = require('fs');
const { ethers } = require('hardhat');
const redis = require('redis');
const path = require('path');
const { sendToKafka } = require('./producer_2');
const { Buffer } = require('node:buffer');

const redisHost = process.env.REDIS_HOST || 'localhost';
const redisPort = parseInt(process.env.REDIS_PORT, 10) || 6379;

// REDIS CLIENT
const redisClient = redis.createClient({
  socket: {
    host: redisHost,
    port: redisPort
  },
  database: 0
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
const processBinaryData = async (key, value, contract) => {
  console.log('Processing data for key:', key);
  
  try {

    let send_buffer = value
    if (Buffer.isBuffer(send_buffer) === false){
      send_buffer = Buffer.from(send_buffer, 'binary')
    }
    //console.debug(`Length of buffer before set in blockchain: ${send_buffer.length}`)

    const tx = await contract.storeData(key, send_buffer); //CALL storeData TO SAVED THE DATA (CONTRACT)
    const receipt = await tx.wait();

    if (receipt.status !== 1) {
      throw new Error(`Transaction failed for key ${key}`);
    }
    console.info('Transaction confirmed');

    // CALL getData TO RETRIEVE THE STORED DATA (CONTRACT)
    const storedData = await contract.getData(key);
    // console.debug(`Raw data from contract: ${storedData.length}`);// HEXADECIMAL
    // console.debug(`Raw data from contract: ${storedData}`);// HEXADECIMAL

    if (storedData && typeof storedData === 'string' && storedData.startsWith('0x')) {
      // CONVERSION ARRAY BYTES
      const valueBytesArray = ethers.utils.arrayify(storedData);
      //console.debug(`Array of bytes length after conversion: ${valueBytesArray.length}`);

      // CONVERSION BYTES
      const valueBytes = Buffer.from(valueBytesArray, 'binary');
      //console.debug(`Bytes length after conversion: ${valueBytes.length}`);

      // SEND THE KEY AND VALUE TO KAFKA PRODUCER
      await sendToKafka(key, valueBytes);
      console.log('Message successfully send to kafka producer: vote_result.');
    } else {
      console.error('Data retrieved from contract is not in the expected format');
      return;
    }

  } catch (error) {
    console.error(`Error storing or retrieving data in blockchain or kafka for key ${key}:`, error.message);
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
        const result  = await redisClient.sendCommand(['GET', key], {
          returnBuffers: true
        });
      
        if (result) {
          // const valueHex = result.toString('hex');
          // console.debug(`Length of value retrieved from Redis: ${valueHex.length}`);
          // console.debug(`Value representation from Redis:`, valueHex);
          await processBinaryData(key, result, contract);
          await deleteKeyFromRedis(key)
        }else {
          console.error(`Unexpected type for key ${key}: ${typeof result}`);
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
