import pytest
from video_translator.text_processor import split_text, translate_text


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Hello. How are you? I'm fine!", ["Hello.", "How are you?", "I'm fine!"]),
        (
            "This is a test. It has multiple sentences.",
            ["This is a test.", "It has multiple sentences."],
        ),
        ("Single sentence.", ["Single sentence."]),
    ],
)
def test_split_text(input_text, expected):
    assert split_text(input_text) == expected


@pytest.mark.parametrize(
    "input_text,expected",
    [
        ("Hello", "Xin chào"),
        ("Good morning", "Chào buổi sáng"),
        ("How are you?", "Bạn khỏe không?"),
    ],
)
def test_translate_text(input_text, expected):
    assert translate_text(input_text).lower() == expected.lower()


def test_translate_text_error():
    with pytest.raises(RuntimeError):
        translate_text("" * 5000)  # Try to translate an extremely long text
