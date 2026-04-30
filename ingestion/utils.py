import json

def load_existing_ids(file_path):
    ids = set()
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                ids.add(data["id"])
    except FileNotFoundError:
        pass

    return ids

def extract_id(url):
    return url.rstrip("/").split("/")[-1]