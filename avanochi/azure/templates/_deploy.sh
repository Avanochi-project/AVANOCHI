# ================================
#   Create Azure Resource Group
# ================================

az group create \
  --name avanochi-rg \
  --location spaincentral

# ================================
#   Deploy Azure Storage Account
# ================================

az storage account create \
  --name avanochistorage \
  --location spaincentral \
  --resource-group avanochi-rg \
  --sku Standard_LRS

# ================================
#   Deploy Azure Function App
# ================================

az functionapp create \
  --resource-group avanochi-rg \
  --consumption-plan-location westeurope \
  --runtime python \
  --runtime-version 3.10 \
  --functions-version 4 \
  --name avanochi-funcapp \
  --storage-account avanochistorage \
  --os-type linux

az functionapp config appsettings set \
  --name avanochi-funcapp \
  --resource-group avanochi-rg \
  --settings "AzureWebJobsFeatureFlags=EnableWorkerIndexing"

az functionapp restart \
  --name avanochi-funcapp \
  --resource-group avanochi-rg

# ================================
#   Deploy Azure Cosmos DB
# ================================

az cosmosdb create \
  --name avanochi-cosmosdb \
  --resource-group avanochi-rg \
  --kind GlobalDocumentDB \
  --locations regionName=spaincentral failoverPriority=0 isZoneRedundant=False

# Create SQL database
az cosmosdb sql database create \
  --account-name avanochi-cosmosdb \
  --name avanochi-db \
  --resource-group avanochi-rg

# Create container
az cosmosdb sql container create \
  --account-name avanochi-cosmosdb \
  --database-name avanochi-db \
  --name avanochi-container \
  --partition-key-path "/user_id" \
  --resource-group avanochi-rg

# ======================================
#   Connection string for Funciton App
# ======================================

COSMOS_CONN=$(az cosmosdb keys list \
  --name avanochi-cosmosdb \
  --resource-group avanochi-rg \
  --type connection-strings \
  --query "connectionStrings[0].connectionString" \
  -o tsv)

az functionapp config appsettings set \
  --resource-group avanochi-rg \
  --name avanochi-funcapp \
  --settings "COSMOSDB_CONNECTION_STRING=$COSMOS_CONN"
