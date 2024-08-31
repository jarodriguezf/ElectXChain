// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract data_blockchain {
    mapping(string => bytes) private data; // KEY->VALUE

    event DataStored(string key, bytes value);// EVENT FOR THE SAVED DATA

    // STORE NEW DATA IN THE MAPPER OBJECT
    function storeData(string calldata key, bytes calldata value) external {
        // SAVE THE VALUE
        data[key] = value;
        emit DataStored(key, value);
    }
    
    // GET THE DATA SAVED IN THE MAPPER OBJECT
    function getData(string calldata key) external view returns (bytes memory) {
        // Devolver el valor almacenado para la clave dada
        return data[key];
    }
}
