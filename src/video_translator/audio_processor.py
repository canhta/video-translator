import moviepy.editor as mp
import speech_recognition as sr
from pathlib import Path


def extract_audio(video_path: Path) -> Path:
    """
    Extract audio from a video file.

    Args:
        video_path (Path): Path to the input video file.

    Returns:
        Path: Path to the extracted audio file.
    """
    audio_path = video_path.with_suffix(".wav")
    video = mp.VideoFileClip(str(video_path))
    video.audio.write_audiofile(str(audio_path))
    return audio_path


def transcribe_audio(audio_path: Path) -> str:
    """
    Transcribe audio to text using Google Speech Recognition.

    Args:
        audio_path (Path): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(str(audio_path)) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        raise ValueError("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        raise ConnectionError(
            f"Could not request results from Google Speech Recognition service; {e}"
        )
