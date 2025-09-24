# shared/db.py
from azure.cosmos import CosmosClient
import os

COSMOS_DB_URL = os.getenv("COSMOS_DB_URL", "https://localhost:8081/")
COSMOS_DB_KEY = os.getenv("COSMOS_DB_KEY", "your_local_key")
DATABASE_NAME = os.getenv("COSMOS_DB_NAME", "AvanochiDB")

client = CosmosClient(COSMOS_DB_URL, COSMOS_DB_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

def get_container(container_name: str, partition_key: str = "/id"):
    return database.create_container_if_not_exists(
        id=container_name,
        partition_key=partition_key,
        offer_throughput=400
    )
