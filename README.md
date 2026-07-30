# TextSummarizer 📝

TextSummarizer is a high-level, full-stack Python web application built with **Streamlit**. It upgrades the traditional text summarization process by leveraging advanced Machine Learning and AI algorithms, providing both Extractive and Abstractive summarization, OCR capabilities, and language translation.

## Features ✨

- **Extractive Summarization:** Uses `spaCy` to score sentences based on word frequencies and extract the most important sentences from the text.
- **Abstractive Summarization:** Uses Hugging Face `transformers` to generate AI-powered, human-like summaries.
- **OCR (Image to Text):** Upload an image (JPG/PNG), and the application uses `EasyOCR` to extract the text automatically.
- **File Parsing:** Directly upload `.pdf` or `.docx` documents to extract and summarize the text.
- **Translation:** Translate your generated summaries into multiple languages using the `googletrans` API.
- **Keyword & Title Generation:** Automatically generates a title and extracts top keywords from your summary.
- **Export Options:** Download your summarized text as `.txt` or `.docx`.

## Technology Stack 🛠️

- **Frontend/UI:** Streamlit
- **NLP/Summarization:** SpaCy, Transformers (PyTorch)
- **OCR:** EasyOCR, OpenCV, Pillow
- **Translation:** Googletrans
- **File Extraction:** pdfplumber, python-docx

## Installation & Setup 🚀

To run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/araneeskhan/TextSummarizer.git
   cd TextSummarizer
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   # source env/bin/activate    # On macOS/Linux
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download the SpaCy English Language Model:**
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application 💻

Once everything is installed, you can start the Streamlit application by running:

```bash
streamlit run app.py
```

This will automatically open the application in your default web browser (usually at `http://localhost:8501`).

## Usage Guide 📖

- **Home (Summarizer):** Paste text or upload a document to get started. Adjust the sliders to choose between Extractive or Abstractive summarization.
- **Image to Text (OCR):** Upload an image to extract text, which you can then send to the Summarizer page.
- **Manage Profile & Help/Support:** Navigation tabs representing additional functionality and support pages.

## References 🔗
- [Dns Cache Poisoning Attack](https://drive.google.com/file/d/1dDXTXJaPmjgF5dOSJ9IZksL_hgoCNE-k/view?usp=sharing)

## License 📜
ⓒ 2026 - All Rights Reserved.
