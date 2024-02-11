# Data Schema


## Overview

The database schema for the dairy farmers' carbon emission reporting project integrates a relational model to facilitate data collection through a WhatsApp chatbot and secure storage on the Polygon blockchain. It comprises three main tables: Users, Emission Report, and Blockchain Transaction. These tables store detailed farmer profiles, carbon emission reports with quantitative and qualitative data, and immutable transaction records linking each report to a specific blockchain entry.

## Tables

### Table 1: Users

| Field          | Type          | Description                                         |
|----------------|---------------|-----------------------------------------------------|
| **FarmerID**   | `VARCHAR(255)` | Unique identifier for each farmer.                 |
| **Name**       | `VARCHAR(255)` | Farmer's full name.                                 |
| **WhatsAppNumber** | `VARCHAR(15)`  | Contact number used for WhatsApp communication.    |
| **FarmLocation**   | `VARCHAR(255)` | Geographical location of the farm.                 |
| **FarmSize**       | `DECIMAL`      | Size of the farm (e.g., in hectares).              |


### Table 2: Emission Report

| Field            | Type           | Description                                             |
|------------------|----------------|---------------------------------------------------------|
| **ReportID**     | `VARCHAR(255)` | Unique identifier for each emission report.            |
| **FarmerID**     | `VARCHAR(255)` | Links to Farmer Information.                           |
| **ReportDate**   | `DATE`         | Date when the report was submitted.                    |
| **EmissionType** | `VARCHAR(50)`  | Type of emission (e.g., methane, CO2).                 |
| **EmissionSource** | `VARCHAR(255)` | Source of emission within the farm (e.g., livestock, machinery). |
| **Quantity**       | `DECIMAL`      | Quantified emission (e.g., in kilograms of CO2 equivalent). |
| **CalculationMethod**| `VARCHAR(255)` | Method or model used for emission calculation |

### Table 3: Blockchain Transaction

| Field            | Type          | Description                                                      |
|------------------|---------------|------------------------------------------------------------------|
| **TransactionID** | `VARCHAR(255)`| Unique identifier for the blockchain transaction.               |
| **ReportID**      | `VARCHAR(255)`| Links to Emission Report.                                        |
| **TransactionHash** | `VARCHAR(255)`| Hash of the transaction on the Polygon blockchain.               |
| **Timestamp**      | `DATETIME`    | Date and time when the transaction was recorded on the blockchain.|
| **BlockNumber**    | `INT`         | The block number on the Polygon blockchain where the transaction was recorded.|
| **WalletAddress**  | `VARCHAR(255)`| The blockchain wallet address used for the transaction.          |
