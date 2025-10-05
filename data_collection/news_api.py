# data_collection/news_api.py

import pandas as pd
from newsapi import NewsApiClient
import config # Our custom configuration file

def fetch_news(query: str, page_size: int = 100) -> pd.DataFrame:
    """
    Fetches the latest news articles for a given query from the News API.

    Args:
        query (str): The search term for news articles (e.g., 'Nvidia').
        page_size (int): The number of articles to fetch. Max is 100.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the cleaned news data,
                      or an empty DataFrame if no articles are found.
    """
    print(f"Fetching news for query: '{query}'...")
    try:
        # Initialize the client with the API key from our config file
        newsapi = NewsApiClient(api_key=config.NEWS_API_KEY)

        # Fetch the articles
        all_articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='publishedAt', # Get the most recent articles first
            page_size=page_size
        )

        # Gracefully handle cases with no results
        if not all_articles['articles']:
            print(f"No articles found for '{query}'.")
            return pd.DataFrame()

        # Convert the list of articles into a pandas DataFrame
        df = pd.DataFrame(all_articles['articles'])

        # --- Data Cleaning ---
        # We only need a few columns for our dashboard
        df = df[['publishedAt', 'title', 'description', 'source', 'url']]
        # The 'source' column is a dictionary, so we extract just the name
        df['source'] = df['source'].apply(lambda s: s['name'])
        # Drop any rows that don't have a title or description
        df.dropna(subset=['title', 'description'], inplace=True)

        print(f"✅ Found {len(df)} relevant articles for '{query}'.")
        return df

    except Exception as e:
        print(f"An error occurred while fetching news: {e}")
        return pd.DataFrame()