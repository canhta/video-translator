import logging
from pathlib import Path
from .audio_processor import extract_audio, transcribe_audio
from .text_processor import split_text, translate_text
from .video_processor import (
    text_to_speech,
    adjust_audio_duration,
    combine_audio_and_video,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def translate_video(input_path: str, output_path: str) -> None:
    """
    Translate a video from English to Vietnamese.

    Args:
        input_path (str): Path to the input video file.
        output_path (str): Path where the translated video will be saved.
    """
    try:
        input_path = Path(input_path)
        output_path = Path(output_path)

        logger.info(f"Processing video: {input_path}")

        # Extract audio
        audio_path = extract_audio(input_path)

        # Transcribe audio
        english_text = transcribe_audio(audio_path)

        # Split and translate text
        sentences = split_text(english_text)
        translated_sentences = [translate_text(sentence) for sentence in sentences]

        # Generate Vietnamese audio
        vietnamese_audio = text_to_speech(translated_sentences)

        # Adjust audio duration
        adjusted_audio = adjust_audio_duration(audio_path, vietnamese_audio)

        # Combine audio and video
        combine_audio_and_video(input_path, adjusted_audio, output_path)

        logger.info(f"Translated video saved to: {output_path}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python -m video_translator.main <input_video> <output_video>")
        sys.exit(1)
    translate_video(sys.argv[1], sys.argv[2])
