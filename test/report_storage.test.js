const ReportStorage = artifacts.require("ReportStorage");

contract("ReportStorage", (accounts) => {
  let reportStorage = null;
  before(async () => {
    reportStorage = await ReportStorage.deployed();
  });

  it("should store a report hash", async () => {
    await reportStorage.storeReport("report1", "hash1", { from: accounts[0] });
    const report = await reportStorage.reports("report1");
    assert(report.reportHash === "hash1", "The report hash was not stored correctly.");
  });

  it("should retrieve a report hash", async () => {
    const reportHash = await reportStorage.getReportHash("report1");
    assert(reportHash === "hash1", "The report hash was not retrieved correctly.");
  });
});
