from openai import OpenAI
from backend.app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def encode_dense(query: str) -> list[float]:
    response = client.embeddings.create(
        input=[query],
        model=settings.embedding_model,
    )
    return response.data[0].embedding
