import faiss
import numpy as np
import ollama
import requests
import pickle
import os

PERSIST_PATH = "vector_store"

def generate_embedding(text: str) -> list[float]:
    response = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": "nomic-embed-text", "prompt": text}
    )
    response.raise_for_status()
    return response.json()["embedding"]

def query_ollama_with_context(text:str,query: str, top_k: int = 1) -> str:
    index = faiss.read_index(os.path.join(PERSIST_PATH, "index.faiss"))
    with open(os.path.join(PERSIST_PATH, "metadata.pkl"), "rb") as f:
        docs = pickle.load(f)
    query_embedding = np.array([generate_embedding(query)], dtype="float32")
    distances, indices = index.search(query_embedding,top_k)
    print(distances,indices)
    matched_docs = []
    # matched_docs = [docs[i]["content"] for i in indices[0] if i < len(docs) and distances < DISTANCE_THRESHOLD]
    for i, dist in zip(indices[0], distances[0]):
        if i < len(docs):
            doc = docs[i]
            content = doc["content"] if isinstance(doc, dict) else doc
            matched_docs.append(content)
    context = "\n\n".join(matched_docs)
    print(matched_docs,"iiiiiiiiiiiiiii")
    if not matched_docs:
        return "No relveant info found "
    # print(context)
    prompt = f"{text}Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
    try:
        response = ollama.chat(
        model='mistral',
        messages=[
        {"role": "user", "content": prompt}
        ],stream=True
        )
        for chunk in response:
            yield  chunk['message']['content']    
    except Exception as e:
        print(f"\n Error: {e}") 
    # response.raise_for_status()
    # print("response",response)
    #return response.json()["response"].strip()
