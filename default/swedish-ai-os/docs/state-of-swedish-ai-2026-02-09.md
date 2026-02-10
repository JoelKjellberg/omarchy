# State of Swedish-Speaking AI (Snapshot: 2026-02-09)

## What is mature right now

- Swedish ASR is production-grade in both cloud and local stacks.
  - OpenAI speech-to-text exposes `gpt-4o-transcribe` and `gpt-4o-mini-transcribe` and lists Swedish among supported languages.
  - KBLab's Swedish-adapted Whisper models report strong WER improvements vs OpenAI Whisper on Swedish benchmarks (example table values for `kb-whisper-large`: FLEURS 5.4, CommonVoice 4.1, NST 5.2).

- Swedish TTS is production-ready in cloud and local options.
  - OpenAI text-to-speech offers `gpt-4o-mini-tts` with multilingual language support including Swedish.
  - Piper publishes Swedish voices (`sv_SE`) that run fully offline.

- Swedish language data availability has improved, but conversational speech remains the bottleneck.
  - Common Voice Swedish is still modest in size (v23 card: 57 total recorded hours, 47 validated).
  - RixVox-v2 provides a much larger Swedish speech base (dataset card: nearly 23,000 hours; 2.72 TB download size).

- Speech-to-speech multilingual research includes Swedish support.
  - Meta SeamlessM4T-v2 lists Swedish (`swe`) in supported languages for speech and text tasks.

## Strategic implication for an Omarchy-like Swedish OS

Inference from the sources above:
- Default to local Swedish ASR (`KBLab/kb-whisper-*`) for privacy and strong Swedish quality.
- Keep an API fallback (`gpt-4o-mini-transcribe`) for noisy real-world microphone conditions.
- Default to local TTS (Piper Swedish voice) for offline mode; keep OpenAI TTS as a higher-naturalness fallback.
- Use a multilingual LLM path (`openai` or local `ollama`) but pin Swedish system prompts and UX copy.
- Treat Swedish data curation as a first-class product feature (user corrections -> retraining/evaluation sets).

## Sources

- OpenAI speech-to-text guide: https://platform.openai.com/docs/guides/speech-to-text
- OpenAI text-to-speech guide: https://platform.openai.com/docs/guides/text-to-speech
- OpenAI supported languages: https://platform.openai.com/docs/guides/text?api-mode=responses#supported-languages
- KBLab kb-whisper-large model card: https://huggingface.co/KBLab/kb-whisper-large
- KBLab kb-whisper-medium model card: https://huggingface.co/KBLab/kb-whisper-medium
- RixVox-v2 dataset card: https://huggingface.co/datasets/KBLab/rixvox-v2
- Common Voice Swedish subset card: https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0/viewer/sv-SE
- Piper voices documentation: https://tderflinger.github.io/piper-docs/about/voices/
- SeamlessM4T-v2 language support: https://huggingface.co/facebook/seamless-m4t-v2-large
- AI Sweden GPT-SW3 announcement: https://www.ai.se/en/news/ai-sweden-first-deliver-national-large-language-model
