from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.app.schemas.query import QueryRequest, QueryResponse, ChatRequest
from backend.app.rag.generator import generate_answer, stream_answer
from backend.app.rag.orchestrator import stream_chat
from backend.app.core.session_store import get_or_create_session
import json

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    try:
        result = generate_answer(request.query)

        return QueryResponse(
            answer=result
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate answer: {str(e)}"
        )
    

@router.post("/query/stream")
def query_stream(request: QueryRequest):
    try:
        return StreamingResponse(
            stream_answer(request.query),
            media_type="text/event-stream"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate streaming answer: {str(e)}"
        )


@router.post("/chat/stream")
def chat_stream(request: ChatRequest):
    session_id, conversation = get_or_create_session(request.session_id)

    def event_stream():
        # First event sends the session_id back to the client so it can reuse it
        yield f"event: session\ndata: {json.dumps({'session_id': session_id})}\n\n"
        yield from stream_chat(conversation, request.message, session_id)

    return StreamingResponse(event_stream(), media_type="text/event-stream")