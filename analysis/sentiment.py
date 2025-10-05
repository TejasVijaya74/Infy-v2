# analysis/sentiment.py

import pandas as pd
import streamlit as st
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline
from tqdm import tqdm # Import tqdm for the progress bar

# --- MODEL LOADING ---
@st.cache_resource
def load_roberta_model():
    """Loads and caches the RoBERTa sentiment analysis model."""
    print("Loading Deep Analysis Model (RoBERTa)...")
    model = pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment-latest",
        device=-1 
    )
    print("Deep Analysis Model Loaded.")
    return model

# --- ANALYSIS FUNCTIONS ---

def _analyze_sentiment_vader(text_series: pd.Series) -> tuple[pd.Series, pd.Series]:
    """Analyzes sentiment using the fast VADER model."""
    analyzer = SentimentIntensityAnalyzer()
    scores = text_series.astype(str).apply(lambda text: analyzer.polarity_scores(text)['compound'])
    
    def score_to_label(score):
        if score >= 0.05: return 'POSITIVE'
        elif score <= -0.05: return 'NEGATIVE'
        else: return 'NEUTRAL'
            
    labels = scores.apply(score_to_label)
    return labels, scores

def _analyze_sentiment_roberta(text_series: pd.Series, progress_bar) -> tuple[pd.Series, pd.Series]:
    """Analyzes sentiment using the more accurate RoBERTa model with a progress bar."""
    roberta_model = load_roberta_model()
    
    results = []
    text_list = text_series.astype(str).to_list()
    
    # Use tqdm to iterate with a progress bar
    for i, text in enumerate(tqdm(text_list, desc="Analyzing with RoBERTa")):
        try:
            # Process one by one for better feedback
            result = roberta_model(text, truncation=True, max_length=512, padding=True)
            results.extend(result)
        except Exception as e:
            # Handle potential errors on a single text
            results.append({'label': 'NEUTRAL', 'score': 0.0})
        
        # Update the Streamlit progress bar
        progress_bar.progress((i + 1) / len(text_list), text=f"Analyzing article {i+1}/{len(text_list)}")

    labels = [res['label'].upper() for res in results]
    
    def result_to_score(res):
        if res['label'].lower() == 'positive': return res['score']
        elif res['label'].lower() == 'negative': return -res['score']
        return 0.0
        
    scores = [result_to_score(res) for res in results]
    
    return pd.Series(labels), pd.Series(scores)


def analyze_sentiment(text_series: pd.Series, model_choice: str, progress_bar=None) -> tuple[pd.Series, pd.Series]:
    """Main function to route analysis to the chosen model."""
    print(f"Performing sentiment analysis with '{model_choice}' model...")
    if model_choice == 'Fast (VADER)':
        return _analyze_sentiment_vader(text_series)
    elif model_choice == 'Deep (RoBERTa)':
        # Pass the progress bar to the roberta function
        return _analyze_sentiment_roberta(text_series, progress_bar)
    else:
        return _analyze_sentiment_vader(text_series)