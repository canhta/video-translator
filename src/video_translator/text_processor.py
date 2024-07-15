from googletrans import Translator
import re

def split_text(text: str) -> list[str]:
    """
    Split the input text into sentences.
    
    Args:
        text (str): The input text to be split.
    
    Returns:
        list[str]: A list of sentences.
    """
    # This is a simple sentence splitter. For more complex texts, consider using nltk.
    return re.split(r'(?<=[.!?])\s+', text)

def translate_text(text: str) -> str:
    """
    Translate the input text from English to Vietnamese.
    
    Args:
        text (str): The input text to be translated.
    
    Returns:
        str: The translated text.
    """
    translator = Translator()
    try:
        result = translator.translate(text, src='en', dest='vi')
        return result.text
    except Exception as e:
        raise RuntimeError(f"Translation failed: {str(e)}")