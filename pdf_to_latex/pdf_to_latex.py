import os
import sys
import json
from PyPDF2 import PdfReader
import openai
from dotenv import load_dotenv
from langdetect import detect  # Import was missing

load_dotenv()

# Initialize OpenRouter with Mistral-7B-Instruct-v0.2
openai.api_key = os.getenv("OPENROUTER_API_KEY")
openai.api_base = "https://openrouter.ai/api/v1"

# Mistral-7B-Instruct-v0.2 is a great free option for document processing

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file with better formatting."""
    try:
        reader = PdfReader(pdf_path)
        text = ""
        for page in reader.pages:
            # Extract text with better spacing
            page_text = page.extract_text()
            # Clean up text by removing extra spaces and newlines
            page_text = ' '.join(page_text.split())
            text += page_text + "\n\n"
        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        sys.exit(1)

def detect_language(text):
    """Detect the language of the input text."""
    try:
        return detect(text)
    except Exception as e:  # Added explicit exception handling
        print(f"Error detecting language: {e}")
        return "en"

def convert_to_latex(text, template=None, target_language=None):
    """Convert text to LaTeX format using Mistral-7B-Instruct-v0.2."""
    try:
        # Prepare system message with detailed instructions
        system_message = """You are a PDF to LaTeX converter. Your task is to convert the given text into proper LaTeX format while maintaining the exact document structure. Follow these rules:

1. Keep all mathematical notation exactly as it appears in the original text
2. Maintain proper formatting for equations and symbols
3. Preserve all special characters and accents
4. Keep the exact structure of exercises and questions
5. Use appropriate LaTeX environments for lists and equations
6. Maintain proper spacing and alignment
7. Use \section* for unnumbered sections
8. Properly format mathematical notation with \text{} for text in math mode
9. Use proper LaTeX commands for special characters and accents
10. Maintain consistent document structure

The output should be a complete, compilable LaTeX document that looks as close as possible to the original PDF."""
        
        if template:
            if os.path.exists(template):  # If it's a file path
                with open(template, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                system_message += f"\nUse this template as a reference:\n{template_content}"
            else:  # If it's a prompt
                system_message += f"\nUse this template description:\n{template}"
        else:
            system_message += "\nIf no specific template is provided, maintain the original structure of the document."

        if target_language:
            system_message += f"\nConvert the content to {target_language} while maintaining the document structure."

        # Truncate text if it's too long (OpenAI API has token limits)
        max_length = 15000  # Adjust based on model token limits
        if len(text) > max_length:
            print(f"Warning: Text is too long ({len(text)} chars). Truncating to {max_length} chars.")
            text = text[:max_length]

        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct-v0.2",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": f"Convert the following text to LaTeX format:\n\n{text}"
                }
            ],
            headers={
                "HTTP-Referer": "https://openrouter.ai/",  # Required for OpenRouter
            }
        )
        
        # Process the response to ensure proper LaTeX formatting
        latex_content = response.choices[0].message.content
        
        # Remove unwanted text like code blocks
        if "```latex" in latex_content:
            latex_content = latex_content.split("```latex")[1]
            if "```" in latex_content:
                latex_content = latex_content.split("```")[0]
        
        # Add necessary packages if not present
        if '\\documentclass' not in latex_content:
            latex_content = r"""\documentclass{article}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{enumitem}
\usepackage{siunitx}
\usepackage{physics}
\usepackage{mathtools}
\usepackage{bm}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[french]{babel}

\begin{document}

""" + latex_content
        
        # Ensure proper document structure
        if '\\end{document}' not in latex_content:
            latex_content += "\n\\end{document}"
        
        # Post-process the LaTeX content to fix common issues
        latex_content = latex_content.replace('\\text{SC}', '\\text{SC}')
        latex_content = latex_content.replace('\\text{R}', '\\text{R}')
        latex_content = latex_content.replace('\\text{AB}', '\\text{AB}')
        latex_content = latex_content.replace('\\text{A�?TB�?T}', '\\text{A\\textquotesingle B\\textquotesingle}')
        latex_content = latex_content.replace('\\text{d�?T}', '\\text{d\\textquotesingle}')
        
        return latex_content
    except Exception as e:
        print(f"Error converting to LaTeX: {e}")
        sys.exit(1)

def save_latex_output(latex_content, output_path):
    """Save the LaTeX content to a file."""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        print(f"LaTeX file saved as: {output_path}")
    except Exception as e:
        print(f"Error saving LaTeX file: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("1. python pdf_to_latex.py input.pdf")
        print("2. python pdf_to_latex.py input.pdf template.tex")
        print("3. python pdf_to_latex.py input.pdf \"prompt_for_template\"")
        print("4. python pdf_to_latex.py input.pdf template.tex target_language")
        print("5. python pdf_to_latex.py input.pdf \"prompt_for_template\" target_language")
        sys.exit(1)

    input_pdf = sys.argv[1]
    template = None
    target_language = None
    
    # Create output filename based on input filename
    output_tex = os.path.splitext(os.path.basename(input_pdf))[0] + ".tex"

    # Check if input file exists
    if not os.path.exists(input_pdf):
        print(f"Error: Input file {input_pdf} not found")
        sys.exit(1)

    # Process the PDF
    print(f"Processing {input_pdf}...")
    pdf_text = extract_text_from_pdf(input_pdf)

    # Handle different usage patterns
    if len(sys.argv) >= 3:  # Check for template or prompt
        template = sys.argv[2]
        
    if len(sys.argv) >= 4:  # Check for target language
        target_language = sys.argv[3]

    # Convert to LaTeX
    print("Converting to LaTeX...")
    latex_content = convert_to_latex(pdf_text, template, target_language)
    
    # Save the output
    save_latex_output(latex_content, output_tex)
    print("Conversion complete!")

if __name__ == "__main__":
    main()