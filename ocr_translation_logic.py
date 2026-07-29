import easyocr
from googletrans import Translator
import pdfplumber
from docx import Document
from PIL import Image
import numpy as np

# Initialize OCR Reader (Language: English)
try:
    reader = easyocr.Reader(['en'], gpu=False)
except Exception as e:
    print(f"Warning: EasyOCR failed to initialize: {e}")
    reader = None

# Initialize Translator
translator = Translator()

def extract_text_from_image(image_file):
    """
    Extracts text from an uploaded image file using EasyOCR.
    """
    if not reader:
        return "Error: OCR engine not initialized."
        
    try:
        # Convert PIL Image or file-like object to numpy array for EasyOCR
        img = Image.open(image_file)
        img_np = np.array(img)
        
        # Read text
        result = reader.readtext(img_np, detail=0)
        return " ".join(result)
    except Exception as e:
        return f"Error during OCR extraction: {str(e)}"

def translate_text(text, target_language='en'):
    """
    Translates text to the specified target language using Google Translate API.
    """
    try:
        translated = translator.translate(text, dest=target_language)
        return translated.text
    except Exception as e:
        return f"Error during translation: {str(e)}"

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from a PDF file.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(docx_file):
    """
    Extracts text from a Word document (.docx).
    """
    text = ""
    try:
        doc = Document(docx_file)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
