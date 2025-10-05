# app.py

import streamlit as st
import pandas as pd
import time
from datetime import datetime, timedelta
import plotly.graph_objects as go
from prophet.plot import plot_plotly

# --- Our Custom Modules ---
from data_collection import news_api
from analysis import sentiment
from analysis import forecasting
from analysis import synthesis
from utils import alerting
import config

# --- Page Configuration ---
st.set_page_config(
    page_title="Strategic Intelligence Dashboard", 
    page_icon="https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/chart-line.svg", 
    layout="wide"
)

# --- Page Title ---
st.title("Strategic Intelligence Dashboard")
st.text(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (IST)")

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

with st.sidebar.form(key='input_form'):
    st.subheader("Keywords & Competitors")
    keywords_input = st.text_area("Enter Keywords (comma-separated)", placeholder="e.g., Tesla, Microsoft, AI Regulation")
    st.subheader("Time Range")
    start_date = st.date_input("Start date", datetime.now() - timedelta(days=7))
    end_date = st.date_input("End date", datetime.now())
    st.subheader("Analysis Model")
    model_selection = st.sidebar.radio("Select Analysis Model", options=['Fast (VADER)', 'Deep (RoBERTa)'])
    submit_button = st.form_submit_button(label='Analyze')

selected_keywords = [keyword.strip() for keyword in keywords_input.split(',') if keyword.strip()]

# --- Data Loading (ONLY fetching, no analysis) ---
@st.cache_data
def load_data(keywords: tuple, start_dt, end_dt):
    """Fetches news data only, without analysis. This part is cached."""
    all_data = []
    for keyword in keywords:
        news_df = news_api.fetch_news(keyword)
        if not news_df.empty:
            news_df['keyword'] = keyword
            all_data.append(news_df)
    
    if not all_data: return pd.DataFrame()

    combined_df = pd.concat(all_data, ignore_index=True)
    combined_df['publishedAt'] = pd.to_datetime(combined_df['publishedAt'])
    mask = (combined_df['publishedAt'].dt.date >= start_dt) & (combined_df['publishedAt'].dt.date <= end_dt)
    filtered_df = combined_df.loc[mask].copy()
    return filtered_df

# --- Main App Logic ---
if submit_button and selected_keywords:
    # 1. Load data using the cached function
    data_df = load_data(tuple(selected_keywords), start_date, end_date)

    if not data_df.empty:
        # 2. Perform analysis in the main script with a live progress bar
        data_df['full_text'] = data_df['title'] + ". " + data_df['description'].fillna('')
        text_to_analyze = data_df['title'] if model_selection == 'Deep (RoBERTa)' else data_df['full_text']
        
        my_bar = st.progress(0, text="Analysis in progress. Please wait.")
        labels, scores = sentiment.analyze_sentiment(text_to_analyze, model_choice=model_selection, progress_bar=my_bar)
        my_bar.empty() # Remove the progress bar after completion

        data_df['sentiment_label'] = labels
        data_df['sentiment_score'] = scores
        
        # --- Display the rest of the dashboard ---
        alerts_list = alerting.generate_alerts(data_df)
        st.subheader("AI Executive Summary")
        with st.spinner("Synthesizing insights..."):
            summary_text = synthesis.generate_summary(data_df)
            st.info(summary_text)

        st.markdown("---")
        
        tab1, tab2, tab3 = st.tabs(["Live Benchmark", "Deep Dive Analysis", f"Alerts ({len(alerts_list)})"])

        with tab1:
            # (Tab 1 code remains the same)
            st.header(f"Live Sentiment Benchmark: {', '.join(selected_keywords)}")
            col_met1, col_met2 = st.columns([3, 1])
            with col_met1:
                st.subheader("Competitor Sentiment Trajectories")
                comparison_df = data_df.set_index('publishedAt').groupby(['keyword', pd.Grouper(freq='D')])['sentiment_score'].mean().unstack(level='keyword').fillna(0)
                st.line_chart(comparison_df)
            with col_met2:
                st.subheader("Overall Sentiment")
                sentiment_counts = data_df['sentiment_label'].value_counts()
                fig = go.Figure(data=[go.Pie(labels=sentiment_counts.index, values=sentiment_counts.values, hole=.4)])
                fig.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20, marker=dict(colors=['#28a745', '#dc3545', '#ffc107'], line=dict(color='#0E1117', width=2)))
                fig.update_layout(title_text="Sentiment Distribution", showlegend=True, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # (Tab 2 code remains the same)
            st.header(f"Deep Dive Analysis for '{selected_keywords[0]}'")
            forecast_data = data_df[data_df['keyword'] == selected_keywords[0]]
            if not forecast_data.empty:
                st.subheader(f"Predictive Forecast")
                prophet_model, forecast_df = forecasting.forecast_sentiment(forecast_data)
                fig_forecast = plot_plotly(prophet_model, forecast_df)
                fig_forecast.update_layout(title=f"Sentiment Forecast for the Next {config.FORECAST_DAYS} Days", xaxis_title="Date", yaxis_title="Predicted Sentiment Score")
                st.plotly_chart(fig_forecast, use_container_width=True)
                st.markdown("---")
                st.subheader("Filtered News Articles")
                st.dataframe(forecast_data[['publishedAt', 'keyword', 'title', 'source', 'sentiment_label', 'sentiment_score']].sort_values(by='publishedAt', ascending=False), use_container_width=True)
            else:
                st.warning(f"No data for '{selected_keywords[0]}' in the selected time range.")

        with tab3:
            # (Tab 3 code remains the same)
            st.header("Automated Alert History")
            alerts_df = pd.DataFrame(alerts_list)
            if not alerts_df.empty:
                for index, row in alerts_df.head(20).iterrows():
                    st.markdown(f"**{row['alert_type']}** | {row['keyword']} | {row['timestamp'].strftime('%Y-%m-%d')}")
                    st.markdown(f"[{row['headline']}]({row['url']})")
                    st.markdown(f"*Source: {row['source']}* | *Sentiment: {row['sentiment']}*")
                    st.markdown("---")
            else:
                st.success("No significant alerts found in the selected data.")

    else:
        st.warning("No data found for the selected keywords and time range.")

else:
    st.info("Please enter keywords and click 'Analyze' to begin.")