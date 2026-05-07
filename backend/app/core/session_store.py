import uuid
import asyncio
import logging
from datetime import datetime, timedelta
from backend.app.rag.conversation import Conversation

logger = logging.getLogger(__name__)

SESSION_TTL_MINUTES = 360
CLEANUP_INTERVAL_SECONDS = 300

# In-memory session store: session_id -> {conversation, last_active}
_sessions: dict[str, dict] = {}


def get_or_create_session(session_id: str | None) -> tuple[str, Conversation]:
    if session_id and session_id in _sessions:
        _sessions[session_id]["last_active"] = datetime.now()
        return session_id, _sessions[session_id]["conversation"]

    new_id = str(uuid.uuid4())
    _sessions[new_id] = {
        "conversation": Conversation(),
        "last_active": datetime.now(),
    }
    logger.info(f"New session created: {new_id}")
    return new_id, _sessions[new_id]["conversation"]


async def cleanup_expired_sessions():
    while True:
        await asyncio.sleep(CLEANUP_INTERVAL_SECONDS)
        cutoff = datetime.now() - timedelta(minutes=SESSION_TTL_MINUTES)
        expired = [sid for sid, s in _sessions.items() if s["last_active"] < cutoff]
        for sid in expired:
            del _sessions[sid]
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired session(s)")
