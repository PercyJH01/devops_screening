import gzip
import json
from azure.storage.blob import BlobServiceClient
from azure.cosmos import CosmosClient

COSMOS_CONN = "<cosmos_connection_string>"
BLOB_CONN = "<blob_connection_string>"
DB_NAME = "BillingDB"
CONTAINER = "Records"
BLOB_CONTAINER = "billing-archive"

client = CosmosClient.from_connection_string(COSMOS_CONN)
db = client.get_database_client(DB_NAME)
container = db.get_container_client(CONTAINER)

blob_service = BlobServiceClient.from_connection_string(BLOB_CONN)
blob_container = blob_service.get_container_client(BLOB_CONTAINER)

def get_billing_record(record_id):
    try:
        return container.read_item(item=record_id, partition_key=record_id)
    except:
        for blob in blob_container.list_blobs(name_starts_with="billing-archive/"):
            blob_data = blob_container.download_blob(blob.name).readall()
            records = json.loads(gzip.decompress(blob_data).decode('utf-8'))
            for rec in records:
                if rec['id'] == record_id:
                    return rec
    return None
