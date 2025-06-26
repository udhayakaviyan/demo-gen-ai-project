import faiss
import numpy as np
import requests
import os
import pickle

PERSIST_PATH = "vector_store"

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]

def store_in_faiss(docs):
    os.makedirs(PERSIST_PATH, exist_ok=True)
    index = faiss.IndexFlatL2(768)
    vectors = []
    metadata = []

    for doc in docs:
        embedding = generate_embedding(doc["content"])
        vectors.append(normalize(np.array(embedding, dtype="float32")))
        metadata.append(doc)
    index.add(np.array(vectors, dtype="float32"))
    faiss.write_index(index, os.path.join(PERSIST_PATH, "index.faiss"))

    with open(os.path.join(PERSIST_PATH, "metadata.pkl"), "wb") as f:
        pickle.dump(metadata, f)
def normalize(vec):
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec