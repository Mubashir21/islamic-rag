from openai import OpenAI
import json
from tqdm import tqdm
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

def build_embedding_input(chunk):
    return f"""
        Title: {chunk['title']}

        Question: {chunk['question']}

        Content:
        {chunk['text']}
        """.strip()


def embed_batch(texts, model="text-embedding-3-large"):
    response = client.embeddings.create(
        input=texts,
        model=model
    )
    return [d.embedding for d in response.data]


def run_embedding_pipeline(input_file, output_file, batch_size=100):
    batch = []
    records = []

    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in tqdm(lines, desc="Embedding"):
        record = json.loads(line)

        embedding_input = build_embedding_input(record)

        batch.append(embedding_input)
        records.append(record)

        if len(batch) == batch_size:
            embeddings = embed_batch(batch)

            with open(output_file, "a", encoding="utf-8") as out:
                for rec, emb in zip(records, embeddings):
                    rec["embedding"] = emb
                    out.write(json.dumps(rec, ensure_ascii=False) + "\n")

            batch = []
            records = []

    # flush remaining
    if batch:
        embeddings = embed_batch(batch)

        for rec, emb in zip(records, embeddings):
            rec["embedding"] = emb

            with open(output_file, "a", encoding="utf-8") as out:
                out.write(json.dumps(rec, ensure_ascii=False) + "\n")

def safe_embed_batch(batch, retries=3):
    for attempt in range(retries):
        try:
            return embed_batch(batch)
        except Exception as e:
            print(f"[RETRY {attempt+1}] Embedding failed: {e}")
    raise Exception("Embedding failed after retries")