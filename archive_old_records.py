import azure.cosmos.cosmos_client as cosmos_client
from azure.storage.blob import BlobServiceClient
import gzip
import json
from datetime import datetime, timedelta

COSMOS_CONN = "<cosmos_connection_string>"
BLOB_CONN = "<blob_connection_string>"
DB_NAME = "BillingDB"
CONTAINER = "Records"
BLOB_CONTAINER = "billing-archive"

client = cosmos_client.CosmosClient.from_connection_string(COSMOS_CONN)
db = client.get_database_client(DB_NAME)
container = db.get_container_client(CONTAINER)

blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

def archive_old_records():
    cutoff = datetime.utcnow() - timedelta(days=90)
    query = f"SELECT * FROM c WHERE c.timestamp < '{cutoff.isoformat()}'"
    old_records = list(container.query_items(query=query, enable_cross_partition_query=True))

    if old_records:
        file_name = f"{cutoff.year}/{cutoff.month}/archive-{datetime.utcnow().timestamp()}.json.gz"
        compressed_data = gzip.compress(json.dumps(old_records).encode('utf-8'))

        blob_container.upload_blob(file_name, compressed_data)

        for record in old_records:
            container.delete_item(record['id'], partition_key=record['partitionKey'])
