#!/usr/bin/env bash
set -euo pipefail

TARGET_DIR=${1:-"$HOME/.local/share/piper-voices"}
MODEL_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx"
CONFIG_URL="https://huggingface.co/rhasspy/piper-voices/resolve/main/sv/sv_SE/nst/medium/sv_SE-nst-medium.onnx.json"

mkdir -p "$TARGET_DIR"

curl -fL "$MODEL_URL" -o "$TARGET_DIR/sv_SE-nst-medium.onnx"
curl -fL "$CONFIG_URL" -o "$TARGET_DIR/sv_SE-nst-medium.onnx.json"

echo "Downloaded Swedish Piper model to: $TARGET_DIR"
echo "Set in .env: SVAI_PIPER_MODEL_PATH=$TARGET_DIR/sv_SE-nst-medium.onnx"
