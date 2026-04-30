from processing.embedder import embed_batch
from pinecone_client import get_index

index = get_index()

def query_pinecone(query, top_k=5):
    # 1. embed query
    query_embedding = embed_batch([query])[0]

    # 2. search
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace="islamic-rag-v1"
    )

    return results