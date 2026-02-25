#!/usr/bin/env bash
set -euo pipefail

BASE_PACKAGES=(
  python
  python-pip
  python-virtualenv
  ffmpeg
  piper
)

echo "Installing base dependencies for Swedish AI stack..."
sudo pacman -S --needed "${BASE_PACKAGES[@]}"

echo
echo "Optional packages for local ASR/LLM acceleration:"
echo "  sudo pacman -S --needed cuda cudnn ollama"
echo
echo "Done. Next: create a virtualenv and install python deps."
