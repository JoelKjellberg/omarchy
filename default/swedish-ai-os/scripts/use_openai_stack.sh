#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)

cp "$PROJECT_DIR/.env.openai.example" "$PROJECT_DIR/.env"

echo "OpenAI preset activated in: $PROJECT_DIR/.env"
echo "Next: set OPENAI_API_KEY in .env"
echo "Then run: sv-ai-os respond \"Hej\""
