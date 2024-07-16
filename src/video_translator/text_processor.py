import webvtt
import logging
import re
from googletrans import Translator
from typing import List, Dict

logger = logging.getLogger(__name__)


def parse_vtt(vtt_file: str) -> List[Dict[str, str]]:
    logger.info(f"Parsing VTT file: {vtt_file}")
    subtitles = [
        {"start": caption.start, "end": caption.end, "text": caption.text}
        for caption in webvtt.read(vtt_file)
    ]
    logger.info(f"Parsed {len(subtitles)} subtitles")
    return subtitles


def should_translate(text: str) -> bool:
    return not (
        text.strip().startswith("(")
        and text.strip().endswith(")")
        or text.strip().startswith("♪")
        and text.strip().endswith("♪")
    )


def merge_lines(text: str) -> str:
    lines = text.split("\n")
    merged_lines = []
    for i, line in enumerate(lines):
        if i > 0 and not lines[i - 1].strip().endswith((".", "!", "?", ":", ";")):
            merged_lines[-1] += " " + line.strip()
        else:
            merged_lines.append(line.strip())
    return " ".join(merged_lines)


def clean_text(text: str) -> str:
    logger.debug(f"Input text: {text}")

    # Merge multiple lines
    text = merge_lines(text)
    logger.debug(f"Merged text: {text}")

    # Store HTML-like tags
    tags = re.findall(r"<[^>]+>", text)

    # Remove HTML-like tags temporarily
    text = re.sub(r"<[^>]+>", "", text)

    # Remove speaker names (assume they're in all caps followed by a colon)
    text = re.sub(r"^([A-Z][A-Z\s]+:)", "", text)

    # Remove any remaining parentheses and their contents
    text = re.sub(r"\([^)]*\)", "", text)

    # Remove any leading/trailing whitespace
    text = text.strip()

    # Reinsert HTML-like tags
    for tag in tags:
        text = tag + text + tag.replace("<", "</")

    logger.debug(f"Cleaned text: {text}")
    return text


def translate_text(subtitles: List[Dict[str, str]]) -> List[Dict[str, str]]:
    logger.info("Translating subtitles from English to Vietnamese")
    translator = Translator()
    translated_subtitles = []

    for subtitle in subtitles:
        try:
            text = subtitle["text"]
            logger.debug(f"Original text: {text}")
            if should_translate(text):
                cleaned_text = clean_text(text)
                logger.debug(f"Cleaned text: {cleaned_text}")
                if cleaned_text:
                    # Remove HTML-like tags before translation
                    text_to_translate = re.sub(r"<[^>]+>", "", cleaned_text)
                    translated_text = translator.translate(
                        text_to_translate, src="en", dest="vi"
                    ).text
                    # Reinsert HTML-like tags
                    tags = re.findall(r"<[^>]+>", cleaned_text)
                    for tag in tags:
                        translated_text = tag + translated_text + tag.replace("<", "</")
                    logger.debug(f"Translated text: {translated_text}")
                else:
                    translated_text = text  # Keep original if cleaned text is empty
                    logger.debug("Using original text (cleaned text was empty)")
            else:
                translated_text = text
                logger.debug("Using original text (should not translate)")

            translated_subtitles.append(
                {"start": subtitle["start"], "end": subtitle["end"], "text": translated_text}
            )
        except Exception as e:
            logger.error(f"Error translating subtitle: {subtitle['text']}. Error: {str(e)}")
            translated_subtitles.append(subtitle)  # Keep original if translation fails

    logger.info(f"Translated {len(translated_subtitles)} subtitles")
    return translated_subtitles


def align_translated_text(
    translated_subtitles: List[Dict[str, str]], original_subtitles: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    logger.info("Aligning translated text with original timing")
    aligned_subtitles = [
        {"start": orig["start"], "end": orig["end"], "text": trans["text"]}
        for trans, orig in zip(translated_subtitles, original_subtitles)
    ]
    logger.info(f"Aligned {len(aligned_subtitles)} subtitles")
    return aligned_subtitles


def write_vtt_file(captions, output_file_path):
    logger.info("Writing translated subtitles to VTT file")

    with open(output_file_path, "w", encoding="utf-8") as file:
        # Write the VTT header
        file.write("WEBVTT\n")
        file.write("Kind: captions\n")
        file.write("Language: vi\n\n")

        for caption in captions:
            start = caption["start"]
            end = caption["end"]
            text = caption["text"]

            # Write each caption
            file.write(f"{start} --> {end}\n")
            file.write(f"{text}\n\n")

    logger.info(f"VTT file saved as: {output_file_path}")
