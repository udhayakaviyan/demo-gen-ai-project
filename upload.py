import streamlit as st
from scripts.extract import extract_from_folder
from scripts.embed import store_in_faiss
from scripts.query import query_ollama_with_context
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Step 1: Extract
# docs = extract_from_folder("data/images", "data/pptx")
# # Step 2: Embed + Store in FAISS
# store_in_faiss(docs)

# import os
# from scripts.extract import extract_from_folder
# from scripts.embed import store_in_faiss

# Title
st.set_page_config(page_title="AI Doc Assistant", layout="centered")
st.title("Document Intelligence with Mistral")

# Create folders
pptx_folder = "data/pptx"
image_folder = "data/images"
os.makedirs(pptx_folder, exist_ok=True)
os.makedirs(image_folder, exist_ok=True)

# --- Upload Section ---
with st.expander("📤 Upload & Index Files"):
    uploaded_files = st.file_uploader(
        "Upload PowerPoint (.pptx/.ppt) or image files (.png/.jpg/.jpeg)",
        type=["pptx", "ppt", "png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if uploaded_files:
        st.success(f"✅ Uploaded {len(uploaded_files)} file(s)")
        for file in uploaded_files:
            ext = file.name.split(".")[-1].lower()
            folder = pptx_folder if ext in ["pptx", "ppt"] else image_folder
            filepath = os.path.join(folder, file.name)
            with open(filepath, "wb") as f:
                f.write(file.getbuffer())

        if st.button("🔍 Extract & Store in Vector DB"):
            with st.spinner("Processing files and building FAISS index..."):
                docs = extract_from_folder(image_folder, pptx_folder)
                store_in_faiss(docs)
                st.success(f"✅ Processed and stored {len(docs)} document(s)")

with st.expander("💬 Ask a Question"):
    query = st.text_input("What do you want to know?")

    if query and st.button("Ask"):
        st.subheader("🤖 Mistral Says:")
        status = st.status("Thinking...")
        container = st.empty()
        full_response = ""
        text ="You are an expert assistant. Use the context below to answer the user question as precisely and accurately as possible from given embedding context.the question is "
        print(text+query)
        for i, chunk in enumerate(query_ollama_with_context(text+query)):
            if i == 0:
                status.update(label="generating",state= "running")
            full_response += chunk
            container.markdown(full_response)

        status.update(label="Done", state="complete")
