from retrieval.hybrid import hybrid_search
from retrieval.reranker import rerank_matches


def retrieve(query, retrieval_k=20, final_k=5, alpha=0.6):
    candidates = hybrid_search(
        query=query,
        top_k=retrieval_k,
        alpha=alpha
    )

    reranked = rerank_matches(
        query=query,
        matches=candidates,
        top_n=final_k
    )

    return reranked