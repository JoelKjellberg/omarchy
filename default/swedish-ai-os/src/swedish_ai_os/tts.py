from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from swedish_ai_os.config import Settings


class TextToSpeech:
    def synthesize(self, text: str, output_wav: str | Path) -> Path:
        raise NotImplementedError


class PiperTTS(TextToSpeech):
    def __init__(self, model_path: str) -> None:
        self.model_path = Path(model_path).expanduser()

    def synthesize(self, text: str, output_wav: str | Path) -> Path:
        if shutil.which("piper") is None:
            raise RuntimeError("piper binary not found in PATH")

        if not self.model_path.exists():
            raise RuntimeError(f"Piper model not found: {self.model_path}")

        target = Path(output_wav).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)

        subprocess.run(
            ["piper", "--model", str(self.model_path), "--output_file", str(target)],
            input=text.encode("utf-8"),
            check=True,
            capture_output=True,
        )
        return target


class OpenAITTS(TextToSpeech):
    def __init__(self, model: str = "gpt-4o-mini-tts", voice: str = "alloy") -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package not installed") from exc

        self._client = OpenAI()
        self.model = model
        self.voice = voice

    def synthesize(self, text: str, output_wav: str | Path) -> Path:
        target = Path(output_wav).expanduser()
        target.parent.mkdir(parents=True, exist_ok=True)

        audio = self._client.audio.speech.create(
            model=self.model,
            voice=self.voice,
            input=text,
            response_format="wav",
        )
        audio.write_to_file(str(target))
        return target


def build_tts(settings: Settings) -> TextToSpeech:
    if settings.tts_provider == "piper":
        return PiperTTS(model_path=settings.piper_model_path)
    if settings.tts_provider == "openai":
        return OpenAITTS(model=settings.openai_tts_model, voice=settings.openai_tts_voice)

    raise ValueError(f"Unsupported TTS provider: {settings.tts_provider}")
