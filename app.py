import streamlit as st
import io
import docx
from summarizer_logic import generate_extractive_summary, generate_abstractive_summary, extract_keywords, generate_title
from ocr_translation_logic import extract_text_from_image, extract_text_from_pdf, extract_text_from_docx, translate_text
from googletrans import LANGUAGES

# --- Streamlit Configuration ---
st.set_page_config(page_title="Text Summarizer", page_icon="📝", layout="wide")

# Custom CSS for Premium Design
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTextArea textarea {
        background-color: #262730 !important;
        color: #FAFAFA !important;
        border-radius: 10px;
    }
    .stButton>button {
        background-color: #1DB954 !important;
        color: white !important;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1ed760 !important;
    }
    .title-text {
        font-size: 40px;
        font-weight: 900;
        background: -webkit-linear-gradient(45deg, #1DB954, #FFFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .summary-box {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #1DB954;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("Navigation")
menu = st.sidebar.radio("Go to", ["Home (Summarizer)", "Image to Text (OCR)", "Manage Profile", "Help and Support"])

# --- Session State Initialization ---
if 'raw_text' not in st.session_state:
    st.session_state['raw_text'] = ""
if 'summary_text' not in st.session_state:
    st.session_state['summary_text'] = ""

def create_docx(text):
    doc = docx.Document()
    doc.add_paragraph(text)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- Page: Home (Summarizer) ---
if menu == "Home (Summarizer)":
    st.markdown('<p class="title-text">📝 AI Text Summarizer</p>', unsafe_allow_html=True)
    st.write("Wrap up long texts into a specified short length. It condenses long articles to their main points.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Text")
        
        # File Uploading
        uploaded_file = st.file_uploader("Upload a Document (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"])
        if uploaded_file is not None:
            if uploaded_file.name.endswith(".pdf"):
                st.session_state['raw_text'] = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.name.endswith(".docx"):
                st.session_state['raw_text'] = extract_text_from_docx(uploaded_file)
            else:
                st.session_state['raw_text'] = str(uploaded_file.read(), "utf-8")
                
        # Text Area
        text_input = st.text_area("Or Paste/Type Text Here:", value=st.session_state['raw_text'], height=300)
        
        st.write(f"**Word Count:** {len(text_input.split()) if text_input else 0}")
        
        # Options
        summarize_type = st.radio("Summarization Type", ["Extractive (Fast)", "Abstractive (AI - Detailed)"])
        
        if summarize_type == "Extractive (Fast)":
            fraction = st.slider("Summary Length (Fraction of original)", min_value=0.1, max_value=0.9, value=0.3, step=0.1)
        else:
            max_len = st.slider("Max Length (Tokens)", min_value=30, max_value=300, value=130, step=10)
        
        if st.button("Summarize"):
            if not text_input.strip():
                st.warning("Please enter some text to summarize.")
            else:
                with st.spinner("Generating Summary..."):
                    if summarize_type == "Extractive (Fast)":
                        st.session_state['summary_text'] = generate_extractive_summary(text_input, fraction)
                    else:
                        st.session_state['summary_text'] = generate_abstractive_summary(text_input, max_length=max_len)

    with col2:
        st.subheader("Summary Result")
        if st.session_state['summary_text']:
            # Generate Title and Keywords
            st.markdown(f"### {generate_title(st.session_state['summary_text'])}")
            keywords = extract_keywords(st.session_state['summary_text'])
            if keywords:
                st.write(f"**Keywords:** {', '.join(keywords)}")
            
            st.markdown(f'<div class="summary-box">{st.session_state["summary_text"]}</div>', unsafe_allow_html=True)
            st.write(f"**Summary Word Count:** {len(st.session_state['summary_text'].split())}")
            
            # Translation Option
            st.markdown("---")
            st.write("**Translate Summary**")
            lang_options = {name.title(): code for code, name in LANGUAGES.items()}
            target_lang = st.selectbox("Select Language", list(lang_options.keys()), index=list(lang_options.values()).index('en'))
            
            if st.button("Translate"):
                with st.spinner("Translating..."):
                    translated = translate_text(st.session_state['summary_text'], target_language=lang_options[target_lang])
                    st.success("Translated Successfully!")
                    st.markdown(f'<div class="summary-box">{translated}</div>', unsafe_allow_html=True)
                    st.session_state['translated_text'] = translated
            
            # Save/Download Options
            st.markdown("---")
            text_to_download = st.session_state.get('translated_text', st.session_state['summary_text'])
            st.download_button(label="Download as TXT", data=text_to_download, file_name="summary.txt", mime="text/plain")
            st.download_button(label="Download as DOCX", data=create_docx(text_to_download), file_name="summary.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")


# --- Page: Image to Text (OCR) ---
elif menu == "Image to Text (OCR)":
    st.markdown('<p class="title-text">🖼️ Image to Text (OCR)</p>', unsafe_allow_html=True)
    st.write("Extract text from images using AI.")
    
    uploaded_img = st.file_uploader("Upload an Image (.png, .jpg, .jpeg)", type=["png", "jpg", "jpeg"])
    if uploaded_img is not None:
        st.image(uploaded_img, caption="Uploaded Image", use_column_width=True)
        if st.button("Extract Text"):
            with st.spinner("Extracting text..."):
                extracted_text = extract_text_from_image(uploaded_img)
                st.success("Extraction Complete!")
                st.text_area("Extracted Text:", value=extracted_text, height=200)
                
                # Option to send this to summarizer
                if st.button("Send to Summarizer"):
                    st.session_state['raw_text'] = extracted_text
                    st.info("Text sent! Please go to the 'Home' tab to summarize.")

# --- Page: Manage Profile ---
elif menu == "Manage Profile":
    st.markdown('<p class="title-text">👤 Manage Profile</p>', unsafe_allow_html=True)
    st.write("Create an account or login to save your documents to the cloud (Mockup)")
    
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    with tab1:
        st.text_input("Email/Username")
        st.text_input("Password", type="password")
        st.button("Log In")
    with tab2:
        st.text_input("Email")
        st.text_input("New Username")
        st.text_input("New Password", type="password")
        st.button("Sign Up")

# --- Page: Help and Support ---
elif menu == "Help and Support":
    st.markdown('<p class="title-text">📞 Help and Support</p>', unsafe_allow_html=True)
    st.write("Contact us for any queries or feedback.")
    
    st.text_input("Your Name")
    st.text_input("Your Email")
    st.text_area("Problem or Query", height=150)
    if st.button("Submit"):
        st.success("Your message has been sent successfully!")
