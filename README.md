# Strategic Intelligence Dashboard

A full-stack web application that transforms real-time market news into actionable strategic insights using AI. This dashboard provides competitor benchmarking, predictive forecasting, and automated alerting in a clean, interactive interface.

## Features

* **Live Data Pipeline**: Ingests real-time news from the News API for any user-defined keywords.

* **Dual AI Sentiment Analysis**: Users can choose between a fast VADER model for quick analysis or a more accurate, deep-learning RoBERTa model for in-depth sentiment scoring.

* **AI Executive Summary**: Utilizes a T5 summarization model to read all articles and generate a concise, human-readable summary of the key narratives.

* **Predictive Forecasting**: Integrates the Prophet library to forecast future sentiment trends based on historical data.

* **Automated Alerting**: Scans data for strategic keywords (e.g., "acquisition", "lawsuit") and significant sentiment shifts, displaying them in a dedicated alerts tab.

* **Interactive UI**: Built with Streamlit, featuring dynamic filters for keywords and time ranges, a multi-tab layout, and interactive charts for a professional user experience.

## Tech Stack

* **Frontend**: Streamlit

* **Backend/Analysis**: Python, Pandas

* **AI/ML**: Transformers (Hugging Face for RoBERTa & T5), Prophet (Forecasting), VADER

* **Data Source**: News API (via REST)

* **Plotting**: Plotly, Matplotlib/Seaborn

## Local Setup & Installation

Follow these steps to run the project on your local machine.

**1. Clone the repository:**


git clone https://github.com/TejasVijaya74/Infy-v2.git
cd Infy-v2


**2. Create and activate a virtual environment (recommended):**


python -m venv venv

On Windows
venv\Scripts\activate

On macOS/Linux
source venv/bin/activate


**3. Install the required packages:**


pip install -r requirements.txt


**4. Create your secrets file:**

* In the project root, create a folder named `.streamlit`.

* Inside `.streamlit`, create a file named `secrets.toml`.

* Add your API keys to this file:


NEWS_API_KEY = "YOUR_NEWS_API_KEY"
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL"


**5. Run the Streamlit app:**


streamlit run app.py


The application will open in your web browser.
