from fastapi import APIRouter, HTTPException
from backend.app.schemas.query import QueryRequest, QueryResponse
from backend.app.rag.generator import generate_answer
from fastapi.responses import StreamingResponse
from backend.app.rag.generator import stream_answer

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
    return StreamingResponse(
        stream_answer(request.query),
        media_type="text/event-stream"
    )