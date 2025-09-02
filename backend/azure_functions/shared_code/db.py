import os
from azure.cosmos import CosmosClient, PartitionKey

COSMOS_URI = os.getenv("COSMOS_URI")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_VERIFY = os.getenv("COSMOS_VERIFY", "true").lower() == "true"

DATABASE_NAME = os.getenv("COSMOS_DB_NAME", "todoapp")
USER_CONTAINER = os.getenv("COSMOS_USERS_CONTAINER", "users")
TASK_CONTAINER = os.getenv("COSMOS_TASKS_CONTAINER", "tasks")

# connection_verify=False evita problemas de certificado en el emulador
client = CosmosClient(
    COSMOS_URI, credential=COSMOS_KEY, connection_verify=COSMOS_VERIFY
)
db = client.create_database_if_not_exists(id=DATABASE_NAME)

users = db.create_container_if_not_exists(
    id=USER_CONTAINER, partition_key=PartitionKey(path="/email")
)

tasks = db.create_container_if_not_exists(
    id=TASK_CONTAINER, partition_key=PartitionKey(path="/userId")
)
