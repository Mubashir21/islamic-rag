from openai import OpenAI
from rag.retriever import get_relevant_chunks
from rag.prompt_builder import build_context
from dotenv import load_dotenv
import logging
import argparse

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI()

SYSTEM_INSTRUCTIONS = """
You are an assistant answering Islamic questions using a retrieval-augmented generation system.

Rules:
- Use ONLY the provided sources.
- Do NOT use outside knowledge.
- Do NOT invent rulings, evidences, scholars, books, or URLs.
- If the provided sources do not clearly answer the question, say exactly:
  "I could not find a clear answer in the provided sources."
- Answer clearly and concisely.
- When you make a claim, support it using the provided source material.
- Always cite the source URL when available.
- At the end, include a "Sources" section listing the URLs you used.
- If multiple sources disagree or discuss different angles, mention that carefully.
- Do not present your own religious opinion. Only summarize what the provided sources say.

When answering:
- Give the direct ruling first.
- Then explain the condition clearly.
- Cite sources inline using [Source 1], [Source 2], etc.
- End with a Sources section containing the URLs.
- Only cite sources that you include in the final Sources section.
- If multiple sources have the same URL, cite only the first source number for that URL.
- Do not quote source text unless necessary.
"""

def generate_answer(query, top_k=5):
    matches = get_relevant_chunks(query, top_k=top_k)

    context = build_context(matches)

    # if len(context) > 12000:
    #     logger.warning(f"Context too large ({len(context)} chars), truncating.")
    #     context = context[:12000]

    try:
        response = client.responses.create(
            model="gpt-5.5",
            instructions=SYSTEM_INSTRUCTIONS,
            input=f"Question: {query}\n\nSources:\n{context}",
            # temperature=0.2,
        )
        return response.output_text

    except Exception as e:
        return f"An error occurred while generating the answer: {e}"
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask a question to the Islamic RAG system.")

    parser.add_argument(
        "query",
        type=str,
        help="The question you want to ask."
    )

    args = parser.parse_args()

    answer = generate_answer(args.query)
    print("\nAnswer:\n", answer)