from db.query import retrieve_chunks

def get_relevant_chunks(query, top_k=5):
    return retrieve_chunks(query, top_k)