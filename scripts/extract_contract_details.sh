#!/bin/bash

# Make sure jq is installed in your CI/CD environment

CONTRACT_JSON=./build/contracts/ReportStorage.json
OUTPUT_DIR=./config
OUTPUT_CONFIG=$OUTPUT_DIR/contractDetails.json
NETWORK_ID=80001  # Adjust based on the target network

# Check if the output directory exists, create it if not
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi

CONTRACT_ADDRESS=$(jq -r ".networks[\"$NETWORK_ID\"].address" $CONTRACT_JSON)
CONTRACT_ABI=$(jq '.abi' $CONTRACT_JSON)

echo "{\"address\": \"$CONTRACT_ADDRESS\", \"abi\": $CONTRACT_ABI}" > $OUTPUT_CONFIG
