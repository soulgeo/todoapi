FROM python:3.14.3-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock ./
ENV UV_PROJECT_ENVIRONMENT="/opt/venv"
RUN uv sync --frozen --no-install-project

COPY src/ .

ENV PATH="/opt/venv/bin:$PATH"

EXPOSE 8000

CMD ["./entrypoint.sh"]
