from scripts.query import query_ollama_with_context

#Step 3: Query
query = "get feasability difference in waterfall and agile, don't hallucinate?"
answer = query_ollama_with_context(query)
#print("\nAnswer:\n", answer)
