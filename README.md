# Azure Cost Optimization Solution - Full Package

This solution reduces Cosmos DB costs by archiving old billing records to Azure Blob Storage.

## Contents:
- archive_old_records.py: Archives old records.
- retrieve_record.py: Retrieves records from Cosmos DB or archive.
- azure_deploy.sh: Azure CLI script for resource deployment.
- architecture.png: Visual architecture diagram.

## Steps:
1. Deploy resources with `azure_deploy.sh`.
2. Configure Function Apps for archive and retrieval logic.
3. Set Blob lifecycle policies for Cool/Archive tiers.

