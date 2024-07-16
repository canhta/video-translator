import logging
import os
import shutil
import tempfile

temp_files = []


def get_input_files(video_id):
    base_path = os.path.join("input", video_id)
    files = {
        "audio": os.path.join(base_path, "audio.mp3"),
        "video": os.path.join(base_path, "video.mp4"),
        "vtt": os.path.join(
            base_path, "video.en.vtt"
        ),  # Using video.en.vtt instead of audio.en.vtt
    }

    for key, path in files.items():
        if not os.path.exists(path):
            raise FileNotFoundError(f"{key.capitalize()} file not found: {path}")

    return files


def get_output_files(video_id):
    # base_path = os.path.join("output", video_id)
    files = {
        "audio": os.path.join("output", video_id, "audio.mp3"),
        "video": os.path.join("output", video_id, "video.mp4"),
        "vtt": os.path.join("output", video_id, "video.vi.vtt"),
    }

    for key, path in files.items():
        if not os.path.exists(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)

    return files


def save_temporary_file(suffix=".tmp"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    temp_files.append(path)
    return path


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def cleanup_temp_files():
    for file in temp_files:
        try:
            os.remove(file)
        except Exception as e:
            logging.warning(f"Failed to remove temporary file {file}: {str(e)}")
    temp_files.clear()


def ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "FFmpeg is not installed or not in the system PATH. Please install FFmpeg to use this tool."
        )
