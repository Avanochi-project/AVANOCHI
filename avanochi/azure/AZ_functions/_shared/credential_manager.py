# shared/credential_manager.py

import os
from dotenv import load_dotenv

class CredentialManager:

    def __init__(self, env_path: str = None):
        # Load the .env file if a path is provided.
        if env_path:
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()  # Fallback to default .env in project root

    def get_cosmos_credentials(self):        
        # Retrieve Cosmos DB credentials from environment variables.
        return {
            "account_name": os.getenv("COSMOS_DB_ACCOUNT", ""),
            "database_name": os.getenv("COSMOS_DB_DATABASE", ""),
            "container_name": os.getenv("COSMOS_DB_CONTAINER", ""),
            "uri": os.getenv("COSMOS_DB_URI", ""),
            "primary_key": os.getenv("COSMOS_DB_PRIMARY_KEY", "")
        }

    def get_azure_credentials(self):
        # Retrieve general Azure credentials (example: subscription, tenant, client ID).
        return {
            "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID", ""),
            "tenant_id": os.getenv("AZURE_TENANT_ID", ""),
            "client_id": os.getenv("AZURE_CLIENT_ID", ""),
            "client_secret": os.getenv("AZURE_CLIENT_SECRET", "")
        }

    def get(self, key: str, default: str = None):
        # Retrieve any environment variable by key.
        return os.getenv(key, default)
