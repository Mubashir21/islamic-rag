import os
from urllib import response
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))

RERANK_MODEL = "rerank-v4.0-pro"


def build_rerank_document(match):
    meta = match["metadata"]

    return f"""
Title: {meta.get("title", "")}

Question: {meta.get("question", "")}

Content:
{meta.get("text", "")}
""".strip()


def rerank_matches(query, matches, top_n=5):
    if not matches:
        return []

    documents = [build_rerank_document(match) for match in matches]

    response = co.rerank(
        model=RERANK_MODEL,
        query=query,
        documents=documents,
        top_n=top_n,
    )

    reranked = []

    for result in response.results:
        original_match = matches[result.index]

        original_match["rerank_score"] = result.relevance_score
        original_match["pinecone_score"] = original_match.get("score", 0)

        reranked.append(original_match)
    return reranked