from backend.app.retrieval.hybrid import hybrid_search
from backend.app.retrieval.reranker import rerank_matches
from backend.app.core.config import settings


def retrieve(query):
    candidates = hybrid_search(
        query=query,
        top_k=settings.retrieval_k,
        alpha=settings.hybrid_alpha
    )

    reranked = rerank_matches(
        query=query,
        matches=candidates,
        top_n=settings.final_k
    )

    return reranked