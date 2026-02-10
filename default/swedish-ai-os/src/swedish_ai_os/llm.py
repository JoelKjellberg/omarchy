from __future__ import annotations

import requests

from swedish_ai_os.config import Settings


class LanguageModel:
    def generate(self, user_text: str, system_prompt: str) -> str:
        raise NotImplementedError


class OpenAILLM(LanguageModel):
    def __init__(self, model: str = "gpt-4.1-mini") -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("openai package not installed") from exc

        self._client = OpenAI()
        self.model = model

    def generate(self, user_text: str, system_prompt: str) -> str:
        response = self._client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
        )

        text = getattr(response, "output_text", None)
        if text:
            return text.strip()

        raise RuntimeError("OpenAI response did not include output_text")


class OllamaLLM(LanguageModel):
    def __init__(self, model: str, host: str = "http://127.0.0.1:11434") -> None:
        self.model = model
        self.host = host.rstrip("/")

    def generate(self, user_text: str, system_prompt: str) -> str:
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text},
            ],
        }

        response = requests.post(
            f"{self.host}/api/chat",
            json=payload,
            timeout=180,
        )
        response.raise_for_status()

        data = response.json()
        message = data.get("message", {}).get("content", "")
        if not message:
            raise RuntimeError("Ollama response missing message.content")
        return message.strip()


def build_llm(settings: Settings) -> LanguageModel:
    if settings.llm_provider == "openai":
        return OpenAILLM(model=settings.llm_model)
    if settings.llm_provider == "ollama":
        return OllamaLLM(model=settings.ollama_model, host=settings.ollama_host)

    raise ValueError(f"Unsupported LLM provider: {settings.llm_provider}")
