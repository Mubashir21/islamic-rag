from pinecone import Pinecone
from backend.app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

INDEX_NAME = settings.pinecone_index_name

def get_index():
    return pc.Index(INDEX_NAME)