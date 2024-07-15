import pytest
from gtts import gTTS
from video_translator.audio_processor import extract_audio, transcribe_audio
import moviepy.editor as mp
import speech_recognition as sr


@pytest.fixture
def sample_video(tmp_path):
    video_path = tmp_path / "sample.mp4"
    clip = mp.ColorClip(size=(320, 240), color=(255, 0, 0), duration=1)
    clip.write_videofile(str(video_path), fps=24)
    return video_path


def test_extract_audio(sample_video):
    audio_path = extract_audio(sample_video)
    assert audio_path.exists()
    assert audio_path.suffix == ".wav"


@pytest.mark.parametrize(
    "text",
    [
        "Hello, world!",
        "This is a test.",
        "Python is awesome.",
    ],
)
def test_transcribe_audio(tmp_path, text):
    audio_path = tmp_path / "test_audio.wav"
    tts = gTTS(text=text, lang="en")
    tts.save(str(audio_path))

    transcribed_text = transcribe_audio(audio_path)
    assert transcribed_text.lower() == text.lower()


def test_transcribe_audio_error(tmp_path):
    invalid_audio_path = tmp_path / "invalid_audio.wav"
    invalid_audio_path.touch()  # Create an empty file

    with pytest.raises(ValueError):
        transcribe_audio(invalid_audio_path)
