from processing.embedder import embed_batch

def encode_dense(query):
    return embed_batch([query])[0]
