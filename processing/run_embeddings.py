import json
from tqdm import tqdm
from embedder import build_embedding_input, safe_embed_batch
import os

INPUT_FILE = "data/processed/chunks.jsonl"
OUTPUT_FILE = "data/processed/embedded_chunks.jsonl"

BATCH_SIZE = 100


def run_embeddings():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    batch = []
    records = []
    written = 0

    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
        open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in tqdm(f_in, desc="Embedding"):
            record = json.loads(line)

            text = build_embedding_input(record)

            batch.append(text)
            records.append(record)

            if len(batch) == BATCH_SIZE:
                embeddings = safe_embed_batch(batch)

                for rec, emb in zip(records, embeddings):
                    rec["embedding"] = emb
                    f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    written += 1

                    if written % 500 == 0:
                        print(f"[SAVE] {written} embeddings written")

                batch = []
                records = []

        if batch:
            embeddings = safe_embed_batch(batch)

            for rec, emb in zip(records, embeddings):
                rec["embedding"] = emb
                f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")
                written += 1

                if written % 500 == 0:
                    print(f"[SAVE] {written} embeddings written")

if __name__ == "__main__":
    run_embeddings()