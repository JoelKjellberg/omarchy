from __future__ import annotations

from pathlib import Path

from swedish_ai_os.config import Settings


class SpeechToText:
    def transcribe(self, audio_path: str | Path) -> str:
        raise NotImplementedError


class KBWhisperSTT(SpeechToText):
    def __init__(self, model_id: str, revision: str = "main") -> None:
        self.model_id = model_id
        self.revision = revision
        self._pipe = None

    def _build_pipeline(self):
        try:
            import torch
            from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
        except ImportError as exc:
            raise RuntimeError(
                "KBWhisperSTT requires local dependencies. Install with: pip install '.[local]'"
            ) from exc

        has_cuda = torch.cuda.is_available()
        torch_dtype = torch.float16 if has_cuda else torch.float32

        try:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                use_safetensors=True,
                revision=self.revision,
            )
        except Exception:
            model = AutoModelForSpeechSeq2Seq.from_pretrained(
                self.model_id,
                torch_dtype=torch_dtype,
                low_cpu_mem_usage=True,
                revision=self.revision,
            )
        if has_cuda:
            model.to("cuda")

        processor = AutoProcessor.from_pretrained(self.model_id, revision=self.revision)

        device = 0 if has_cuda else -1
        return pipeline(
            "automatic-speech-recognition",
            model=model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            torch_dtype=torch_dtype,
            device=device,
        )

    def transcribe(self, audio_path: str | Path) -> str:
        if self._pipe is None:
            self._pipe = self._build_pipeline()

        result = self._pipe(
            str(audio_path),
            chunk_length_s=30,
            return_timestamps=False,
            generate_kwargs={"task": "transcribe", "language": "sv"},
        )
        text = result.get("text", "") if isinstance(result, dict) else str(result)
        return " ".join(text.split())


class OpenAISTT(SpeechToText):
    def __init__(self, model: str = "gpt-4o-mini-transcribe") -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package not installed") from exc

        self._client = OpenAI()
        self.model = model

    def transcribe(self, audio_path: str | Path) -> str:
        with Path(audio_path).expanduser().open("rb") as handle:
            transcript = self._client.audio.transcriptions.create(
                model=self.model,
                file=handle,
                language="sv",
            )
        return " ".join(transcript.text.split())


def build_stt(settings: Settings) -> SpeechToText:
    if settings.asr_provider == "kb_whisper":
        return KBWhisperSTT(
            model_id=settings.kb_whisper_model,
            revision=settings.kb_whisper_revision,
        )
    if settings.asr_provider == "openai":
        return OpenAISTT(model=settings.openai_stt_model)

    raise ValueError(f"Unsupported ASR provider: {settings.asr_provider}")
