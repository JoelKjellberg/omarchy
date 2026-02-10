#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
ENV_FILE="$PROJECT_DIR/.env"

if [ ! -x "$PROJECT_DIR/.venv/bin/sv-ai-os" ]; then
  echo "Missing .venv or sv-ai-os binary. Run: ./.venv/bin/pip install -e ." >&2
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  echo "Missing $ENV_FILE. Run: ./scripts/use_openai_stack.sh" >&2
  exit 1
fi

if ! grep -q '^OPENAI_API_KEY=[^[:space:]]\+$' "$ENV_FILE"; then
  echo "OPENAI_API_KEY missing in .env. Run: ./scripts/set_openai_key.sh" >&2
  exit 1
fi

cd "$PROJECT_DIR"

echo "Running OpenAI text smoke test..."
"$PROJECT_DIR/.venv/bin/sv-ai-os" --env-file "$ENV_FILE" respond "Skriv exakt: OpenAI pipeline fungerar."
