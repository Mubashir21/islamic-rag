from pinecone import Pinecone, ServerlessSpec
from backend.app.core.config import settings

pc = Pinecone(api_key=settings.pinecone_api_key)

INDEX_NAME = settings.pinecone_index_name

# Create index if it doesn't exist
if INDEX_NAME  not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME ,
        vector_type="dense",
        dimension=3072,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Index ready")