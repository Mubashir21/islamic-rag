from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME  = "islamic-rag"

# Create index if it doesn't exist
if INDEX_NAME  not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME ,
        dimension=3072,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
        )
    )

print("Index ready")