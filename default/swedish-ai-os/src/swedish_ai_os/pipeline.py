from __future__ import annotations

import argparse
import sys
from pathlib import Path

from swedish_ai_os.asr import build_stt
from swedish_ai_os.config import load_settings
from swedish_ai_os.llm import build_llm
from swedish_ai_os.tts import build_tts


def _existing_file(path: str) -> Path:
    file_path = Path(path).expanduser()
    if not file_path.exists():
        raise argparse.ArgumentTypeError(f"File not found: {file_path}")
    return file_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sv-ai-os",
        description="Swedish-first speech/text assistant pipeline.",
    )
    parser.add_argument(
        "--env-file",
        default=".env",
        help="Environment file with provider/model settings (default: .env)",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    transcribe = subparsers.add_parser("transcribe", help="Transcribe Swedish speech from audio file")
    transcribe.add_argument("audio", type=_existing_file, help="Path to audio file")

    respond = subparsers.add_parser("respond", help="Generate Swedish assistant text")
    respond.add_argument("prompt", help="User prompt")
    respond.add_argument("--system", help="Override Swedish system prompt")

    voice = subparsers.add_parser("voice", help="Run full speech pipeline: ASR -> LLM -> TTS")
    voice.add_argument("audio", type=_existing_file, help="Path to user audio file")
    voice.add_argument("--out", default="assistant-response.wav", help="Output WAV path")
    voice.add_argument("--system", help="Override Swedish system prompt")

    return parser


def _run_transcribe(settings, audio: Path) -> int:
    stt = build_stt(settings)
    text = stt.transcribe(audio)
    print(text)
    return 0


def _run_respond(settings, prompt: str, system_override: str | None) -> int:
    llm = build_llm(settings)
    system_prompt = system_override or settings.system_prompt
    response_text = llm.generate(prompt, system_prompt)
    print(response_text)
    return 0


def _run_voice(settings, audio: Path, output_wav: str, system_override: str | None) -> int:
    stt = build_stt(settings)
    llm = build_llm(settings)
    tts = build_tts(settings)

    system_prompt = system_override or settings.system_prompt

    transcript = stt.transcribe(audio)
    response_text = llm.generate(transcript, system_prompt)
    output_path = tts.synthesize(response_text, output_wav)

    print(f"TRANSCRIPT: {transcript}")
    print(f"RESPONSE: {response_text}")
    print(f"AUDIO_FILE: {output_path}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        settings = load_settings(args.env_file)

        if args.command == "transcribe":
            return _run_transcribe(settings, args.audio)

        if args.command == "respond":
            return _run_respond(settings, args.prompt, args.system)

        if args.command == "voice":
            return _run_voice(settings, args.audio, args.out, args.system)

        parser.error(f"Unknown command: {args.command}")
        return 2

    except Exception as exc:  # pragma: no cover
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
