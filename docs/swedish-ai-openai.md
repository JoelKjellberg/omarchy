# Swedish AI OpenAI Integration (Fork)

This fork adds an optional Swedish-first AI stack to Omarchy.

When enabled, installer step `install/config/swedish-ai-openai.sh` will:

- Copy bundled `default/swedish-ai-os` to `~/.local/share/swedish-ai-os`
- Create a Python virtualenv
- Install dependencies with `pip install -e`
- Switch providers to OpenAI for STT/LLM/TTS
- Enable command `omarchy-ai-sv` (from Omarchy `bin/`)

## Enable during install

Set the flag before running Omarchy install:

```bash
export OMARCHY_SWEDISH_AI_OPENAI=true
```

Optional custom install path:

```bash
export OMARCHY_SWEDISH_AI_DIR="$HOME/.local/share/swedish-ai-os"
```

Optional OpenAI key injection at install-time:

```bash
export OMARCHY_OPENAI_API_KEY="sk-..."
```

If no key is provided, set it after install:

```bash
~/.local/share/swedish-ai-os/scripts/set_openai_key.sh
```

## Install from your fork

Use upstream boot script with your fork repo/ref:

```bash
OMARCHY_REPO="<your-github-user>/<your-omarchy-fork>" \
OMARCHY_REF="<your-branch>" \
OMARCHY_SWEDISH_AI_OPENAI=true \
bash -c "$(curl -fsSL https://raw.githubusercontent.com/basecamp/omarchy/master/boot.sh)"
```

## After install

Test quickly:

```bash
omarchy-ai-sv respond "Skriv exakt: Hej fran Omarchy-forken."
```

Full voice pipeline:

```bash
omarchy-ai-sv voice /path/to/swedish-audio.wav --out /tmp/svar.wav
```

## Run as Docker container

The bundled project can also run containerized:

```bash
cd ~/.local/share/swedish-ai-os
docker build -t swedish-ai-os .
docker run --rm --env-file .env swedish-ai-os respond "Skriv exakt: Docker fungerar."
```
