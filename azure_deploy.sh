# Azure CLI Deployment Script
# Variables
RESOURCE_GROUP="BillingSolutionRG"
LOCATION="eastus"
STORAGE_ACCOUNT="billingarchive$(date +%s)"
FUNCTION_APP="billingfuncapp$(date +%s)"
COSMOS_ACCOUNT="billingcosmos$(date +%s)"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Storage Account
az storage account create --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP --location $LOCATION --sku Standard_LRS

# Create Blob Container
az storage container create --name billing-archive --account-name $STORAGE_ACCOUNT

# Create Cosmos DB Account
az cosmosdb create --name $COSMOS_ACCOUNT --resource-group $RESOURCE_GROUP --locations regionName=$LOCATION failoverPriority=0

# Create Serverless Function App
az functionapp create --resource-group $RESOURCE_GROUP --consumption-plan-location $LOCATION --runtime python --functions-version 4 --name $FUNCTION_APP --storage-account $STORAGE_ACCOUNT
