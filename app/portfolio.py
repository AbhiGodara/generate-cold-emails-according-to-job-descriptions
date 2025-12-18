import pandas as pd
import chromadb
import uuid

class Portfolio:
    def __init__(self, path="app/resources/my_portfolio.csv"):
        self.data = pd.read_csv(path)
        self.client = chromadb.PersistentClient("vectorstore")
        self.collection = self.client.get_or_create_collection("portfolio")

    def load(self):
        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"link": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query(self, skills):
        if not skills:
            return []

        results = self.collection.query(
            query_texts=skills,
            n_results=2
        )

        metadatas = results.get("metadatas", [])

        links = []
        for group in metadatas:
            for item in group:
                if "link" in item:
                    links.append(item["link"])

        return links

