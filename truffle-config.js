require('dotenv').config();
const HDWalletProvider = require('@truffle/hdwallet-provider');

const mnemonic = process.env.MNEMONIC;
const infuraProjectId = process.env.INFURA_PROJECT_ID;

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545, // Default port for Ganache; adjust if you're using a different port
      network_id: "*", // Match any network id
    },
    mumbai: {
      provider: () =>
        new HDWalletProvider({
          mnemonic: {
            phrase: mnemonic
          },
          providerOrUrl: `https://polygon-mumbai.infura.io/v3/${infuraProjectId}`,
          // Additional options if needed:
          // numberOfAddresses: 1,
          // shareNonce: true,
          // derivationPath: "m/44'/60'/0'/0/"
        }),
      network_id: 80001,
      confirmations: 2,
      timeoutBlocks: 200,
      skipDryRun: true
    },
  },
  compilers: {
    solc: {
      version: "^0.8.0", // Specify the Solidity compiler version you are using
      settings: {
        optimizer: {
          enabled: true,
          runs: 200 // Optimize for how many times you intend to run the code
        },
      },
    },
  },
  // This line enables the Truffle Dashboard which might be helpful for public networks.
  // It's a newer feature, so feel free to remove it if you don't use the dashboard.
  dashboard: {
    port: 25012,
    host: "localhost"
  },
};
