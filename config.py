# config.py

import streamlit as st

# --- API KEYS ---
# This code securely loads your keys from Streamlit's secrets manager (secrets.toml)
# This prevents your secret keys from being exposed in your code.
try:
    NEWS_API_KEY = st.secrets["NEWS_API_KEY"]
    SLACK_WEBHOOK_URL = st.secrets["SLACK_WEBHOOK_URL"]
except (KeyError, FileNotFoundError):
    # This handles the case where secrets are not yet configured, preventing an error
    NEWS_API_KEY = ""
    SLACK_WEBHOOK_URL = ""


# --- REMOVED PROJECT PARAMETERS ---
# KEYWORDS_TO_TRACK and DEFAULT_KEYWORDS are no longer needed here because
# the app now uses a dynamic text box for user input.


# --- ANALYSIS THRESHOLDS ---
POSITIVE_ALERT_THRESHOLD = 0.8
NEGATIVE_ALERT_THRESHOLD = -0.5

# --- FORECASTING PARAMETERS ---
FORECAST_DAYS = 14