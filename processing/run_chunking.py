import json
from tqdm import tqdm
from chunker import create_chunk_objects
import os

INPUT_FILE = "data/raw/islamqa.jsonl"
OUTPUT_FILE = "data/processed/chunks.jsonl"


def run_chunking():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f_in, \
         open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:

        for line in tqdm(f_in, desc="Chunking"):
            record = json.loads(line)

            chunks = create_chunk_objects(record)

            for chunk in chunks:
                f_out.write(json.dumps(chunk, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    run_chunking()