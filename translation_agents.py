from typing import List, Optional, Dict, Tuple
import os
import time
from dotenv import load_dotenv
from terminology_handler import TerminologyHandler
from utils import (
    format_prompt_for_translation,
    format_prompt_for_reflection,
    format_prompt_for_improvement,
    format_prompt_for_terminology_check
)
import requests

class TranslationPipeline:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AI_API_KEY")
        if not self.api_key:
            raise ValueError("AI_API_KEY not found in environment variables")
        self.terminology_handler = TerminologyHandler()
        self.model = "grok-3-latest"
        self.system_role = "You are an expert and experienced translator who knows many languages."
        self.temperature = 0.8
        self.total_tokens = 0
        self.translation_time = 0
        self.translation_details = []

    def call_xai_api(self, messages):
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
            print("XAI API response status:", response.status_code)
            print("XAI API response text:", response.text)
            response.raise_for_status()
            data = response.json()
            # Update token count
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling XAI API:", e)
            raise

    def set_terminology(self, terminology_file: str, source_lang: str, target_lang: str) -> None:
        """Set the terminology for translation."""
        self.terminology_handler.load_terminology(terminology_file, source_lang, target_lang)

    def translate(self, text: List[str], source_lang: str, target_lang: str) -> Tuple[str, Dict]:
        """
        Process text chunks through the translation pipeline.
        
        Args:
            text: List of text chunks to translate
            source_lang: Source language
            target_lang: Target language
            
        Returns:
            Tuple of (translated text, translation details)
        """
        start_time = time.time()
        translated_chunks = []
        self.translation_details = []
        self.total_tokens = 0
        
        for i, chunk in enumerate(text):
            chunk_details = {
                "chunk_number": i + 1,
                "original_text": chunk,
                "steps": []
            }
            
            # Step 1: Initial Translation
            initial_translation = self._initial_translation(chunk, source_lang, target_lang)
            chunk_details["steps"].append({
                "step": "Initial Translation",
                "result": initial_translation
            })
            
            # Step 2: Reflection
            reflection = self._reflect_on_translation(chunk, initial_translation)
            chunk_details["steps"].append({
                "step": "Reflection",
                "result": reflection
            })
            
            # Step 3: Improved Translation
            improved_translation = self._improve_translation(chunk, initial_translation, reflection)
            chunk_details["steps"].append({
                "step": "Improved Translation",
                "result": improved_translation
            })
            
            # Step 4: Terminology Check
            final_translation = self._check_terminology(improved_translation, source_lang, target_lang)
            chunk_details["steps"].append({
                "step": "Terminology Check",
                "result": final_translation
            })
            
            translated_chunks.append(final_translation)
            self.translation_details.append(chunk_details)
        
        self.translation_time = time.time() - start_time
        
        # Prepare translation details
        details = {
            "total_time": round(self.translation_time, 2),
            "total_tokens": self.total_tokens,
            "chunks": self.translation_details
        }
        
        return "\n".join(translated_chunks), details

    def _initial_translation(self, text: str, source_lang: str, target_lang: str) -> str:
        """
        Initial translation step.
        To be implemented with actual AI API call.
        """
        prompt = format_prompt_for_translation(text, source_lang, target_lang)
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

    def _reflect_on_translation(self, original: str, translation: str) -> str:
        """
        Reflection step to analyze the translation quality.
        To be implemented with actual AI API call.
        """
        prompt = format_prompt_for_reflection(original, translation)
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

    def _improve_translation(self, original: str, initial_translation: str, reflection: str) -> str:
        """
        Final improvement step based on reflection.
        To be implemented with actual AI API call.
        """
        prompt = format_prompt_for_improvement(original, initial_translation, reflection)
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages)

    def _check_terminology(self, translation: str, source_lang: str, target_lang: str) -> str:
        """
        Check and correct terminology in the translation.
        To be implemented with actual AI API call.
        """
        if not self.terminology_handler.terminology_dict:
            return translation
        prompt = format_prompt_for_terminology_check(
            translation,
            self.terminology_handler.get_all_terms(),
            source_lang,
            target_lang
        )
        messages = [
            {"role": "system", "content": self.system_role},
            {"role": "user", "content": prompt}
        ]
        return self.call_xai_api(messages) 