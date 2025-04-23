#from azure.cosmos.partition_key import PartitionKey  # Import PartitionKey
from azure.cosmos import CosmosClient, exceptions
import base64
import json

encoded_data = "eyJsYXRpdHVkZSI6IDI1LjUsICJsb25naXR1ZGUiOiA2MC4yLCAiZGV2aWNlSWQiOiAiUmFzYmVycnlQaWUifQ=="

url = "https://poc-mqtt-messages-storage.documents.azure.com:443/"  # Replace with your Cosmos DB Endpoint
key = ""  # Replace with your Cosmos DB Key
database_name = "SampleDB"  # Replace with your Database Name
container_name = "SampleContainer"  # Replace with your Container Name

def decode_responce(item):
    decoded_bytes = base64.b64decode(item['Body'])
    decoded_json = decoded_bytes.decode('utf-8')
    data = json.loads(decoded_json)
    print(data)
    return data
        

def query_device_id(container, device_id):
    """
    Retrieves items that match a specific iothub-connection-device-id.
    """
    print("\n1. Query by Device ID:")
    query = f"SELECT * FROM c WHERE c.SystemProperties['iothub-connection-device-id'] = '{device_id}'"
    try:
        items = list(container.query_items(query=query,enable_cross_partition_query=True))
        if not items:
            print(f"   No items found with iothub-connection-device-id '{device_id}'.")
            return {}
        for item in items:
            print(f"   {item['id']}: {item['SystemProperties']['iothub-connection-device-id']}")
            print("done")
            data = decode_responce(item)
            return data
    except Exception as e:
        print(f"   Error querying by device ID: {e}")
        
def query_partition_key(container, partition_key_value):
    """
    Retrieves items that match a specific partition key.
    """
    print("\n2. Query by Partition Key:")
    query = f"SELECT * FROM c WHERE c.Properties.partitionKey = '{partition_key_value}'"
    try:
        items = list(container.query_items(query=query,enable_cross_partition_query=True
))
        if not items:
            print(f"   No items found with partitionKey '{partition_key_value}'.")
            return
        for item in items:
            print(item)
            print(f"   {item['id']}: {item['Body']}")
            return decode_responce(item)
            
    except Exception as e:
        print(f"   Error querying by partition key: {e}")


def createClient(deviceId):
    client = CosmosClient(url, credential=key)

    try:
        database = client.get_database_client(database_name)
        container = database.get_container_client(container_name)
        
        container.read()
        print("✅ Connected to container!")

        print("❌ Database or container not found. Check names and casing.")
    except Exception as e:
        print(f"❗ Unexpected error: {e}")
    
    return query_device_id(container,deviceId)
    
    #return query_partition_key(container,deviceId)