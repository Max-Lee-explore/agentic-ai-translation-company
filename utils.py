def get_supported_languages() -> list:
    """
    Returns a list of supported languages for translation.
    This can be expanded based on the AI model's capabilities.
    """
    return [
        "English",
        "Spanish",
        "French",
        "German",
        "Italian",
        "Portuguese",
        "Russian",
        "Chinese (Simplified)",
        "Chinese (Traditional)",
        "Japanese",
        "Korean",
        "Arabic",
        "Hindi",
        "Dutch",
        "Swedish",
        "Polish",
        "Turkish",
        "Vietnamese",
        "Thai",
        "Indonesian",
        "Greek"
    ]

def format_prompt_for_translation(text: str, source_lang: str, target_lang: str) -> str:
    """
    Format the prompt for the initial translation step.
    """
    return f"""Translate the following text from {source_lang} to {target_lang}.
Maintain the original meaning, tone, and style while ensuring natural flow in the target language. Do not add any additional text or comments.

Text to translate:
{text}

Translation:"""

def format_prompt_for_reflection(original: str, translation: str) -> str:
    """
    Format the prompt for the reflection step.
    """
    return f"""Review the following translation and provide detailed feedback on:
1. Accuracy of meaning
2. Natural flow and readability
3. Cultural appropriateness
4. Technical terminology (if any)
5. Areas for improvement

Original text:
{original}

Translation:
{translation}

Feedback:"""

def format_prompt_for_improvement(original: str, initial_translation: str, reflection: str) -> str:
    """
    Format the prompt for the improvement step.
    """
    return f"""Based on the following feedback, improve the translation while maintaining accuracy and natural flow. Do not add any additional text or comments.

Original text:
{original}

Initial translation:
{initial_translation}

Feedback:
{reflection}

Improved translation:"""

def format_prompt_for_terminology_check(translation: str, terminology: dict, source_lang: str, target_lang: str) -> str:
    """
    Format the prompt for the terminology check step.
    """
    terminology_list = "\n".join([f"{source}: {target}" for source, target in terminology.items()])
    
    return f"""Review the following translation and ensure all terms are translated according to the provided terminology list.
If any terms in the translation don't match the terminology list, correct them while maintaining the overall meaning and flow. Do not add any additional text or comments.

Terminology List ({source_lang} -> {target_lang}):
{terminology_list}

Translation to check:
{translation}

Please provide the corrected translation with proper terminology usage:""" 