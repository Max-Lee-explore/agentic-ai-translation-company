from typing import Dict, List, Tuple
import os
from dotenv import load_dotenv
import requests

class ManagerAgent:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("AI_API_KEY")
        if not self.api_key:
            raise ValueError("AI_API_KEY not found in environment variables")
        self.provider = os.getenv("AI_PROVIDER", "xai").lower()
        self.model = os.getenv("DEFAULT_MODEL", "gpt-4")
        self.temperature = 0.7

    def analyze_brief(self, translation_type: str, brief: str, source_text: str = "") -> Dict:
        """
        Analyze the translation brief and determine the appropriate translation approach.
        If no brief is provided or "Help me to decide" is selected, analyze the source text to determine the appropriate style.
        
        Args:
            translation_type: Type of translation (e.g., "Business", "Legal", "Literary", "Help me to decide")
            brief: Detailed brief from the user
            source_text: Source text to analyze if no brief is provided or "Help me to decide" is selected
            
        Returns:
            Dictionary containing:
            - selected_translators: List of translator types to use
            - style_guidelines: Specific style requirements
            - quality_requirements: Quality standards to maintain
            - detected_style: Style detected from source text (if no brief or "Help me to decide")
            - reasoning: Explanation of the manager's decision
        """
        # Define available translators
        available_translators = {
            "Legal": "Legal Translator",
            "Literary": "Literary Translator",
            "Business": "Business Translator",
            "Technical": "Technical Translator",
            "Medical": "Medical Translator",
            "News": "News Translator",
            "Academic": "Academic Translator",
            "Marketing": "Marketing Translator",
            "Master Translator": "Master Translator"
        }

        if translation_type == "Help me to decide" or (not brief and source_text):
            # Analyze source text to determine style
            prompt = f"""As a Translation Project Manager, analyze the following text and determine its style and appropriate translation approach:

Text to analyze:
{source_text[:1000]}  # Analyze first 1000 characters for efficiency

Available translators:
{', '.join(available_translators.keys())}

Please provide:
1. The detected style/type of the text (choose from available types or specify if none match)
2. A list of specialized translators needed (prioritize using available translators)
3. Specific style guidelines to follow
4. Quality requirements and standards to maintain
5. Detailed reasoning for your decisions, including why you chose this particular translator type

Format your response as a JSON object with the following structure:
{{
    "detected_style": "style_name",
    "selected_translators": ["translator1", "translator2"],
    "style_guidelines": ["guideline1", "guideline2"],
    "quality_requirements": ["requirement1", "requirement2"],
    "reasoning": "explanation of decisions"
}}"""
        else:
            # Use provided brief
            prompt = f"""As a Translation Project Manager, analyze the following translation brief and determine the best approach:

Translation Type: {translation_type}
Brief: {brief}

Available translators:
{', '.join(available_translators.keys())}

Please provide:
1. A list of specialized translators needed (prioritize using available translators)
2. Specific style guidelines to follow
3. Quality requirements and standards to maintain
4. Detailed reasoning for your decisions

Format your response as a JSON object with the following structure:
{{
    "selected_translators": ["translator1", "translator2"],
    "style_guidelines": ["guideline1", "guideline2"],
    "quality_requirements": ["requirement1", "requirement2"],
    "reasoning": "explanation of decisions"
}}"""

        messages = [
            {"role": "system", "content": "You are an experienced Translation Project Manager who specializes in coordinating translation projects."},
            {"role": "user", "content": prompt}
        ]

        response = self.call_ai_api(messages)
        analysis = self._parse_response(response)
        
        # Ensure we're using available translators
        if "selected_translators" in analysis:
            # Map the selected translators to available ones
            mapped_translators = []
            for translator in analysis["selected_translators"]:
                # Check if the translator matches any available type
                found_match = False
                for type_name, translator_name in available_translators.items():
                    if type_name.lower() in translator.lower():
                        mapped_translators.append(translator_name)
                        found_match = True
                        break
                if not found_match:
                    # If no match found, use Master Translator
                    mapped_translators.append("Master Translator")
            
            analysis["selected_translators"] = mapped_translators
            if "reasoning" in analysis:
                analysis["reasoning"] += "\nNote: Some requested translators were mapped to available specialists or the Master Translator."
        
        return analysis

    def select_translators(self, translation_type: str, brief: str) -> List[str]:
        """
        Select appropriate translators based on the translation type and brief.
        
        Args:
            translation_type: Type of translation
            brief: Detailed brief from the user
            
        Returns:
            List of translator types to use
        """
        analysis = self.analyze_brief(translation_type, brief)
        return analysis["selected_translators"]

    def get_style_guidelines(self, translation_type: str, brief: str) -> List[str]:
        """
        Get style guidelines based on the translation type and brief.
        
        Args:
            translation_type: Type of translation
            brief: Detailed brief from the user
            
        Returns:
            List of style guidelines to follow
        """
        analysis = self.analyze_brief(translation_type, brief)
        return analysis["style_guidelines"]

    def get_quality_requirements(self, translation_type: str, brief: str) -> List[str]:
        """
        Get quality requirements based on the translation type and brief.
        
        Args:
            translation_type: Type of translation
            brief: Detailed brief from the user
            
        Returns:
            List of quality requirements to maintain
        """
        analysis = self.analyze_brief(translation_type, brief)
        return analysis["quality_requirements"]

    def call_ai_api(self, messages: List[Dict]) -> str:
        """Call the appropriate AI API based on the provider."""
        if self.provider == "xai":
            return self._call_xai_api(messages)
        elif self.provider == "openai":
            return self._call_openai_api(messages)
        elif self.provider == "anthropic":
            return self._call_anthropic_api(messages)
        elif self.provider == "google":
            return self._call_google_api(messages)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _call_xai_api(self, messages: List[Dict]) -> str:
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

    def _call_openai_api(self, messages: List[Dict]) -> str:
        """Call the OpenAI API with the given messages."""
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

    def _call_anthropic_api(self, messages: List[Dict]) -> str:
        """Call the Anthropic API with the given messages."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }
        
        # Convert messages to Anthropic format
        prompt = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": self.temperature,
            "max_tokens": 4000
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["content"][0]["text"]
        except Exception as e:
            print("Error calling Anthropic API:", e)
            raise

    def _call_google_api(self, messages: List[Dict]) -> str:
        """Call the Google AI API with the given messages."""
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key
        }
        
        # Convert messages to Google format
        contents = [{"parts": [{"text": m["content"]}]} for m in messages]
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": self.temperature
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print("Error calling Google AI API:", e)
            raise

    def _parse_response(self, response: str) -> Dict:
        """Parse the API response into a structured dictionary."""
        try:
            # Find the JSON object in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx == -1 or end_idx == 0:
                raise ValueError("No JSON object found in response")
            
            json_str = response[start_idx:end_idx]
            import json
            parsed = json.loads(json_str)
            
            # Ensure all required fields are present
            if "reasoning" not in parsed:
                parsed["reasoning"] = "No specific reasoning provided"
            if "detected_style" not in parsed:
                parsed["detected_style"] = None
                
            return parsed
        except Exception as e:
            print("Error parsing response:", e)
            # Return default values if parsing fails
            return {
                "selected_translators": ["General Translator"],
                "style_guidelines": ["Maintain professional tone", "Ensure accuracy"],
                "quality_requirements": ["High accuracy", "Natural flow"],
                "reasoning": "Using default settings due to parsing error",
                "detected_style": None
            } 