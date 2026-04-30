from processing.embedder import embed_batch
from db.pinecone_client import get_index

index = get_index()

def retrieve_chunks(query, top_k=5):
    query_embedding = embed_batch([query])[0]

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True,
        namespace="islamic-rag-v1"
    )

    return results["matches"]