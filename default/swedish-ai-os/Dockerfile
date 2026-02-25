FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml requirements.txt README.md ./
COPY src ./src
COPY scripts ./scripts
COPY docs ./docs
COPY .env.example ./.env.example
COPY .env.openai.example ./.env.openai.example

RUN pip install --upgrade pip && pip install .

ENTRYPOINT ["sv-ai-os"]
CMD ["--help"]
