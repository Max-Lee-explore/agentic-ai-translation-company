# AI-Powered Translation System

This is an advanced translation system that uses multiple AI agents to provide high-quality translations. The system supports various file formats and implements a multi-step translation process with reflection and improvement stages.

## Features

- Drag-and-drop file upload interface
- Support for multiple file formats (PDF, DOCX, PPTX, JSON, HTML, TXT)
- Multiple language pair selection
- Multi-step translation process with reflection and improvement
- Automatic text chunking for large documents
- Download translated files
- Google Drive integration (optional)

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys:
   ```
   AI_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open the web interface (default: http://localhost:7860)
2. Upload a file using drag-and-drop or file browser
3. Select source and target languages
4. Click "Translate"
5. Download the translated file when processing is complete

## Supported File Formats

- PDF (.pdf)
- Microsoft Word (.docx)
- Microsoft PowerPoint (.pptx)
- JSON (.json)
- HTML (.html)
- Plain Text (.txt, .md)

## Translation Process

1. File Processing
   - File type detection
   - Text extraction
   - Chunking (if needed)

2. Translation Pipeline
   - Initial translation
   - Reflection and review
   - Improvement and editing

3. Output Generation
   - Format reconstruction
   - File saving
   - Download preparation 