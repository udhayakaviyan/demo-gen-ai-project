import streamlit as st
from scripts.query import query_ollama_with_context

# query = "stages in agile development methodology, give instructured format?"
# answer = query_ollama_with_context(query)
# from scripts.query import query_ollama_with_context  # or however you import

st.title("💬 Ask Mistral with Context")

query = st.text_input("Enter your question:")

if query and st.button("Ask"):
    st.subheader("🤖 Mistral Says:")
    output_area = st.empty()
    full_response = ""

    for chunk in query_ollama_with_context(query):
        full_response += chunk
        output_area.markdown(full_response)