from ..step import Step
from langchain_openai import OpenAIEmbeddings
from pymilvus import connections, Collection


class KnowledgeInjectionStep(Step):
    def __init__(
        self,
        order,
        client,
        collection_name,
        file_path,
        model="text-embedding-3-small",
        top_k=5,
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

    def run(self, args):
        if "prompt" not in args:
            raise ValueError("Prompt not provided in arguments")
        base_prompt = args["prompt"]
        similar_doc_ids = self.retrieve_similar_documents(base_prompt)
        knowledge_texts = [
            self.fetch_document_text_by_line_number(line_num)
            for line_num in similar_doc_ids
        ]
        return self.construct_prompt_with_knowledge(base_prompt, knowledge_texts)

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
        # Retrieve the specific line from the file using the line number
        with open(self.file_path, "r") as file:
            for current_line, text in enumerate(file, 1):
                if current_line == line_num:
                    return text.strip()
        return f"Document text for line {line_num} not found"

    def construct_prompt_with_knowledge(self, base_prompt, knowledge_texts):
        combined_prompt = (
            base_prompt + "\nRelevant context:\n" + "\n".join(knowledge_texts)
        )
        return combined_prompt
