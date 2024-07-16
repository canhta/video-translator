import argparse
import logging
from .video_processor import compose_final_video
from .audio_processor import generate_translated_speech, synchronize_audio
from .text_processor import parse_vtt, translate_text, align_translated_text, write_vtt_file
from .utils import (
    setup_logging,
    cleanup_temp_files,
    ensure_ffmpeg,
    get_input_files,
    get_output_files,
)


def main():
    try:
        # Parse command line arguments
        parser = argparse.ArgumentParser(
            description="Convert video speech from English to Vietnamese"
        )
        parser.add_argument("id", help="ID of the YouTube video to translate")
        args = parser.parse_args()
        id = args.id
        # Set up logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info(f"Starting video translation process for ID: {id}")

        # Ensure FFmpeg is installed
        ensure_ffmpeg()

        # Get input and output file paths
        input_files = get_input_files(id)
        output_files = get_output_files(id)

        # Step 1: Parse VTT subtitle file
        logger.info("Parsing VTT subtitle file")
        subtitles = parse_vtt(input_files["vtt"])

        # Step 2: Translate text from English to Vietnamese
        logger.info("Translating subtitles from English to Vietnamese")
        translated_subtitles = translate_text(subtitles)
        write_vtt_file(translated_subtitles, output_files["vtt"])

        # Step 3: Align translated text with original timing
        logger.info("Aligning translated text with original timing")
        aligned_translated_subtitles = align_translated_text(translated_subtitles, subtitles)

        # Step 4: Generate translated speech
        logger.info("Generating translated speech")
        translated_audio = generate_translated_speech(aligned_translated_subtitles)

        # Step 5: Synchronize translated audio with original audio
        logger.info("Synchronizing translated audio with original audio")
        synchronized_audio = synchronize_audio(
            input_files["audio"], translated_audio, aligned_translated_subtitles
        )

        # Step 6: Compose final video with translated audio
        logger.info("Composing final video with translated audio")
        compose_final_video(input_files["video"], synchronized_audio, output_files["video"])

        logger.info(f"Video translation completed successfully. Output saved as: {output_files["video"]}")
    except FileNotFoundError as e:
        logger.error(f"File not found: {str(e)}")
    except RuntimeError as e:
        logger.error(f"Runtime error: {str(e)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during video translation: {str(e)}")
    finally:
        # Clean up temporary files
        cleanup_temp_files()


if __name__ == "__main__":
    main()
