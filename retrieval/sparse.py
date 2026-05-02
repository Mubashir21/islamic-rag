from pinecone_text.sparse import BM25Encoder
import json
import os
import pickle
from tqdm import tqdm

ENCODER_PATH = "retrieval/bm25_encoder.pkl"


def fit_sparse_encoder(chunks_file):
    print("[SPARSE] Loading corpus...")

    corpus = []

    with open(chunks_file, "r", encoding="utf-8") as f:
        for line in tqdm(f, desc="Building corpus"):
            record = json.loads(line)
            text = build_sparse_input(record)
            corpus.append(text)

    print(f"[SPARSE] Fitting BM25 on {len(corpus)} documents...")

    encoder = BM25Encoder(stem=False, remove_stopwords=False)
    encoder.fit(corpus)
    encoder.dump(ENCODER_PATH)

    print("[SPARSE] Encoder saved")

    return encoder


def load_sparse_encoder():
    if not os.path.exists(ENCODER_PATH):
        raise Exception("BM25 encoder not found. Run fit_sparse_encoder first.")

    encoder = BM25Encoder(stem=False, remove_stopwords=False)
    encoder.load(ENCODER_PATH)

    return encoder


def build_sparse_input(record):
    return f"{record.get('title','')} {record.get('question','')} {record.get('text','')}"


def encode_sparse(encoder, text, mode="query"):
    if mode == "document":
        return encoder.encode_documents(text)
    elif mode == "query":
        return encoder.encode_queries(text)
    else:
        raise ValueError("mode must be 'document' or 'query'")


if __name__ == "__main__":
    fit_sparse_encoder("data/processed/chunks.jsonl")