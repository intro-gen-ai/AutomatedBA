import configparser
from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

if __name__ == '__main__':
    # connect to milvus
    cfp = configparser.RawConfigParser()
    cfp.read('config_serverless.ini')
    milvus_uri = cfp.get('prior-knowledge', 'uri')
    token = cfp.get('prior-knowledge', 'token')

    connections.connect("default",
                        uri=milvus_uri,
                        token=token)
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