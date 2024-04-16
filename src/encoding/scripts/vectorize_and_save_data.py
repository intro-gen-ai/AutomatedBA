import configparser
import os
import time
from openai import OpenAI, RateLimitError
from langchain.text_splitter import CharacterTextSplitter
from pymilvus import connections, Collection, FieldSchema, DataType, CollectionSchema
from langchain_community.document_loaders import TextLoader
from src.util import get_requirement_file 

def get_embedding_with_retry(
    client, text, model="text-embedding-3-small", max_retries=5
):
    retry_count = 0
    while retry_count < max_retries:
        try:
            text = text.replace("\n", " ")
            print("Getting embedding for:", text)
            return client.embeddings.create(input=[text], model=model).data[0].embedding
        except RateLimitError:
            wait_time = 2**retry_count  # Exponential backoff
            print(
                f"Rate limit exceeded, waiting for {wait_time} seconds before retrying..."
            )
            time.sleep(wait_time)
            retry_count += 1
    raise Exception(
        "Failed to get embedding after several retries due to rate limiting."
    )


def check_milvus_connection():
    # TO DO: un-hardcode
    try:
        milvus_uri = "https://in03-10fc789d75c4b64.api.gcp-us-west1.zillizcloud.com"
        token = "bf430bccd895611a762829314dcf5205ba81e416f365fa6104f94f4851542dfe3ba7a00a2453d61b20bd928a80a7d5b1453cc157"
        connections.connect("default", uri=milvus_uri, token=token)
        print(f"Connecting to DB: {milvus_uri}")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        return False
    return True


def check_data_folder(path="../data/"):
    if not os.path.exists(path):
        print(f"Data folder '{path}' does not exist.")
        return False
    return True


def vectorize_and_store(client, file_path, collection_name):
    text_loader = TextLoader(file_path)
    docs = text_loader.load()
    vectors = []
    ids = []  # List to store unique IDs for each vector
    doc_id = 0  # Start with an ID, increment for each line/document

    for doc in docs:
        print(doc)
        lines = doc.page_content.split("\n")  # Split the document into lines
        for line in lines:
            if line.strip():  # Only process non-empty lines
                embedding = get_embedding_with_retry(client, line)
                vectors.append(embedding)
                ids.append(doc_id)
                doc_id += 1  # Increment the ID for the next line/document

    # Define the schema with a key field
    id_field = FieldSchema(
        name="id", dtype=DataType.INT64, is_primary=True, auto_id=False
    )
    vector_field = FieldSchema(
        name="vector", dtype=DataType.FLOAT_VECTOR, dim=len(vectors[0])
    )
    collection_schema = CollectionSchema(fields=[id_field, vector_field])

    # Create the collection
    collection = Collection(name=collection_name, schema=collection_schema)

    # Prepare the data for insertion (combining IDs and vectors)
    entities = [
        {"id": id_val, "vector": vector} for id_val, vector in zip(ids, vectors)
    ]

    # Insert data into the collection
    collection.insert(entities)


def main(client):
    if check_milvus_connection() and check_data_folder("../data"):
        # Vectorize and store BA knowledge
        ba_file_path = "../data/ba_knowledge.txt"
        vectorize_and_store(client, ba_file_path, "ba_knowledge")

        # Vectorize and store SQL knowledge
        sql_file_path = "../data/sql_knowledge.txt"
        vectorize_and_store(client, sql_file_path, "sql_knowledge")

        connections.disconnect("default")

if __name__ == "__main__":
    openai_api_key = get_requirement_file(".openai_secret")
    # openai_api_key = os.getenv()
    if not openai_api_key:
        raise KeyError("No OpenAI Key Provided")
    client = OpenAI(api_key=openai_api_key)
    main(client)