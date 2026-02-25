#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
ENV_FILE="$PROJECT_DIR/.env"

if [ ! -f "$ENV_FILE" ]; then
  cp "$PROJECT_DIR/.env.openai.example" "$ENV_FILE"
fi

KEY=""
if [ "${1:-}" != "" ]; then
  KEY="$1"
elif [ -n "${OPENAI_API_KEY:-}" ]; then
  KEY="$OPENAI_API_KEY"
elif command -v llm >/dev/null 2>&1 && llm keys get openai >/dev/null 2>&1; then
  KEY="$(llm keys get openai)"
elif [ -t 0 ]; then
  read -rsp "Enter OPENAI_API_KEY: " KEY
  echo
else
  echo "No OPENAI_API_KEY available. Pass it as arg, env var, or run interactively." >&2
  exit 1
fi

if [ -z "$KEY" ]; then
  echo "OPENAI_API_KEY is empty." >&2
  exit 1
fi

escaped_key=$(printf '%s' "$KEY" | sed -e 's/[\\/&]/\\&/g')

if grep -q '^OPENAI_API_KEY=' "$ENV_FILE"; then
  sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$escaped_key/" "$ENV_FILE"
else
  printf '\nOPENAI_API_KEY=%s\n' "$KEY" >> "$ENV_FILE"
fi

echo "OPENAI_API_KEY set in $ENV_FILE"
