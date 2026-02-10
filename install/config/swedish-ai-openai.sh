# Install and configure Swedish AI OS starter on top of Omarchy.
# Enabled only when OMARCHY_SWEDISH_AI_OPENAI=true.

if [[ ${OMARCHY_SWEDISH_AI_OPENAI:-false} != "true" ]]; then
  echo "Skipping Swedish AI OpenAI setup (set OMARCHY_SWEDISH_AI_OPENAI=true to enable)."
  return 0
fi

SWEDISH_AI_SOURCE_PATH="$OMARCHY_PATH/default/swedish-ai-os"
SWEDISH_AI_PATH="${OMARCHY_SWEDISH_AI_DIR:-$HOME/.local/share/swedish-ai-os}"

if [[ ! -d $SWEDISH_AI_SOURCE_PATH ]]; then
  echo "Swedish AI source bundle missing: $SWEDISH_AI_SOURCE_PATH" >&2
  exit 1
fi

# Ensure runtime dependencies exist for the Python pipeline.
omarchy-pkg-add python python-pip ffmpeg

mkdir -p "$SWEDISH_AI_PATH"

# Copy bundled starter project into user-local path.
tar -C "$SWEDISH_AI_SOURCE_PATH" -cf - . | tar -C "$SWEDISH_AI_PATH" -xf -
chmod +x "$SWEDISH_AI_PATH"/scripts/*.sh

python -m venv "$SWEDISH_AI_PATH/.venv"
"$SWEDISH_AI_PATH/.venv/bin/pip" install -e "$SWEDISH_AI_PATH"

# Set OpenAI providers as defaults for ASR/LLM/TTS.
"$SWEDISH_AI_PATH/scripts/use_openai_stack.sh"

if [[ -n ${OMARCHY_OPENAI_API_KEY:-} ]]; then
  escaped_key=$(printf '%s' "$OMARCHY_OPENAI_API_KEY" | sed -e 's/[\\/&]/\\&/g')
  sed -i "s/^OPENAI_API_KEY=.*/OPENAI_API_KEY=$escaped_key/" "$SWEDISH_AI_PATH/.env"
  chmod 600 "$SWEDISH_AI_PATH/.env"
  echo "Configured OPENAI_API_KEY from OMARCHY_OPENAI_API_KEY."
else
  echo "OPENAI_API_KEY not set during install. Run $SWEDISH_AI_PATH/scripts/set_openai_key.sh after first boot."
fi

echo "Swedish AI stack installed at: $SWEDISH_AI_PATH"
echo "Command available: omarchy-ai-sv respond \"Hej\""
