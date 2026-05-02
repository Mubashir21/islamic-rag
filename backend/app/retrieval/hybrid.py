from backend.app.db.pinecone_client import get_index
from backend.app.retrieval.dense import encode_dense
from backend.app.retrieval.sparse import load_sparse_encoder, encode_sparse

from backend.app.core.config import settings

index = get_index()
encoder = load_sparse_encoder()

def hybrid_score_norm(dense, sparse, alpha=0.8):
    if alpha < 0 or alpha > 1:
        raise ValueError("Alpha must be between 0 and 1")
    hs = {
        'indices': sparse['indices'],
        'values':  [v * (1 - alpha) for v in sparse['values']]
    }
    return [v * alpha for v in dense], hs


def hybrid_search(query, top_k=40, alpha=0.8):
    dense_vector = encode_dense(query)
    sparse_vector = encode_sparse(encoder, query, mode="query")

    hdense, hsparse = hybrid_score_norm(dense_vector, sparse_vector, alpha)

    results = index.query(
        vector=hdense,
        sparse_vector=hsparse,
        top_k=top_k,
        include_metadata=True,
        namespace=settings.pinecone_namespace
    )
  
    return results["matches"]