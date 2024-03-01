import configparser
import os
import time
from openai import OpenAI, RateLimitError
from langchain.text_splitter import CharacterTextSplitter
from pymilvus import connections, Collection, FieldSchema, DataType, CollectionSchema
from langchain_community.document_loaders import TextLoader


def get_embedding_with_retry(client, text, model="text-embedding-3-small", max_retries=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            text = text.replace("\n", " ")
            print("Getting embedding for:", text)
            return client.embeddings.create(input=[text], model=model).data[0].embedding
        except RateLimitError:
            wait_time = 2 ** retry_count  # Exponential backoff
            print(f"Rate limit exceeded, waiting for {wait_time} seconds before retrying...")
            time.sleep(wait_time)
            retry_count += 1
    raise Exception("Failed to get embedding after several retries due to rate limiting.")


def check_milvus_connection():
    try:
        cfp = configparser.RawConfigParser()
        cfp.read('config_serverless.ini')
        milvus_uri = cfp.get('prior-knowledge', 'uri')
        token = cfp.get('prior-knowledge', 'token')
        connections.connect("default", uri=milvus_uri, token=token)
        print(f"Connecting to DB: {milvus_uri}")
    except Exception as e:
        print(f"Failed to connect to Milvus: {e}")
        return False
    return True


def check_data_folder(path="../data"):
    if not os.path.exists(path):
        print(f"Data folder '{path}' does not exist.")
        return False
    return True


def vectorize_and_store(client, file_path, collection_name):
    text_loader = TextLoader(file_path)
    docs = text_loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=0)
    vectors = []
    ids = []  # List to store unique IDs for each vector
    doc_id = 0  # Start with an ID, increment for each vector

    for doc in docs:
        print(doc)
        chunks = text_splitter.split_text(doc.page_content)
        for chunk in chunks:
            vectors.append(get_embedding_with_retry(client, chunk))
            ids.append(doc_id)
            doc_id += 1  # Increment the ID for the next vector

    # Define the schema with a key field
    id_field = FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=False)
    vector_field = FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=len(vectors[0]))
    collection_schema = CollectionSchema(fields=[id_field, vector_field])

    # Create the collection
    collection = Collection(name=collection_name, schema=collection_schema)

    # Prepare the data for insertion (combining IDs and vectors)
    entities = [{"id": id_val, "vector": vector} for id_val, vector in zip(ids, vectors)]

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
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        openai_api_key="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"
    client = OpenAI(api_key=openai_api_key)
    main(client)