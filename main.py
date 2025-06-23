from scripts.extract import extract_from_folder
from scripts.embed import store_in_faiss
from scripts.query import query_ollama_with_context

# Step 1: Extract
docs = extract_from_folder("data/images", "data/pptx")

# Step 2: Embed + Store in FAISS
store_in_faiss(docs)

#Step 3: Query
query = "What is product backlog?"
answer = query_ollama_with_context(query)
#print("\nAnswer:\n", answer)
