from scripts.extract import extract_from_folder
from scripts.embed import store_in_faiss

# Step 1: Extract
docs = extract_from_folder("data/images", "data/pptx")
# Step 2: Embed + Store in FAISS
store_in_faiss(docs)