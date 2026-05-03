# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.11.15-slim AS builder

WORKDIR /install

COPY backend/requirements.txt .

RUN pip install --upgrade pip && \
    pip install --prefix=/install/packages --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11.15-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install/packages /usr/local

# Copy only what the backend needs at runtime
COPY --chown=user backend/ ./backend/
COPY --chown=user artifacts/ ./artifacts/

# HuggingFace Spaces requires port 7860
EXPOSE 7860

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
