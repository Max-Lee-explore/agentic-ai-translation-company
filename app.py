import os
import gradio as gr
from dotenv import load_dotenv
from file_handlers import FileHandler
from translation_agents import TranslationPipeline
from utils import get_supported_languages

# Load environment variables
load_dotenv()

class TranslationApp:
    def __init__(self):
        self.file_handler = FileHandler()
        self.translation_pipeline = TranslationPipeline()
        self.supported_languages = get_supported_languages()

    def process_translation(self, file, terminology_file, source_lang, target_lang):
        try:
            # Process the input file
            text_chunks = self.file_handler.process_file(file.name)
            
            # Process terminology if provided
            if terminology_file:
                self.translation_pipeline.set_terminology(
                    terminology_file.name,
                    source_lang,
                    target_lang
                )
            
            # Translate the text
            translated_text, translation_details = self.translation_pipeline.translate(
                text_chunks,
                source_lang,
                target_lang
            )
            
            # Save the translated file
            translated_file = self.file_handler.save_translated_file(translated_text, file.name)
            
            # Save the translation details
            details_file = self.file_handler.save_translation_details(translation_details, file.name)
            
            # Prepare status message
            status = f"Translation completed in {translation_details['total_time']} seconds.\n"
            status += f"Total tokens used: {translation_details['total_tokens']}"
            
            return translated_file, details_file, status
            
        except Exception as e:
            return None, None, f"Error during translation: {str(e)}"

def create_interface():
    app = TranslationApp()
    
    with gr.Blocks(title="AI Translation System", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# AI-Powered Translation System")
        gr.Markdown("Upload your file and select languages to translate")
        
        with gr.Row():
            with gr.Column():
                file_input = gr.File(
                    label="Upload File to Translate",
                    file_types=[".pdf", ".docx", ".pptx", ".json", ".html", ".txt", ".md"],
                    type="filepath"
                )
                terminology_file = gr.File(
                    label="Upload Terminology List (Optional)",
                    file_types=[".csv", ".json", ".xlsx", ".xls", ".txt"],
                    type="filepath"
                )
                source_lang = gr.Dropdown(
                    choices=app.supported_languages,
                    label="Source Language",
                    value="English"
                )
                target_lang = gr.Dropdown(
                    choices=app.supported_languages,
                    label="Target Language",
                    value="Spanish"
                )
                translate_btn = gr.Button("Translate", variant="primary")
            
            with gr.Column():
                translated_file = gr.File(label="Translated File")
                details_file = gr.File(label="Translation Details")
                status = gr.Textbox(label="Status", interactive=False)
        
        translate_btn.click(
            fn=app.process_translation,
            inputs=[file_input, terminology_file, source_lang, target_lang],
            outputs=[translated_file, details_file, status]
        )
        
        gr.Markdown("""
        ### Supported File Formats
        - PDF (.pdf)
        - Microsoft Word (.docx)
        - Microsoft PowerPoint (.pptx)
        - JSON (.json)
        - HTML (.html)
        - Plain Text (.txt, .md)

        ### Terminology List Formats
        - CSV (.csv) - Two columns: source term, target term
        - JSON (.json) - Dictionary of terms
        - Excel (.xlsx, .xls) - Two columns: source term, target term
        - Text (.txt) - Tab or colon-separated terms
        """)
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True) 