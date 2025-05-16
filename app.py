import os
import gradio as gr
from dotenv import load_dotenv
from file_handlers import FileHandler
from translation_agents import TranslationPipeline
from utils import get_supported_languages
import base64

# Load environment variables
load_dotenv()

def get_base64_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

class TranslationApp:
    def __init__(self):
        self.file_handler = FileHandler()
        self.translation_pipeline = TranslationPipeline()
        self.supported_languages = get_supported_languages()

    def process_translation(self, file, terminology_file, source_lang, target_lang, translation_type, manager_brief):
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
            
            # Translate the text with the manager's brief
            translated_text, translation_details = self.translation_pipeline.translate(
                text_chunks,
                source_lang,
                target_lang,
                translation_type,
                manager_brief
            )
            
            # Save the translated file
            translated_file = self.file_handler.save_translated_file(translated_text, file.name, translation_details)
            
            # Save the translation details
            details_file = self.file_handler.save_translation_details(translation_details, file.name)
            
            # Prepare status message
            status = f"Translation completed in {translation_details['total_time']} seconds.\n"
            status += f"Total tokens used: {translation_details['total_tokens']}\n"
            status += f"Translation type: {translation_details['translation_type']}\n"
            status += f"Selected translators: {', '.join(translation_details['selected_translators'])}\n"
            status += f"\nManager's Decision:\n{translation_details['manager_reasoning']}"
            
            return translated_file, details_file, status
            
        except Exception as e:
            return None, None, f"Error during translation: {str(e)}"

def create_interface():
    app = TranslationApp()
    
    # Get base64 encoded background image
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bg_image_path = os.path.join(current_dir, 'images', 'bg.png')
    bg_image_base64 = get_base64_image(bg_image_path)
    
    # Custom CSS for background image
    custom_css = f"""
    .gradio-container {{
        background-image: url('data:image/png;base64,{bg_image_base64}');
        background-size: 100% auto;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
        width: 100%;
        margin: 0;
        padding: 0;
    }}
    """
    
    with gr.Blocks(title="Agentic AI Translation System", theme=gr.themes.Soft(), css=custom_css) as interface:
        gr.Markdown("<h1 style='text-align: center;'>Agentic AI Translation System</h1>")
        gr.Markdown("<p style='text-align: center; font-size: 1.2em; color: #FF6B00;'>From Manager to Proofreader: An agentic AI translation system built on collaboration, role-based expertise, and full-stack delivery.</p>")
        gr.Markdown("### Upload your file and select languages to translate")
        
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
                
                # New UI elements for manager briefing
                translation_type = gr.Dropdown(
                    choices=[
                        "Help me to decide",
                        "Business",
                        "Legal",
                        "Literary",
                        "Technical",
                        "Medical",
                        "News",
                        "Academic",
                        "Marketing",
                        "Master Translator"
                    ],
                    label="Translation Type",
                    value="Business"
                )
                
                manager_brief = gr.Textbox(
                    label="Brief for Translation Manager",
                    placeholder="Describe your translation needs, style preferences, and any specific requirements...",
                    lines=4
                )
                
                translate_btn = gr.Button("Translate", variant="primary")
            
            with gr.Column():
                translated_file = gr.File(label="Translated File")
                details_file = gr.File(label="Translation Details")
                status = gr.Textbox(label="Status", interactive=False)
                
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
        
        translate_btn.click(
            fn=app.process_translation,
            inputs=[
                file_input,
                terminology_file,
                source_lang,
                target_lang,
                translation_type,
                manager_brief
            ],
            outputs=[translated_file, details_file, status]
        )
        
        gr.Markdown("---")  # Add a horizontal line
        gr.Markdown("### Created by Max Lee")
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(share=True) 