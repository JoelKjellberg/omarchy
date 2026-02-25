from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*_args, **_kwargs):
        return False


@dataclass(frozen=True)
class Settings:
    asr_provider: str
    kb_whisper_model: str
    kb_whisper_revision: str
    openai_stt_model: str

    llm_provider: str
    llm_model: str
    ollama_model: str
    ollama_host: str

    tts_provider: str
    piper_model_path: str
    openai_tts_model: str
    openai_tts_voice: str

    system_prompt: str


_ALLOWED = {
    "asr_provider": {"kb_whisper", "openai"},
    "llm_provider": {"openai", "ollama"},
    "tts_provider": {"piper", "openai"},
}


def _env(name: str, default: str) -> str:
    value = os.getenv(name, default).strip()
    return value if value else default


def _validate(name: str, value: str) -> str:
    allowed = _ALLOWED.get(name)
    if allowed is None:
        return value
    if value not in allowed:
        valid = ", ".join(sorted(allowed))
        raise ValueError(f"Invalid {name}={value!r}. Allowed values: {valid}")
    return value


def load_settings(env_file: str | None = ".env") -> Settings:
    if env_file:
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path, override=False)

    return Settings(
        asr_provider=_validate("asr_provider", _env("SVAI_ASR_PROVIDER", "kb_whisper")),
        kb_whisper_model=_env("SVAI_KB_WHISPER_MODEL", "KBLab/kb-whisper-medium"),
        kb_whisper_revision=_env("SVAI_KB_WHISPER_REVISION", "main"),
        openai_stt_model=_env("SVAI_OPENAI_STT_MODEL", "gpt-4o-mini-transcribe"),
        llm_provider=_validate("llm_provider", _env("SVAI_LLM_PROVIDER", "openai")),
        llm_model=_env("SVAI_LLM_MODEL", "gpt-4.1-mini"),
        ollama_model=_env("SVAI_OLLAMA_MODEL", "llama3.1"),
        ollama_host=_env("SVAI_OLLAMA_HOST", "http://127.0.0.1:11434"),
        tts_provider=_validate("tts_provider", _env("SVAI_TTS_PROVIDER", "piper")),
        piper_model_path=_env("SVAI_PIPER_MODEL_PATH", "/opt/piper/voices/sv_SE-nst-medium.onnx"),
        openai_tts_model=_env("SVAI_OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        openai_tts_voice=_env("SVAI_OPENAI_TTS_VOICE", "alloy"),
        system_prompt=_env(
            "SVAI_SYSTEM_PROMPT",
            "Du ar en svensk rostassistent i ett Arch-baserat system. Svara kort, tydligt och pa svenska.",
        ),
    )
