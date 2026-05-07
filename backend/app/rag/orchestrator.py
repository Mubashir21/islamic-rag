import json
import logging
from backend.app.rag.conversation import Conversation
from backend.app.rag.router import route_message
from backend.app.rag.retriever import retrieve
from backend.app.rag.prompt_builder import build_context
from backend.app.rag.generator import stream_chat_answer

logger = logging.getLogger(__name__)


# ── SSE helpers ───────────────────────────────────────────────────────────────

def status_event(message: str) -> str:
    return f"event: status\ndata: {json.dumps({'message': message})}\n\n"

def token_event(text: str) -> str:
    return f"event: token\ndata: {json.dumps({'text': text})}\n\n"

def done_event() -> str:
    return "event: done\ndata: {}\n\n"


# ── Orchestrator ──────────────────────────────────────────────────────────────

def stream_chat(conversation: Conversation, new_message: str):
    """
    Main entry point for the agentic chat flow.
    Yields SSE-formatted strings: status events, token events, then done.
    Updates conversation state as it goes.
    """

    # Step 1: route the message
    yield status_event("Understanding your question...")
    route_result = route_message(conversation.get_history(), new_message)
    route = route_result.get("route", "retrieval_needed")
    logger.info(f"Route: {route}")

    # Step 2: handle out of scope immediately
    if route == "out_of_scope":
        reply = "I can only answer questions related to Islam."
        yield token_event(reply)
        yield done_event()
        conversation.add_message("user", new_message)
        conversation.add_message("assistant", reply)
        return

    # Step 3: get chunks — either fresh retrieval or cached from last turn
    if route == "retrieval_needed":
        yield status_event("Searching Islamic sources...")
        query = route_result.get("rewritten_query") or new_message
        try:
            chunks = retrieve(query)
            conversation.update_chunks(chunks)
        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            reply = "Sorry, the search service is temporarily unavailable. Please try again shortly."
            yield token_event(reply)
            yield done_event()
            return
        yield status_event("Reviewing sources...")
    else:
        # conversation_only — reuse chunks from the previous retrieval
        yield status_event("Checking previous conversation...")
        chunks = conversation.last_chunks

    # Step 4: build context and stream the answer
    context = build_context(chunks)
    full_answer = ""

    try:
        for token in stream_chat_answer(conversation.get_history(), new_message, context):
            full_answer += token
            yield token_event(token)
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        reply = "Sorry, the answer could not be generated. Please try again shortly."
        yield token_event(reply)
        yield done_event()
        return

    yield done_event()

    # Step 5: update conversation history after a successful response
    conversation.add_message("user", new_message)
    conversation.add_message("assistant", full_answer)
