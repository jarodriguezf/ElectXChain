// Importar ethers desde Hardhat
const { ethers } = require("hardhat");
const fs = require('fs');

async function main() {
  // GET THE CONTRACT
  const Contract = await ethers.getContractFactory("data_blockchain");

  // DEPLOY
  console.log("Deployment the contract...");

  const contract = await Contract.deploy();

  await contract.deployed();

  console.log("Contract deployed in the address:", contract.address);
  // CREATE A JSON ADDRESS FILE
  fs.writeFileSync('deployments.json', JSON.stringify({ contractAddress: contract.address }));
}

// HANDLE ERROR
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
