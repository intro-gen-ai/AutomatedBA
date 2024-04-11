import configparser
from pymilvus import (
    connections,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
    utility,
)

if __name__ == "__main__":
    # connect to milvus
    cfp = configparser.RawConfigParser()
    files_read = cfp.read("config_serverless.ini")

    # TO DO: un-hardcode
    milvus_uri = "https://in03-10fc789d75c4b64.api.gcp-us-west1.zillizcloud.com"
    token = "bf430bccd895611a762829314dcf5205ba81e416f365fa6104f94f4851542dfe3ba7a00a2453d61b20bd928a80a7d5b1453cc157"

    connections.connect("default", uri=milvus_uri, token=token)
    print(f"Connecting to DB: {milvus_uri}")

    # BA specific domain knowledge
    ba_collection_name = "ba_knowledge"
    ba_vector_dimension = 10  # Adjust based on your actual vector size

    # Check if the collection exists and create it if it doesn't
    if not utility.has_collection(ba_collection_name):
        connections.create_collection(ba_collection_name, ba_vector_dimension)
    else:
        print(f"Collection {ba_collection_name} already exists.")

    # SQL coding knowledge
    sql_collection_name = "sql_knowledge"
    sql_vector_dimension = 10  # Adjust based on your actual vector size

    # Check if the collection exists and create it if it doesn't
    if not utility.has_collection(sql_collection_name):
        connections.create_collection(sql_collection_name, sql_vector_dimension)
    else:
        print(f"Collection {sql_collection_name} already exists.")

    connections.disconnect("default")
