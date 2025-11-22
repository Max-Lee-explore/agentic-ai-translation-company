from typing import List, Optional, Dict, Tuple
import os
import time
from dotenv import load_dotenv
from .terminology_handler import TerminologyHandler
from .manager_agent import ManagerAgent
from .specialized_translators import (
    LiteraryTranslator,
    LegalTranslator,
    MasterTranslator,
    NewsTranslator,
    AcademicTranslator,
    TechnicalTranslator,
    MedicalTranslator,
    MarketingTranslator,
    BusinessTranslator
)
from .utils import (
    format_prompt_for_translation,
    format_prompt_for_reflection,
    format_prompt_for_improvement,
    format_prompt_for_terminology_check
)
import requests

class TranslationPipeline:
    def __init__(self, api_key: str, provider: str = "openrouter", model: str = "gpt-4", temperatures: Optional[Dict[str, float]] = None):
        self.api_key = api_key
        self.provider = provider.lower()
        self.model = model
        self.terminology_handler = TerminologyHandler(api_key, provider, model)
        self.manager_agent = ManagerAgent(api_key, provider, model)
        
        # Default temperatures
        default_temps = {
            'literary': 0.8,
            'legal': 0.65,
            'technical': 0.65,
            'medical': 0.6,
            'news': 0.7,
            'academic': 0.7,
            'marketing': 0.8,
            'business': 0.7,
            'master': 0.7
        }
        
        # Merge with custom temperatures if provided
        if temperatures:
            default_temps.update(temperatures)
        
        # Initialize translators with custom temperatures
        self.literary_translator = LiteraryTranslator(api_key, provider, model, default_temps['literary'])
        self.legal_translator = LegalTranslator(api_key, provider, model, default_temps['legal'])
        self.news_translator = NewsTranslator(api_key, provider, model, default_temps['news'])
        self.academic_translator = AcademicTranslator(api_key, provider, model, default_temps['academic'])
        self.technical_translator = TechnicalTranslator(api_key, provider, model, default_temps['technical'])
        self.medical_translator = MedicalTranslator(api_key, provider, model, default_temps['medical'])
        self.marketing_translator = MarketingTranslator(api_key, provider, model, default_temps['marketing'])
        self.business_translator = BusinessTranslator(api_key, provider, model, default_temps['business'])
        self.master_translator = MasterTranslator(api_key, provider, model, default_temps['master'])
        
        self.system_role = "You are an expert and experienced translator who knows many languages."
        self.temperature = 0.8
        self.total_tokens = 0
        self.translation_time = 0
        self.translation_details = []

    def call_ai_api(self, messages):
        """Call the appropriate AI API based on the provider."""
        if self.provider == "xai":
            return self._call_xai_api(messages)
        elif self.provider == "openai":
            return self._call_openai_api(messages)
        elif self.provider == "anthropic":
            return self._call_anthropic_api(messages)
        elif self.provider == "google":
            return self._call_google_api(messages)
        elif self.provider == "openrouter":
            return self._call_openrouter_api(messages)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _call_openrouter_api(self, messages):
        """Call the OpenRouter API with the given messages."""
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:5173",  # Client URL
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
            # Update token count
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling OpenRouter API:", e)
            raise

    def _call_xai_api(self, messages):
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
            # Update token count
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling XAI API:", e)
            raise

    def _call_openai_api(self, messages):
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
            # Update token count
            self.total_tokens += data.get("usage", {}).get("total_tokens", 0)
            return data["choices"][0]["message"]["content"]
        except Exception as e:
            print("Error calling OpenAI API:", e)
            raise

    def _call_anthropic_api(self, messages):
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
            # Update token count (approximate)
            self.total_tokens += len(prompt.split()) + len(data["content"][0]["text"].split())
            return data["content"][0]["text"]
        except Exception as e:
            print("Error calling Anthropic API:", e)
            raise

    def _call_google_api(self, messages):
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
            # Update token count (approximate)
            self.total_tokens += sum(len(m["content"].split()) for m in messages) + len(data["candidates"][0]["content"]["parts"][0]["text"].split())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            print("Error calling Google AI API:", e)
            raise

    def set_terminology(self, terminology_file: str, source_lang: str, target_lang: str) -> None:
        """Set the terminology for translation."""
        self.terminology_handler.load_terminology(terminology_file, source_lang, target_lang)

    def translate(self, text_chunks: List[str], source_lang: str, target_lang: str, translation_type: str, brief: str = "", glossary: Dict[str, str] = None, model_name: str = None, provider_name: str = None):
        """
        Run the translation pipeline on the input text chunks.
        Yields status updates and finally the result.
        Tracks token usage throughout the process.
        """
        print("\nStarting translation process...")
        print(f"Source language: {source_lang}")
        print(f"Target language: {target_lang}")
        print(f"Translation type: {translation_type}")
        print(f"Provider: {provider_name or self.provider}")
        print(f"Model: {model_name or self.model}")
        
        # Initialize token counter
        total_tokens = 0
        
        # Step 1: Analyze brief and select translators (Manager Agent)
        print("\nAnalyzing text...")
        yield {"status": "Analyzing text..."}
        
        # If "Help me to decide" or no brief, analyze source text
        source_text_for_analysis = text_chunks[0] if text_chunks else ""
        analysis = self.manager_agent.analyze_brief(translation_type, brief, source_text_for_analysis)
        
        # Track tokens from analysis (estimate if not available)
        if isinstance(analysis, dict) and 'usage' in analysis:
            total_tokens += analysis.get('usage', {}).get('total_tokens', 0)
        
        print(f"Analysis complete: {analysis}")
        selected_translators = analysis["selected_translators"]
        style_guidelines = analysis["style_guidelines"]
        quality_requirements = analysis["quality_requirements"]
        detected_style = analysis.get("detected_style")
        
        if detected_style:
            print(f"Using detected style: {detected_style}")
        
        yield {"status": "analysis_complete", "analysis": analysis}

        # Step 2: Process chunks
        translated_chunks = []
        all_chunk_details = []
        
        for i, chunk in enumerate(text_chunks):
            print(f"\nProcessing chunk {i+1} of {len(text_chunks)}")
            yield {"status": f"Processing chunk {i+1}/{len(text_chunks)}", "progress": (i / len(text_chunks)) * 100}
            
            chunk_detail = {"original": chunk, "steps": []}
            
            # Estimate tokens for this chunk (rough approximation: 1 token ≈ 4 characters)
            chunk_tokens_estimate = len(chunk) // 4
            
            # 2.1 Initial Translation
            print("Step 1: Initial Translation")
            yield {"status": "Initial translation"}
            initial_translation = self._initial_translation_with_specialist(
                chunk, source_lang, target_lang, selected_translators, style_guidelines
            )
            chunk_detail["steps"].append({
                "step": "Initial Translation",
                "result": initial_translation
            })
            # Estimate: input + output tokens
            total_tokens += chunk_tokens_estimate + (len(initial_translation) // 4)
            
            # 2.2 Reflection
            print("Step 2: Reflection")
            yield {"status": "Reflection"}
            reflection = self._reflect_on_translation(
                chunk, initial_translation, source_lang, target_lang, 
                style_guidelines, quality_requirements
            )
            chunk_detail["steps"].append({
                "step": "Reflection",
                "result": reflection
            })
            # Estimate: combined input + reflection output
            total_tokens += (chunk_tokens_estimate + len(initial_translation) // 4) + (len(reflection) // 4)
            
            # 2.3 Improvement
            print("Step 3: Improvement")
            yield {"status": "Improvement"}
            improved_translation = self._improve_translation(
                chunk, initial_translation, reflection, source_lang, target_lang,
                style_guidelines, quality_requirements
            )
            chunk_detail["steps"].append({
                "step": "Improvement",
                "result": improved_translation
            })
            # Estimate: all context + improved output
            total_tokens += (chunk_tokens_estimate + len(initial_translation) // 4 + len(reflection) // 4) + (len(improved_translation) // 4)
            
            # 2.4 Terminology Check (skip if no glossary)
            if glossary:
                print("Step 4: Terminology Check")
                yield {"status": "Terminology check"}
                final_translation = self._check_terminology(
                    chunk, improved_translation, source_lang, target_lang, glossary
                )
                chunk_detail["steps"].append({
                    "step": "Terminology Check",
                    "result": final_translation
                })
                # Estimate: improved translation + glossary + final output
                glossary_size = sum(len(k) + len(v) for k, v in glossary.items()) // 4
                total_tokens += (len(improved_translation) // 4 + glossary_size) + (len(final_translation) // 4)
            else:
                print("Step 4: Skipping Terminology Check (no glossary provided)")
                final_translation = improved_translation
            
            translated_chunks.append(final_translation)
            all_chunk_details.append(chunk_detail)

        # Combine results
        final_text = "\n\n".join(translated_chunks)
        
        print(f"\nTranslation completed successfully! Total tokens used (estimated): {total_tokens}")
        yield {
            "status": "completed",
            "result": {
                "translated_text": final_text,
                "details": {
                    "analysis": analysis,
                    "selected_translators": selected_translators,
                    "style_guidelines": style_guidelines,
                    "quality_requirements": quality_requirements,
                    "chunks": all_chunk_details,
                    "total_tokens": total_tokens,
                    "model": model_name or self.model,
                    "provider": provider_name or self.provider
                }
            }
        }

    def _initial_translation_with_specialist(self, text: str, source_lang: str, target_lang: str, selected_translators: List[str], style_guidelines: List[str] = None) -> str:
        """Initial translation step using specialized translator."""
        # Use the first selected translator (primary choice)
        if not selected_translators:
            translator = "master"
        else:
            translator_desc = selected_translators[0].lower()
            if "literary" in translator_desc or "creative" in translator_desc or "artistic" in translator_desc:
                translator = "literary"
            elif "legal" in translator_desc:
                translator = "legal"
            elif "technical" in translator_desc:
                translator = "technical"
            elif "medical" in translator_desc:
                translator = "medical"
            elif "news" in translator_desc or "journal" in translator_desc:
                translator = "news"
            elif "academic" in translator_desc or "scholarly" in translator_desc:
                translator = "academic"
            elif "marketing" in translator_desc or "promotional" in translator_desc:
                translator = "marketing"
            elif "business" in translator_desc or "corporate" in translator_desc:
                translator = "business"
            else:
                translator = "master"
        
        # Call the appropriate translator
        if translator == "literary":
            return self.literary_translator.translate(text, source_lang, target_lang)
        elif translator == "legal":
            return self.legal_translator.translate(text, source_lang, target_lang)
        elif translator == "technical":
            return self.technical_translator.translate(text, source_lang, target_lang)
        elif translator == "medical":
            return self.medical_translator.translate(text, source_lang, target_lang)
        elif translator == "news":
            return self.news_translator.translate(text, source_lang, target_lang)
        elif translator == "academic":
            return self.academic_translator.translate(text, source_lang, target_lang)
        elif translator == "marketing":
            return self.marketing_translator.translate(text, source_lang, target_lang)
        elif translator == "business":
            return self.business_translator.translate(text, source_lang, target_lang)
        else:
            # Use master translator with style guidelines
            quality_reqs = ["High accuracy", "Natural flow", "Cultural appropriateness"]
            return self.master_translator.translate(text, source_lang, target_lang, style_guidelines or [], quality_reqs)

    def _reflect_on_translation(self, original: str, translation: str, source_lang: str, target_lang: str, style_guidelines: List[str], quality_requirements: List[str]) -> str:
        """
        Reflection step to analyze the translation quality.
        """
        guidelines_str = "\n".join([f"- {g}" for g in style_guidelines]) if style_guidelines else "None specified"
        requirements_str = "\n".join([f"- {r}" for r in quality_requirements]) if quality_requirements else "None specified"
        
        prompt = f"""Analyze this translation from {source_lang} to {target_lang}:

Original text:
{original}

Translation:
{translation}

Style Guidelines:
{guidelines_str}

Quality Requirements:
{requirements_str}

Provide a detailed critique covering:
1. Accuracy and completeness
2. Style and tone adherence  
3. Cultural appropriateness
4. Areas for improvement

Keep your analysis concise and actionable."""
        
        messages = [
            {"role": "system", "content": "You are a Translation Quality Analyst reviewing translations."},
            {"role": "user", "content": prompt}
        ]
        return self.call_ai_api(messages)

    def _improve_translation(self, original: str, initial_translation: str, reflection: str, source_lang: str, target_lang: str, style_guidelines: List[str], quality_requirements: List[str]) -> str:
        """
        Final improvement step based on reflection.
        """
        guidelines_str = "\n".join([f"- {g}" for g in style_guidelines]) if style_guidelines else "None specified"
        requirements_str = "\n".join([f"- {r}" for r in quality_requirements]) if quality_requirements else "None specified"
        
        prompt = f"""Improve this translation from {source_lang} to {target_lang} based on the feedback:

Original text:
{original}

Current translation:
{initial_translation}

Feedback:
{reflection}

Style Guidelines:
{guidelines_str}

Quality Requirements:
{requirements_str}

Provide ONLY the improved translation, without any explanation."""
        
        messages = [
            {"role": "system", "content": "You are a Translation Editor improving translations based on feedback."},
            {"role": "user", "content": prompt}
        ]
        return self.call_ai_api(messages)

    def _check_terminology(self, original: str, translation: str, source_lang: str, target_lang: str, glossary: Dict[str, str] = None) -> str:
        """
        Check and correct terminology in the translation.
        """
        return self.terminology_handler.check_terminology(translation, source_lang, target_lang, glossary)