#!/usr/bin/env bash

# ================================
#   Configuration Variables
# ================================

RESOURCE_GROUP="avanochi-rg"
LOCATION="spaincentral"
STORAGE_ACCOUNT="avanochistorage"
FUNCTION_APP="avanochi-funcapp"
COSMOS_ACCOUNT="avanochi-cosmosdb"
COSMOS_DB="avanochi-db"
COSMOS_CONTAINER="avanochi-container"
PLAN_LOCATION="westeurope"   # region for function consumption plan

# ================================
#   Create Azure Resource Group
# ================================

az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION

# ================================
#   Deploy Azure Storage Account
# ================================

az storage account create \
    --name $STORAGE_ACCOUNT \
    --location $LOCATION \
    --resource-group $RESOURCE_GROUP \
    --sku Standard_LRS

# ================================
#   Deploy Azure Function App
# ================================

az functionapp create \
    --resource-group $RESOURCE_GROUP \
    --consumption-plan-location $PLAN_LOCATION \
    --runtime python \
    --runtime-version 3.10 \
    --functions-version 4 \
    --name $FUNCTION_APP \
    --storage-account $STORAGE_ACCOUNT \
    --os-type linux

az functionapp config appsettings set \
    --name $FUNCTION_APP \
    --resource-group $RESOURCE_GROUP \
    --settings "AzureWebJobsFeatureFlags=EnableWorkerIndexing"

az functionapp restart \
    --name $FUNCTION_APP \
    --resource-group $RESOURCE_GROUP

# ================================
#   Deploy Azure Cosmos DB
# ================================

az cosmosdb create \
    --name $COSMOS_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --kind GlobalDocumentDB \
    --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False

# Create SQL database
az cosmosdb sql database create \
    --account-name $COSMOS_ACCOUNT \
    --name $COSMOS_DB \
    --resource-group $RESOURCE_GROUP

# Create container
az cosmosdb sql container create \
    --account-name $COSMOS_ACCOUNT \
    --database-name $COSMOS_DB \
    --name $COSMOS_CONTAINER \
    --partition-key-path "/id" \
    --resource-group $RESOURCE_GROUP

# ======================================
#   Extract Cosmos DB credentials
# ======================================

COSMOS_DB_URI=$(az cosmosdb show \
    --name $COSMOS_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --query "documentEndpoint" \
    -o tsv)

COSMOS_DB_PRIMARY_KEY=$(az cosmosdb keys list \
    --name $COSMOS_ACCOUNT \
    --resource-group $RESOURCE_GROUP \
    --type keys \
    --query "primaryMasterKey" \
    -o tsv)

# ===============================================
#   Inject Cosmos DB settings into Function App
# ===============================================

az functionapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $FUNCTION_APP \
    --settings \
    COSMOS_DB_URI=$COSMOS_DB_URI \
    COSMOS_DB_PRIMARY_KEY=$COSMOS_DB_PRIMARY_KEY \
    COSMOS_DB_DATABASE=$COSMOS_DB \
    COSMOS_DB_CONTAINER=$COSMOS_CONTAINER
