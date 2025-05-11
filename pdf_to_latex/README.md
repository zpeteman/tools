# PDF to LaTeX Converter

This tool converts PDF documents into LaTeX format with support for multiple languages using AI.

## Features
- Converts PDF to LaTeX
- Supports multiple languages
- Uses AI for document understanding and conversion
- Maintains document structure

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your OpenRouter API key:
```
OPENROUTER_API_KEY=your_api_key_here
```

## Usage
```bash
python pdf_to_latex.py input.pdf --output output.tex --language english
```

## Supported Languages
- English
- Spanish
- French
- German
- Italian
- And more...

## Note
Make sure to sign up for an OpenRouter account and get your API key from https://openrouter.ai/
