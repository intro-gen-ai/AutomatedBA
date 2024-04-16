from ..step import Step
from langchain_openai import OpenAIEmbeddings
from pymilvus import Collection, connections
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
        self.prompt = prompt

    def run(self, args):
        base_prompt = self.prompt #args["prompt"]
        #if "prompt" not in args:
        #raise ValueError("Prompt not provided in arguments")
        similar_doc_ids = self.retrieve_similar_documents(base_prompt)
        knowledge_texts = [
            self.fetch_document_text_by_line_number(line_num)
            for line_num in similar_doc_ids
        ]
        return [base_prompt, knowledge_texts]

    def getRequirements(self):
        return [self.file_path]

    def retrieve_similar_documents(self, query_text):
        query_vector = (
            self.client.embeddings.create(input=[query_text], model=self.model)
            .data[0]
            .embedding
        )
        collection = Collection(name=self.collection_name)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        results = collection.search(
            [query_vector], "vector", search_params, self.top_k, "id"
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
