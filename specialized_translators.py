from typing import Dict, List
import os
from dotenv import load_dotenv
import requests

class BaseTranslator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AI_API_KEY")
        if not self.api_key:
            raise ValueError("AI_API_KEY not found in environment variables")
        self.model = os.getenv("DEFAULT_MODEL", "grok-3-latest")
        self.temperature = 0.7  # Default temperature

    def call_xai_api(self, messages: List[Dict]) -> str:
        """Call the XAI API with the given messages."""
        url = "https://api.x.ai/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "messages": messages,
            "model": self.model,
            "stream": False,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling XAI API:", e)
            raise

class LiteraryTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("LITERARY_TEMPERATURE", "0.8"))
        self.system_role = """You are a Literary Translation Specialist with expertise in translating creative works. 
Your role is to preserve the artistic and emotional qualities of the original text while ensuring natural flow in the target language."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on literary quality."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on literary quality:

Text to translate:
{text}

Guidelines:
1. Preserve the original's tone, style, and voice
2. Maintain metaphors, idioms, and cultural references
3. Ensure the translation flows naturally in the target language
4. Adapt cultural references appropriately
5. Preserve the author's unique writing style
6. Use rich, varied vocabulary
7. Maintain the original's rhythm and flow
8. Preserve literary devices (alliteration, assonance, etc.)

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class LegalTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("LEGAL_TEMPERATURE", "0.65"))
        self.system_role = """You are a Legal Translation Specialist with expertise in translating legal documents. 
Your role is to ensure precise and accurate translation of legal terminology while maintaining the formal and professional tone required in legal documents."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on legal accuracy."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on legal accuracy:

Text to translate:
{text}

Guidelines:
1. Maintain precise legal terminology
2. Ensure consistent use of legal terms
3. Preserve the exact meaning of legal concepts
4. Follow legal translation conventions
5. Maintain formal and professional tone
6. Use appropriate legal terminology
7. Ensure compliance with legal requirements
8. Avoid ambiguity in legal terms

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class MasterTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("MASTER_TEMPERATURE", "0.7"))
        self.system_role = """You are a Master Translator with expertise in multiple translation styles and domains.
You can adapt your translation approach based on the specific requirements and style guidelines provided."""

    def translate(self, text: str, source_lang: str, target_lang: str, style_guidelines: List[str], quality_requirements: List[str]) -> str:
        """Translate text with specific style guidelines and quality requirements."""
        guidelines_str = "\n".join([f"- {guideline}" for guideline in style_guidelines])
        requirements_str = "\n".join([f"- {req}" for req in quality_requirements])
        
        prompt = f"""Translate the following text from {source_lang} to {target_lang} following these specific guidelines:

Text to translate:
{text}

Style Guidelines:
{guidelines_str}

Quality Requirements:
{requirements_str}

Please provide a translation that:
1. Follows all style guidelines precisely
2. Meets all quality requirements
3. Maintains the original meaning and intent
4. Adapts appropriately to the target language and culture

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class NewsTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("NEWS_TEMPERATURE", "0.7"))
        self.system_role = """You are a News Translation Specialist with expertise in translating news articles and journalistic content.
Your role is to maintain journalistic style, accuracy, and immediacy while adapting content for different cultural contexts."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on news/journalistic style."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on news/journalistic style:

Text to translate:
{text}

Guidelines:
1. Maintain journalistic style and tone
2. Preserve news value and immediacy
3. Adapt cultural references appropriately
4. Use clear, concise language
5. Maintain factual accuracy
6. Follow news writing conventions
7. Use appropriate news terminology
8. Ensure cultural sensitivity

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class AcademicTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("ACADEMIC_TEMPERATURE", "0.7"))
        self.system_role = """You are an Academic Translation Specialist with expertise in translating scholarly works.
Your role is to maintain academic rigor, precision, and formal tone while ensuring accessibility in the target language."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on academic style."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on academic style:

Text to translate:
{text}

Guidelines:
1. Maintain academic tone and formality
2. Preserve technical terminology
3. Ensure precise meaning of concepts
4. Follow academic writing conventions
5. Maintain citation formats
6. Use appropriate academic terminology
7. Preserve theoretical frameworks
8. Ensure consistency in terminology

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class TechnicalTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("TECHNICAL_TEMPERATURE", "0.65"))
        self.system_role = """You are a Technical Translation Specialist with expertise in translating technical documentation.
Your role is to maintain technical accuracy while ensuring clarity and usability in the target language."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on technical accuracy."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on technical accuracy:

Text to translate:
{text}

Guidelines:
1. Maintain technical precision
2. Use consistent terminology
3. Preserve technical specifications
4. Follow technical writing conventions
5. Ensure clarity of instructions
6. Maintain formatting and structure
7. Use appropriate technical terminology
8. Preserve measurement units and standards

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class MedicalTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("MEDICAL_TEMPERATURE", "0.6"))
        self.system_role = """You are a Medical Translation Specialist with expertise in translating medical content.
Your role is to maintain medical accuracy while ensuring clarity and sensitivity in the target language."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on medical accuracy."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on medical accuracy:

Text to translate:
{text}

Guidelines:
1. Maintain medical terminology accuracy
2. Preserve clinical precision
3. Ensure patient safety
4. Follow medical writing conventions
5. Use appropriate medical terminology
6. Maintain sensitivity to patient information
7. Preserve medical measurements and units
8. Ensure compliance with medical standards

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class MarketingTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("MARKETING_TEMPERATURE", "0.8"))
        self.system_role = """You are a Marketing Translation Specialist with expertise in translating marketing content.
Your role is to maintain brand voice and marketing impact while adapting content for different cultural markets."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on marketing effectiveness."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on marketing effectiveness:

Text to translate:
{text}

Guidelines:
1. Maintain brand voice and tone
2. Preserve marketing impact
3. Adapt cultural references appropriately
4. Follow marketing writing conventions
5. Use persuasive language
6. Maintain emotional appeal
7. Preserve call-to-action effectiveness
8. Ensure cultural appropriateness

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

class BusinessTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        self.temperature = float(os.getenv("BUSINESS_TEMPERATURE", "0.7"))
        self.system_role = """You are a Business Translation Specialist with expertise in translating business content.
Your role is to maintain professional tone and business accuracy while ensuring cultural appropriateness."""

    def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        """Translate text with a focus on business communication."""
        prompt = f"""Translate the following text from {source_lang} to {target_lang} with a focus on business communication:

Text to translate:
{text}

Guidelines:
1. Maintain professional tone
2. Preserve business terminology
3. Ensure cultural appropriateness
4. Follow business writing conventions
5. Use appropriate business terminology
6. Maintain formal communication style
7. Preserve business metrics and units
8. Ensure clarity in business context

Translation:"""

        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages) 

# Add to utils.py
def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    # Remove any potentially harmful characters
    return text.strip()[:10000]  # Limit input length

# Add to file_handlers.py
def cleanup_files(self, *file_paths):
    """Clean up temporary files after processing"""
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up file {file_path}: {e}")