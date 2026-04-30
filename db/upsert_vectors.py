import json
from tqdm import tqdm
from pinecone_client import get_index

index = get_index()

def run_upsert(file_path, batch_size=100):
    batch = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Uploading to Pinecone"):
            record = json.loads(line)

            vector = {
                "id": record["id"],
                "values": record["embedding"],
                "metadata": {
                    "doc_id": str(record["doc_id"]),
                    "chunk_index": record.get("chunk_index", 0),
                    "text": record.get("text") or "",
                    "title": record.get("title") or "",
                    "question": record.get("question") or "",
                    "topics": record.get("topics") or [],
                    "url": record.get("url") or "",
                    "source": record.get("source") or "IslamQA"
                }
            }

            batch.append(vector)

            if len(batch) == batch_size:
                index.upsert(vectors=batch, namespace="islamic-rag-v1")
                batch = []

        # flush remaining
        if batch:
            index.upsert(vectors=batch, namespace="islamic-rag-v1")

    print("Upload complete")

if __name__ == "__main__":
    run_upsert("data/processed/embedded_chunks.jsonl")