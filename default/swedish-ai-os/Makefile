IMAGE ?= swedish-ai-os
ENV_FILE ?= .env
WORKDIR ?= /work
PROMPT ?= Svara pa svenska: hej
AUDIO_IN ?= input.wav
AUDIO_OUT ?= output.wav

.PHONY: help env check-env check-audio build run respond transcribe voice smoke compose-run compose-voice

help:
	@echo "Targets:"
	@echo "  make env            # Create .env from .env.openai.example if missing"
	@echo "  make build          # Build docker image"
	@echo "  make run            # Run text response (set PROMPT='...')"
	@echo "  make transcribe     # Transcribe AUDIO_IN to stdout"
	@echo "  make voice          # ASR -> LLM -> TTS to AUDIO_OUT"
	@echo "  make smoke          # Quick OpenAI smoke prompt"
	@echo "  make compose-run    # docker compose text response"
	@echo "  make compose-voice  # docker compose full voice pipeline"
	@echo "Variables: IMAGE ENV_FILE PROMPT AUDIO_IN AUDIO_OUT"

env:
	@if [[ ! -f $(ENV_FILE) ]]; then \
		cp .env.openai.example $(ENV_FILE); \
		echo "Created $(ENV_FILE) from .env.openai.example"; \
		echo "Set OPENAI_API_KEY in $(ENV_FILE) before running OpenAI calls."; \
	else \
		echo "Using existing $(ENV_FILE)"; \
	fi

check-env:
	@if [[ ! -f $(ENV_FILE) ]]; then \
		echo "Missing $(ENV_FILE). Run: make env" >&2; \
		exit 1; \
	fi

check-audio:
	@if [[ ! -f $(AUDIO_IN) ]]; then \
		echo "Missing input audio file: $(AUDIO_IN)" >&2; \
		exit 1; \
	fi

build:
	docker build -t $(IMAGE) .

run: check-env
	docker run --rm --env-file $(ENV_FILE) $(IMAGE) respond "$(PROMPT)"

respond: run

transcribe: check-env check-audio
	docker run --rm --env-file $(ENV_FILE) -v "$(CURDIR):$(WORKDIR)" -w $(WORKDIR) $(IMAGE) \
		transcribe "$(WORKDIR)/$(AUDIO_IN)"

voice: check-env check-audio
	docker run --rm --env-file $(ENV_FILE) -v "$(CURDIR):$(WORKDIR)" -w $(WORKDIR) $(IMAGE) \
		voice "$(WORKDIR)/$(AUDIO_IN)" --out "$(WORKDIR)/$(AUDIO_OUT)"

smoke: check-env
	docker run --rm --env-file $(ENV_FILE) $(IMAGE) respond "Skriv exakt: Docker fungerar."

compose-run: check-env
	docker compose run --rm swedish-ai-os respond "$(PROMPT)"

compose-voice: check-env check-audio
	docker compose run --rm swedish-ai-os \
		voice "$(WORKDIR)/$(AUDIO_IN)" --out "$(WORKDIR)/$(AUDIO_OUT)"
