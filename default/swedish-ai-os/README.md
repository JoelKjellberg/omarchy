# Swedish AI OS Starter (Arch/Omarchy-style)

Swedish-first speech and text stack designed for an Arch-based system architecture:

- ASR: local `KBLab/kb-whisper-*` or OpenAI `gpt-4o-mini-transcribe`
- LLM: OpenAI Responses API or local Ollama
- TTS: local Piper Swedish voice (`sv_SE`) or OpenAI `gpt-4o-mini-tts`

This is a runnable implementation, not just planning docs.

## 1) Install system dependencies (Arch)

```bash
cd /path/to/swedish-ai-os
./scripts/install_arch_deps.sh
```

## 2) Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
# For local kb-whisper with transformers/torch:
pip install -e ".[local]"
```

## 3) Configure

```bash
cp .env.example .env
./scripts/download_swedish_models.sh
```

Update `.env` as needed, especially:
- `SVAI_PIPER_MODEL_PATH`
- `OPENAI_API_KEY` (if using OpenAI providers)

OpenAI fast start (ASR + LLM + TTS via OpenAI):
```bash
./scripts/use_openai_stack.sh
```

Set OpenAI key (interactive, avoids shell history):
```bash
./scripts/set_openai_key.sh
```

## 4) Run

Text only:
```bash
sv-ai-os respond "Skriv en kort sammanfattning av dagens uppgifter"
```

Speech to text:
```bash
sv-ai-os transcribe /path/to/swedish-audio.wav
```

Full voice pipeline (ASR -> LLM -> TTS):
```bash
sv-ai-os voice /path/to/swedish-audio.wav --out /tmp/svar.wav
```

OpenAI smoke test:
```bash
./scripts/openai_smoke_test.sh
```

## 5) Run in Docker (OpenAI mode)

Build image:
```bash
docker build -t swedish-ai-os .
```

Text response:
```bash
docker run --rm --env-file .env swedish-ai-os respond "Svara pa svenska: hej"
```

Voice pipeline with mounted audio file:
```bash
docker run --rm --env-file .env -v "$PWD:/work" -w /work swedish-ai-os \
  voice /work/input.wav --out /work/output.wav
```

Compose equivalent:
```bash
docker compose run --rm swedish-ai-os respond "Skriv exakt: Docker fungerar."
```

Makefile shortcuts:
```bash
make env
make build
make run PROMPT="Svara pa svenska: hej"
make voice AUDIO_IN=input.wav AUDIO_OUT=output.wav
make smoke
make test-docker
```

`make test-docker` validates `.env` and performs a live OpenAI container call.

See all targets:
```bash
make help
```

## 6) Optional OS localization

```bash
./scripts/configure_swedish_locale.sh
```

## Why these defaults

The architecture choices are grounded in a dated source snapshot:
- `docs/state-of-swedish-ai-2026-02-09.md`

## Repo layout

- `src/swedish_ai_os/config.py`: env-driven provider/model settings
- `src/swedish_ai_os/asr.py`: Swedish ASR providers
- `src/swedish_ai_os/llm.py`: response generation providers
- `src/swedish_ai_os/tts.py`: speech synthesis providers
- `src/swedish_ai_os/pipeline.py`: CLI entrypoint
- `scripts/`: Arch and model setup scripts
- `docs/`: capability and market snapshot
