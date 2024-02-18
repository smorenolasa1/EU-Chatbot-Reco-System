// Truffle script to manage the deployment of smart contract to the Polygon network
const ReportStorage = artifacts.require("ReportStorage");

module.exports = function (deployer) {
  deployer.deploy(ReportStorage);
};
