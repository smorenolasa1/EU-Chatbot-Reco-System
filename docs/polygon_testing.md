# Getting Started With Testing Smart Contract Deployment

To locally test your smart contract for the Polygon storage solution using Truffle, follow these steps, assuming you already have a test report contract but need to set up a `.env` file and adjust your Truffle configuration for local testing.

### Prerequisites

Ensure Node.js (v12.x or higher) and Truffle are installed. If not, install Truffle globally using npm:

```sh
npm install -g truffle
```

### Step 1: Set Up Your `.env` File for Local Testing

Since your `truffle-config.js` expects environment variables, create a `.env` file in your project's root directory for local development purposes. For local testing, you won't need actual values for `MNEMONIC` or `INFURA_PROJECT_ID`. Instead, you'll configure Truffle to use Ganache as your local blockchain.

```plaintext
# .env file content for local testing
MNEMONIC='candy maple cake sugar pudding cream honey rich smooth crumble sweet treat'
INFURA_PROJECT_ID=dummyValueNotUsedLocally
```

### Step 2: Install Required npm Packages

Ensure `dotenv` and `@truffle/hdwallet-provider` are installed. If you haven't installed them yet, run:

```sh
npm install dotenv @truffle/hdwallet-provider
```

### Step 3: Adjust `truffle-config.js` for Local Development

Modify your `truffle-config.js` to include a configuration for local development using Ganache. You can either modify the existing file or create a new network configuration specifically for Ganache.

1. **Install Ganache**: Download Ganache from [trufflesuite.com/ganache](https://www.trufflesuite.com/ganache) and start it.

2. **Configure Local Network in `truffle-config.js`**:
   Add a development network configuration to use Ganache:

```javascript
require('dotenv').config();
const HDWalletProvider = require('@truffle/hdwallet-provider');

const mnemonic = process.env.MNEMONIC; // Used for other networks, not local

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545, // Default Ganache port
      network_id: "*", // Match any network
    },
    mumbai: {
      // Your existing Mumbai network configuration
    },
  },
  compilers: {
    solc: {
      version: "^0.8.0",
    }
  }
};
```

This setup allows you to use Ganache for local testing without affecting your existing Mumbai testnet configuration.

### Step 4: Compile and Migrate Your Contract Locally

1. **Compile Your Smart Contract**:
   ```sh
   truffle compile
   ```

2. **Migrate the Contract to Ganache**:
   Ensure Ganache is running, then execute:
   ```sh
   truffle migrate --network development
   ```

### Step 5: Test Your Contract

You can interact with your contract in a Truffle console connected to Ganache:

```sh
truffle console --network development
```

Inside the console, you can interact with your deployed contract, for example:

```javascript
let instance = await ReportStorage.deployed()
await instance.storeReport("1", "hash1")
let reportHash = await instance.getReportHash("1")
console.log(reportHash)
```

### Conclusion

You've now set up a local development environment suitable for testing your Polygon storage solution smart contract using Ganache and Truffle. This approach allows for rapid development and testing without the need for real MNEMONIC or INFURA_PROJECT_ID values, nor incurring transaction costs on the Mumbai testnet.

**Note**: When deploying to the Mumbai testnet the transaction cost consist of testnet MATIC, which does not have real-world value. Testnet MATIC can be freely obtained from various faucets provided by the community or the Polygon team.

