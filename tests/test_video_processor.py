import pytest
from pathlib import Path
from video_translator.video_processor import (
    text_to_speech,
    adjust_audio_duration,
    combine_audio_and_video,
)
import moviepy.editor as mp
from pydub import AudioSegment


@pytest.fixture
def sample_sentences():
    return ["Xin chào.", "Đây là một bài kiểm tra.", "Python thật tuyệt vời."]


def test_text_to_speech(sample_sentences, tmp_path):
    audio_path = text_to_speech(sample_sentences)
    assert audio_path.exists()
    assert audio_path.suffix == ".mp3"


def test_adjust_audio_duration(tmp_path):
    original_audio = tmp_path / "original.wav"
    generated_audio = tmp_path / "generated.mp3"

    AudioSegment.silent(duration=1000).export(original_audio, format="wav")
    AudioSegment.silent(duration=2000).export(generated_audio, format="mp3")

    adjusted_audio = adjust_audio_duration(original_audio, generated_audio)
    assert adjusted_audio.exists()
    assert adjusted_audio.suffix == ".wav"

    adjusted = AudioSegment.from_wav(str(adjusted_audio))
    assert abs(len(adjusted) - 1000) < 50  # Allow small difference due to processing


def test_combine_audio_and_video(tmp_path):
    video_path = tmp_path / "sample.mp4"
    audio_path = tmp_path / "sample.wav"
    output_path = tmp_path / "output.mp4"

    clip = mp.ColorClip(size=(320, 240), color=(255, 0, 0), duration=1)
    clip.write_videofile(str(video_path), fps=24)
    AudioSegment.silent(duration=1000).export(audio_path, format="wav")

    combine_audio_and_video(video_path, audio_path, output_path)
    assert output_path.exists()
    assert output_path.suffix == ".mp4"
