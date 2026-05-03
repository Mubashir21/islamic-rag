# ── Stage 1: builder ──────────────────────────────────────────────────────────
# Install dependencies into a separate layer so they don't need to be
# reinstalled every time we change app code.
FROM python:3.11.15-slim AS builder

WORKDIR /install

COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/packages --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11.15-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install/packages /usr/local

# Copy only what the backend needs at runtime
COPY backend/ ./backend/
COPY artifacts/ ./artifacts/

# HuggingFace Spaces requires port 7860
EXPOSE 7860

# Run the FastAPI app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
