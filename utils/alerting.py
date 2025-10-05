# utils/alerting.py
import pandas as pd
import requests
import config

# --- STRATEGATEGIC KEYWORDS ---
STRATEGIC_KEYWORDS = {
    'partnership': 'Partnership/Alliance',
    'acquisition': 'Merger/Acquisition',
    'acquire': 'Merger/Acquisition',
    'merger': 'Merger/Acquisition',
    'launch': 'Product Launch',
    'release': 'Product Launch',
    'unveil': 'Product Launch',
    'lawsuit': 'Legal/Regulatory',
    'investigation': 'Legal/Regulatory',
    'regulatory': 'Legal/Regulatory',
    'funding': 'Financial',
    'investment': 'Financial',
}

def generate_alerts(df: pd.DataFrame) -> list:
    """
    Scans a dataframe of news articles and generates a list of strategic alerts.
    """
    if df.empty:
        return []

    print("Generating alerts...")
    alerts = []

    # --- 1. Keyword Alerts ---
    # Create a lowercased text column if it doesn't exist
    if 'full_text' not in df.columns:
        df['full_text'] = df['title'] + ". " + df['description'].fillna('')
        
    df['text_lower'] = df['full_text'].str.lower()
    
    for keyword, alert_type in STRATEGIC_KEYWORDS.items():
        # Find articles that contain the strategic keyword
        keyword_df = df[df['text_lower'].str.contains(keyword)]
        
        for index, row in keyword_df.iterrows():
            alerts.append({
                "timestamp": row['publishedAt'],
                "keyword": row.get('keyword', 'N/A'),
                "alert_type": alert_type,
                "headline": row['title'],
                "source": row['source'],
                "url": row.get('url', '#'),
                "sentiment": row.get('sentiment_label', 'N/A')
            })

    # --- 2. Sentiment Spike Alerts ---
    daily_sentiment = df.set_index('publishedAt').groupby(['keyword', pd.Grouper(freq='D')])['sentiment_score'].mean()
    sentiment_change = daily_sentiment.diff()
    spike_alerts = sentiment_change[abs(sentiment_change) > 0.5]
    
    for (keyword, timestamp), change in spike_alerts.items():
        change_type = "Positive Spike 🟢" if change > 0 else "Negative Spike 🔴"
        alerts.append({
            "timestamp": timestamp,
            "keyword": keyword,
            "alert_type": "Sentiment Spike",
            "headline": f"{change_type} of {change:.2f} in average sentiment.",
            "source": "Trend Analysis",
            "url": "#",
            "sentiment": "POSITIVE" if change > 0 else "NEGATIVE"
        })
    
    # Sort alerts by most recent first
    if alerts:
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)

    print(f"Found {len(alerts)} potential alerts.")
    return alerts


def send_slack_alert(message: str):
    """Sends a message to the configured Slack webhook."""
    if not config.SLACK_WEBHOOK_URL:
        print("Slack Webhook URL not set in config.")
        return

    payload = {"text": message}
    try:
        response = requests.post(config.SLACK_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            print(f"Slack alert sent successfully!")
        else:
            print(f"Failed to send Slack alert: {response.text}")
    except Exception as e:
        print(f"Slack alert error: {e}")