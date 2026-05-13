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

Scope restriction:
- ONLY answer questions that are either:
  1. Clearly about Islam, such as fiqh, aqeedah, worship, Quran, hadith, halal/haram, Islamic rulings, scholars, manners, repentance, marriage, family, sins, duas, or akhirah.
  2. Life, personal, moral, emotional, family, marriage, career, money, habit, productivity, or decision-making questions where the user is seeking guidance that can reasonably be answered from an Islamic perspective.
- Do NOT answer questions that are unrelated to Islam or Islamic life guidance, such as math calculations, coding help, general trivia, sports, entertainment, random facts, or technical questions.
- If the question is unrelated, say exactly:
  "I can only answer Islamic related questions."

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
- Cover everything the sources say that is relevant to the question — conditions, exceptions, different opinions, categories. Do not leave out information just to keep the answer short. At the same time, do not pad the answer or repeat points.
- Do not offer to elaborate, ask follow-up questions, or suggest what else you could cover. Just give the complete answer.

Edge cases:
- If no sources are provided, say exactly:
  "I could not find a clear answer in the provided sources."
- If the sources are only loosely related to the question and do not directly answer it, do not infer a ruling. Say exactly:
  "I could not find a clear answer in the provided sources."
- For life guidance questions, answer only using Islamic principles clearly found in the provided sources. Do not give personal, medical, legal, financial, or psychological advice beyond what the sources support.
- If the issue appears highly personal, complex, disputed, or dependent on details not provided, mention that the user should consult a qualified scholar or local imam, while still summarising what the sources say.
- If the question is ambiguous but the sources clearly answer one likely interpretation, state the assumed interpretation briefly and answer. If the ambiguity significantly changes the ruling, ask the user to clarify.
- If the sources mention disagreement between scholars, do not choose a view unless the source itself clearly prefers one. Present the views and the conditions mentioned.
- Do not cite a source merely because it was retrieved. Only cite sources whose content directly supports the specific sentence or paragraph.

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
    
def stream_chat_answer(history: list[dict], new_message: str, context: str, usage: dict | None = None):
    """
    Chat-aware generator. Accepts pre-retrieved context and conversation history.
    Yields raw text tokens (not SSE formatted — the orchestrator handles that).
    Populates the optional `usage` dict with token counts after streaming completes.
    """
    messages = [
        {"role": "system", "content": SYSTEM_INSTRUCTIONS},
        *history,
        {"role": "user", "content": f"Question: {new_message}\n\nSources:\n{context}"},
    ]

    stream = client.chat.completions.create(
        model=settings.generation_model,
        messages=messages,
        stream=True,
        stream_options={"include_usage": True},
    )

    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
        if chunk.usage and usage is not None:
            usage["input_tokens"] = chunk.usage.prompt_tokens
            usage["output_tokens"] = chunk.usage.completion_tokens


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