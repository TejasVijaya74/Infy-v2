# analysis/forecasting.py

import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly
import config

def forecast_sentiment(df: pd.DataFrame):
    """
    Uses Prophet to forecast sentiment trends based on historical data.

    Args:
        df (pd.DataFrame): DataFrame containing 'publishedAt' and 'sentiment_score' columns.

    Returns:
        tuple: A tuple containing the Prophet model and the forecast DataFrame.
    """
    print("Generating forecast...")

    # Prophet requires columns to be named 'ds' (datestamp) and 'y' (value)
    prophet_df = df[['publishedAt', 'sentiment_score']].rename(
        columns={'publishedAt': 'ds', 'sentiment_score': 'y'}
    )

    # --- FIX: Remove timezone information from the 'ds' column ---
    prophet_df['ds'] = prophet_df['ds'].dt.tz_localize(None)

    # Initialize and fit the model
    model = Prophet(daily_seasonality=True)
    model.fit(prophet_df)

    # Create a dataframe for future predictions
    future = model.make_future_dataframe(periods=config.FORECAST_DAYS)
    forecast = model.predict(future)

    print("Forecast complete.")
    return model, forecast