from openai import OpenAI
from backend.app.rag.retriever import retrieve
from backend.app.rag.prompt_builder import build_context
import logging
import argparse
import json
from backend.app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_INSTRUCTIONS = """
You are an assistant answering Islamic questions using a retrieval-augmented generation system.

Rules:
- Use ONLY the provided sources.
- Do NOT use outside knowledge.
- Do NOT invent rulings, evidences, scholars, books, or URLs.
- If the provided sources do not clearly answer the question, say exactly:
  "I could not find a clear answer in the provided sources."
- Do not present your own religious opinion. Only summarize what the provided sources say.
- Read ALL provided chunks before answering.
- Do not omit relevant cases, categories, exceptions, or conditions mentioned in the sources.
- If the sources mention different groups (e.g., believer, disbeliever, hypocrite, sinner), explain each relevant group separately.
- If the sources mention different angles or conditions, mention them carefully.
- Answer clearly and concisely, but do not be so brief that important source information is lost.

Citations:
- Each UNIQUE URL corresponds to one Source number (e.g., [Source 1]).
- Multiple chunks from the same URL must use the SAME Source number.
- Only cite a source if you actually used information from it.
- Every inline citation must correspond to a real URL provided in the context.
- Do NOT cite chunk numbers. Only cite Source numbers.

Sources section:
- At the end, include a "### Sources" section.
- List ONLY the sources that were cited in the answer.
- Format each source exactly like this:
  [Source X] <URL>
- Do NOT include any source that was not cited.
- Do NOT duplicate sources.

Answer structure:
- Start with the direct answer.
- Then explain relevant conditions, categories, or exceptions.
- When useful, use short headings such as:
  - General answer
  - For the believer
  - For the disbeliever
  - Conditions
  - Exceptions
""".strip()

def generate_answer(query):
    matches = retrieve(query)

    if not matches or len(matches) == 0:
        return "I could not find a clear answer in the provided sources."

    context = build_context(matches)

    # if len(context) > 12000:
    #     logger.warning(f"Context too large ({len(context)} chars), truncating.")
    #     context = context[:12000]

    try:
        response = client.responses.create(
            model=settings.generation_model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=f"Question: {query}\n\nSources:\n{context}",
        )
        return response.output_text

    except Exception as e:
        return f"An error occurred while generating the answer: {e}"
    
def stream_answer(query: str):
    try:
        matches = retrieve(query)
        context = build_context(matches)
    except Exception as e:
        logger.error(f"Retrieval failed: {e}")
        yield f"data: {json.dumps('Sorry, the search service is temporarily unavailable. This is likely due to a rate limit — please wait a moment and try again.')}\n\n"
        yield "event: done\ndata: [DONE]\n\n"
        return

    try:
        stream = client.responses.create(
            model=settings.generation_model,
            instructions=SYSTEM_INSTRUCTIONS,
            input=f"Question: {query}\n\nSources:\n{context}",
            stream=True,
        )

        for event in stream:
            if event.type == "response.output_text.delta":
                yield f"data: {json.dumps(event.delta)}\n\n"

        yield "event: done\ndata: [DONE]\n\n"

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        yield f"data: {json.dumps('Sorry, the answer could not be generated. This may be due to an API issue — please try again shortly.')}\n\n"
        yield "event: done\ndata: [DONE]\n\n"
    
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