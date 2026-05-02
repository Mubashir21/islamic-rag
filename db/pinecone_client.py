from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

INDEX_NAME = "islamic-rag-hybrid"

def get_index():
    return pc.Index(INDEX_NAME)