// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ReportStorage {
    struct Report {
        string reportID;
        string reportHash;
    }

    mapping(string => Report) public reports;

    function storeReport(string memory reportID, string memory reportHash) public {
        reports[reportID] = Report(reportID, reportHash);
    }

    function getReportHash(string memory reportID) public view returns (string memory) {
        return reports[reportID].reportHash;
    }
}
