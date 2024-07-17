import os
import logging
from pydub import AudioSegment
from .utils import save_temporary_file
from gtts import gTTS

logger = logging.getLogger(__name__)


def time_to_seconds(time_str):
    """Convert time string (HH:MM:SS.mmm) to seconds."""
    h, m, s = time_str.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def process_audio(audio_file):
    # This function can be expanded to include any necessary audio processing
    logger.info(f"Processing audio file: {audio_file}")
    return audio_file


def generate_translated_speech(aligned_translated_subtitles):
    logger.info("Generating translated speech")
    translated_audio_segments = []
    for subtitle in aligned_translated_subtitles:
        text = subtitle["text"]
        start = time_to_seconds(subtitle["start"])
        end = time_to_seconds(subtitle["end"])
        duration = int((end - start) * 1000)  # Convert to milliseconds
        audio_segment = text_to_speech(text, "vi")
        # Adjust the duration of the generated speech to match the original subtitle timing
        if len(audio_segment) > duration:
            audio_segment = audio_segment[:duration]
        else:
            audio_segment = audio_segment + AudioSegment.silent(
                duration=duration - len(audio_segment)
            )
        translated_audio_segments.append(audio_segment)

    logger.info("Combining translated audio segments")
    combined_audio = sum(translated_audio_segments)
    output_file = save_temporary_file(suffix=".wav")
    combined_audio.export(output_file, format="wav")
    logger.info(f"Translated speech generated and saved to {output_file}")
    return output_file


def synchronize_audio(original_audio, translated_audio, aligned_translated_subtitles):
    logger.info("Synchronizing translated audio with original audio")

    try:
        # Try to load the original audio file based on its extension
        _, ext = os.path.splitext(original_audio)
        if ext.lower() == ".wav":
            original = AudioSegment.from_wav(original_audio)
        elif ext.lower() == ".mp3":
            original = AudioSegment.from_mp3(original_audio)
        else:
            original = AudioSegment.from_file(original_audio)

        # Try to load the translated audio file
        _, ext = os.path.splitext(translated_audio)
        if ext.lower() == ".wav":
            translated = AudioSegment.from_wav(translated_audio)
        elif ext.lower() == ".mp3":
            translated = AudioSegment.from_mp3(translated_audio)
        else:
            translated = AudioSegment.from_file(translated_audio)

    except Exception as e:
        logger.error(f"Error loading audio files: {str(e)}")
        raise

    synchronized = AudioSegment.silent(duration=len(original))

    for subtitle in aligned_translated_subtitles:
        start = int(time_to_seconds(subtitle["start"]) * 1000)  # Convert to milliseconds
        end = int(time_to_seconds(subtitle["end"]) * 1000)
        duration = end - start

        if len(translated) < duration:
            logger.warning(
                f"Translated audio is shorter than expected for subtitle: {subtitle['text']}"
            )
            translated_segment = translated
            translated = AudioSegment.empty()
        else:
            translated_segment = translated[:duration]
            translated = translated[duration:]

        synchronized = synchronized.overlay(translated_segment, position=start)

    output_file = save_temporary_file(suffix=".wav")
    synchronized.export(output_file, format="wav")
    logger.info(f"Synchronized audio saved to {output_file}")
    return output_file


def text_to_speech(text, lang):
    logger.info(f"Converting text to speech: {text[:30]}...")
    tts = gTTS(text=text, lang=lang)
    audio_file = save_temporary_file(suffix=".mp3")
    tts.save(audio_file)
    audio_segment = AudioSegment.from_mp3(audio_file)
    return audio_segment
