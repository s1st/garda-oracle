# Garda dashboard: FastAPI + Jinja2, pure-Python scoring.
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_COMPILE_BYTECODE=1 \
    PORT=8080

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.11.12 /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md LICENSE ./
COPY src ./src
RUN uv sync --frozen --no-editable

RUN useradd --system --uid 1001 --create-home oracle
USER oracle

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080
CMD ["sh", "-c", "uvicorn garda.web:app --host 0.0.0.0 --port ${PORT}"]
