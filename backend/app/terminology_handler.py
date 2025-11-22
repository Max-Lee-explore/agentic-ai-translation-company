from typing import Dict, List, Optional
import json
import csv
import pandas as pd
import requests

class TerminologyHandler:
    def __init__(self, api_key: str = None, provider: str = "openrouter", model: str = "gpt-4", temperature: float = 0.7):
        self.terminology_dict: Dict[str, str] = {}
        self.source_lang: Optional[str] = None
        self.target_lang: Optional[str] = None
        self.api_key = api_key
        self.provider = provider.lower() if provider else "openrouter"
        self.model = model
        self.temperature = temperature

    def call_ai_api(self, messages: List[Dict]) -> str:
        """Call the appropriate AI API based on the provider."""
        if not self.api_key:
            # If no API key, just return the text unchanged
            return messages[-1]["content"].split("Text to review:")[-1].split("Guidelines:")[0].strip()
        
        if self.provider == "openrouter":
            return self._call_openrouter_api(messages)
        elif self.provider == "openai":
            return self._call_openai_api(messages)
        elif self.provider == "xai":
            return self._call_xai_api(messages)
        else:
            # Fallback: return text unchanged
            return messages[-1]["content"].split("Text to review:")[-1].split("Guidelines:")[0].strip()

    def _call_openrouter_api(self, messages: List[Dict]) -> str:
        """Call the OpenRouter API."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5173",
            "X-Title": "Agentic AI Translator"
        }
        payload = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling OpenRouter API:", e)
            raise

    def _call_openai_api(self, messages: List[Dict]) -> str:
        """Call the OpenAI API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "messages": messages,
            "model": self.model,
            "temperature": self.temperature
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling OpenAI API:", e)
            raise

    def _call_xai_api(self, messages: List[Dict]) -> str:
        """Call the XAI API."""
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

    def check_terminology(self, text: str, source_lang: str, target_lang: str, glossary: Dict[str, str] = None) -> str:
        """
        Check and correct terminology in the translated text.
        If a glossary is provided, prioritize its terms.
        """
        glossary_prompt = ""
        if glossary:
            glossary_str = "\n".join([f"{k} -> {v}" for k, v in glossary.items()])
            glossary_prompt = f"""
            Strictly enforce the following terminology glossary:
            {glossary_str}
            """

        prompt = f"""Review the following translation from {source_lang} to {target_lang} for terminology accuracy and consistency.
        
        {glossary_prompt}

        Text to review:
        {text}
        
        Guidelines:
        1. Ensure technical terms are used correctly
        2. Check for consistency across the text
        3. Verify domain-specific terminology
        4. Maintain standard industry terms
        5. If a glossary is provided, YOU MUST use the terms from it.
        
        Return ONLY the corrected text. If no changes are needed, return the original text."""

        messages = [
            {"role": "system", "content": "You are a Terminology Specialist. Your role is to ensure precise and consistent use of terminology."},
            {"role": "user", "content": prompt}
        ]
        
        return self.call_ai_api(messages)

    def load_terminology(self, file_path: str, source_lang: str, target_lang: str) -> None:
        """
        Load terminology from various file formats.
        Supported formats: CSV, JSON, Excel, TXT
        """
        self.source_lang = source_lang
        self.target_lang = target_lang
        
        file_ext = file_path.lower().split('.')[-1]
        
        if file_ext == 'csv':
            self._load_from_csv(file_path)
        elif file_ext == 'json':
            self._load_from_json(file_path)
        elif file_ext in ['xlsx', 'xls']:
            self._load_from_excel(file_path)
        elif file_ext == 'txt':
            self._load_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported terminology file format: {file_ext}")

    def _load_from_csv(self, file_path: str) -> None:
        """Load terminology from CSV file."""
        try:
            df = pd.read_csv(file_path)
            if len(df.columns) < 2:
                raise ValueError("CSV must have at least 2 columns: source term and target term")
            
            self.terminology_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            raise ValueError(f"Error loading CSV terminology file: {str(e)}")

    def _load_from_json(self, file_path: str) -> None:
        """Load terminology from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self.terminology_dict = data
                else:
                    raise ValueError("JSON must be a dictionary of terms")
        except Exception as e:
            raise ValueError(f"Error loading JSON terminology file: {str(e)}")

    def _load_from_excel(self, file_path: str) -> None:
        """Load terminology from Excel file."""
        try:
            df = pd.read_excel(file_path)
            if len(df.columns) < 2:
                raise ValueError("Excel must have at least 2 columns: source term and target term")
            
            self.terminology_dict = dict(zip(df.iloc[:, 0], df.iloc[:, 1]))
        except Exception as e:
            raise ValueError(f"Error loading Excel terminology file: {str(e)}")

    def _load_from_txt(self, file_path: str) -> None:
        """Load terminology from TXT file (tab-separated or colon-separated)."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    
                    if '\t' in line:
                        source, target = line.split('\t', 1)
                    elif ':' in line:
                        source, target = line.split(':', 1)
                    else:
                        continue
                    
                    self.terminology_dict[source.strip()] = target.strip()
        except Exception as e:
            raise ValueError(f"Error loading TXT terminology file: {str(e)}")

    def get_translation(self, term: str) -> Optional[str]:
        """Get the translation for a term if it exists in the terminology."""
        return self.terminology_dict.get(term)

    def get_all_terms(self) -> Dict[str, str]:
        """Get all terminology pairs."""
        return self.terminology_dict.copy()

    def clear_terminology(self) -> None:
        """Clear all loaded terminology."""
        self.terminology_dict.clear()
        self.source_lang = None
        self.target_lang = None 