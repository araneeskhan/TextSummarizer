import spacy
from heapq import nlargest
from transformers import pipeline

# Load SpaCy model for extractive summarization
# Ensure the model is downloaded via: python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Warning: 'en_core_web_sm' model not found. Extractive summarization will fail until it is downloaded.")
    nlp = None

# Load HuggingFace Transformers pipeline for abstractive summarization
try:
    # Using a fast, standard summarization model for CPU efficiency
    summarizer_pipeline = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
except Exception as e:
    print(f"Warning: Transformers summarization pipeline failed to load: {e}")
    summarizer_pipeline = None


def generate_extractive_summary(text, fraction=0.3):
    """
    Generates an extractive summary using SpaCy based on word frequencies.
    """
    if not nlp:
        return "Error: SpaCy model not loaded."
    
    doc = nlp(text)
    
    # Calculate word frequencies
    word_freq = {}
    for token in doc:
        if token.text.lower() not in spacy.lang.en.stop_words.STOP_WORDS and token.text.lower() not in spacy.lang.punctuation:
            if token.text.lower() not in word_freq.keys():
                word_freq[token.text.lower()] = 1
            else:
                word_freq[token.text.lower()] += 1
                
    if not word_freq:
        return "Not enough meaningful words to summarize."
        
    max_freq = max(word_freq.values())
    
    # Normalize frequencies
    for word in word_freq.keys():
        word_freq[word] = word_freq[word] / max_freq
        
    # Score sentences
    sent_score = {}
    sent_tokens = [sent for sent in doc.sents]
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text.lower()]
                else:
                    sent_score[sent] += word_freq[word.text.lower()]
                    
    # Select top fraction of sentences
    select_length = max(1, int(len(sent_tokens) * fraction))
    summary_sents = nlargest(select_length, sent_score, key=sent_score.get)
    
    # Reorder sentences to their original order in the text
    summary_sents = sorted(summary_sents, key=lambda x: sent_tokens.index(x))
    
    final_summary = [word.text for word in summary_sents]
    return " ".join(final_summary)


def generate_abstractive_summary(text, max_length=130, min_length=30):
    """
    Generates an abstractive summary using HuggingFace Transformers.
    """
    if not summarizer_pipeline:
        return "Error: Summarization model not loaded."
    
    # Ensure input isn't too long for the model
    # Most models accept up to 1024 tokens. We'll truncate roughly based on chars.
    if len(text) > 4000:
        text = text[:4000]
        
    try:
        summary = summarizer_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error during abstractive summarization: {str(e)}"


def extract_keywords(text, num_keywords=5):
    """
    Extracts top keywords based on word frequency.
    """
    if not nlp:
        return []
        
    doc = nlp(text)
    word_freq = {}
    for token in doc:
        if token.is_alpha and token.text.lower() not in spacy.lang.en.stop_words.STOP_WORDS:
            word = token.text.lower()
            word_freq[word] = word_freq.get(word, 0) + 1
            
    top_words = nlargest(num_keywords, word_freq, key=word_freq.get)
    return top_words


def generate_title(text):
    """
    Generates a simple title based on the top 2-3 keywords.
    """
    keywords = extract_keywords(text, num_keywords=3)
    if keywords:
        title = " ".join(keywords).title()
        return f"Summary of {title}"
    return "Generated Summary"
