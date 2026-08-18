import os
import chromadb

class VectorStore:
    def __init__(self):
        DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
        print(f"Initializing ChromaDB at {DB_DIR}")
        self.client = chromadb.PersistentClient(path=DB_DIR)
        self.collection = self.client.get_or_create_collection(name="finans_danismanim_docs")

    def add_documents(self, documents, embeddings, metadatas, ids):
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )
        
    def query(self, query_embeddings, n_results=4):
        return self.collection.query(
            query_embeddings=query_embeddings,
            n_results=n_results
        )

    def count(self):
        return self.collection.count()

    def delete_documents(self, ids):
        return self.collection.delete(ids=ids)


