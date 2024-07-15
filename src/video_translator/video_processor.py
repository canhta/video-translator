from pathlib import Path
from gtts import gTTS
from pydub import AudioSegment
import moviepy.editor as mp
import tempfile


def text_to_speech(sentences: list[str]) -> Path:
    """
    Convert a list of sentences to speech.

    Args:
        sentences (list[str]): List of sentences to convert to speech.

    Returns:
        Path: Path to the generated audio file.
    """
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        temp_path = Path(temp_file.name)

    combined_audio = AudioSegment.empty()
    for sentence in sentences:
        tts = gTTS(text=sentence, lang="vi")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp_sentence:
            tts.save(temp_sentence.name)
            audio_segment = AudioSegment.from_mp3(temp_sentence.name)
            combined_audio += audio_segment

    combined_audio.export(temp_path, format="mp3")
    return temp_path


def adjust_audio_duration(original_audio: Path, generated_audio: Path) -> Path:
    """
    Adjust the duration of the generated audio to match the original audio.

    Args:
        original_audio (Path): Path to the original audio file.
        generated_audio (Path): Path to the generated audio file.

    Returns:
        Path: Path to the adjusted audio file.
    """
    original = AudioSegment.from_wav(original_audio)
    generated = AudioSegment.from_mp3(generated_audio)

    adjusted = generated.speedup(playback_speed=len(generated) / len(original))

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        temp_path = Path(temp_file.name)
        adjusted.export(temp_path, format="wav")

    return temp_path


def combine_audio_and_video(
    video_path: Path, audio_path: Path, output_path: Path
) -> None:
    """
    Combine video with the new audio.

    Args:
        video_path (Path): Path to the original video file.
        audio_path (Path): Path to the new audio file.
        output_path (Path): Path where the final video will be saved.
    """
    video = mp.VideoFileClip(str(video_path))
    audio = mp.AudioFileClip(str(audio_path))
    final_clip = video.set_audio(audio)
    final_clip.write_videofile(str(output_path))
