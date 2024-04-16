from ..step import Step
from langchain_openai import OpenAIEmbeddings
from pymilvus import Collection, connections, utility
import os


class KnowledgeInjectionStep(Step):
    def __init__(
        self,
        client,
        collection_name,
        file_path,
        prompt,
        model="text-embedding-3-small",
        top_k=5,
        order = 0
    ):
        super().__init__()
        self.order = order
        self.client = client  # OpenAIEmbeddings client
        self.collection_name = collection_name
        self.file_path = (
            file_path  # Path to the .txt file containing the knowledge base
        )
        self.model = model
        self.top_k = top_k
        self.user_in = prompt

    def run(self, args):
        base_prompt = self.user_in #args["prompt"]
        #if "prompt" not in args:
        #    raise ValueError("Prompt not provided in arguments")
        similar_doc_ids = self.retrieve_similar_documents(base_prompt)
        knowledge_texts = [
            self.fetch_document_text_by_line_number(line_num)
            for line_num in similar_doc_ids
        ]
        
        args["rag_set"]=knowledge_texts
        return args

    def getRequirements(self):
        return [self.file_path]

    def retrieve_similar_documents(self, query_text):
        query_vector = (
            self.client.embeddings.create(input=[query_text], model=self.model)
            .data[0]
            .embedding
        )
        self.check_milvus_connection()
        collection = Collection(name=self.collection_name)

        print(self.collection_name)
        
        collection.load()
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}

        results = collection.search(
            data=[query_vector], 
            anns_field="vector", 
            param = search_params, 
            limit = self.top_k, 
            output_fields = ["id"]
        )
        return [
            hit.id for hit in results[0]
        ]  # Assuming the ID corresponds to the line number in the file

    def fetch_document_text_by_line_number(self, line_num):
        try:
            with open(self.file_path, "r") as file:
                for current_line, text in enumerate(file, 1):
                    if current_line == line_num:
                        return text.strip()
            raise ValueError(f"Document text for line {line_num} not found")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {self.file_path} not found")
    
    def check_milvus_connection(self):
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
