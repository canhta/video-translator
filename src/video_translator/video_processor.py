import subprocess
import logging
from .utils import save_temporary_file

logger = logging.getLogger(__name__)


def extract_audio(input_video):
    output_audio = save_temporary_file(suffix=".wav")
    try:
        logger.info(f"Extracting audio from {input_video}")
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_video,
                "-vn",
                "-acodec",
                "pcm_s16le",
                "-ar",
                "44100",
                "-ac",
                "2",
                output_audio,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Audio extracted successfully to {output_audio}")
        return output_audio
    except subprocess.CalledProcessError as e:
        logger.error(f"Error extracting audio: {e.stderr}")
        raise


def compose_final_video(input_video, synchronized_audio, output_video):
    try:
        logger.info(f"Composing final video with translated audio")
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                input_video,
                "-i",
                synchronized_audio,
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-map",
                "0:v:0",
                "-map",
                "1:a:0",
                output_video,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Final video composed successfully: {output_video}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error composing final video: {e.stderr}")
        raise
