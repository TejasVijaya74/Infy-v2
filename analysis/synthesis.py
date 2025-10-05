# analysis/synthesis.py

import pandas as pd
import streamlit as st
from transformers import pipeline
import re # Import the regular expression module for cleaning

@st.cache_resource
def load_summarizer_model():
    """Loads and caches the AI summarization model."""
    print("Loading AI Summarizer Model (T5-Small)...")
    model = pipeline(
        "summarization",
        model="t5-small",
        device=-1 
    )
    print("AI Summarizer Model Loaded.")
    return model

def generate_summary(df: pd.DataFrame) -> str:
    """
    Generates a concise executive summary from a dataframe of news articles.
    """
    if df.empty or len(df) < 3:
        return "Not enough data available to generate a summary."

    print("Generating AI Executive Summary...")
    summarizer = load_summarizer_model()

    df_sorted = df.sort_values(by='sentiment_score', ascending=False)
    
    # --- NEW: Text Cleaning and Validation ---
    def clean_text(text):
        """Removes newlines, extra spaces, and non-ASCII characters."""
        if not isinstance(text, str):
            return ""
        text = text.replace('\n', ' ').replace('\r', ' ') # Remove newlines
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)       # Remove non-ASCII characters
        text = re.sub(' +', ' ', text).strip()           # Remove extra spaces
        return text

    # Select and clean text from the most relevant articles
    top_positive_text = " ".join(df_sorted.head(3)['full_text'].apply(clean_text).to_list())
    top_negative_text = " ".join(df_sorted.tail(2)['full_text'].apply(clean_text).to_list())
    
    full_context = f"summarize: Positive news highlights: {top_positive_text}. Negative news highlights: {top_negative_text}"

    # --- NEW: Quality check for the input context ---
    # If the combined text is too short, it's not worth summarizing.
    if len(full_context) < 150:
        print("Not enough text content to generate a meaningful summary.")
        return "Not enough article content was found to generate a reliable AI summary. Please try a broader topic or a different time range."

    max_input_length = 1024
    truncated_context = full_context[:max_input_length]

    # Generate the summary
    summary_result = summarizer(
        truncated_context, 
        max_length=150,
        min_length=40,
        do_sample=False
    )
    
    print("Summary Generated.")
    return summary_result[0]['summary_text']