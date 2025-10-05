# Strategic Intelligence Dashboard

A full-stack web application that transforms real-time market news into actionable strategic insights using AI.  
This dashboard provides competitor benchmarking, predictive forecasting, and automated alerting in a clean, interactive interface.
**[Live Demo](https://infy-v2.streamlit.app/)**

---

##  Features

- **Live Data Pipeline**: Ingests real-time news from the News API for any user-defined keywords.  
- **Dual AI Sentiment Analysis**: Choose between a fast **VADER** model for quick results or a **RoBERTa** model for deep-learning accuracy.  
- **AI Executive Summary**: Leverages **T5** to generate concise, human-readable summaries of key narratives.  
- **Predictive Forecasting**: Uses **Prophet** to forecast future sentiment trends.  
- **Automated Alerting**: Flags critical keywords (e.g., *acquisition*, *lawsuit*) and major sentiment shifts.  
- **Interactive UI**: Streamlit-based dashboard with filters, tabs, and interactive charts for a professional user experience.  

---

##  Tech Stack

- **Frontend**: Streamlit  
- **Backend/Analysis**: Python, Pandas  
- **AI/ML**: Hugging Face Transformers (RoBERTa, T5), VADER, Prophet  
- **Data Source**: News API (REST)  
- **Visualization**: Plotly, Matplotlib, Seaborn  

---

##  Local Setup & Installation

Follow these steps to run the project locally:

### 1️. Clone the repository
```bash
git clone https://github.com/TejasVijaya74/Infy-v2.git
cd Infy-v2
```

### 2️. Create & activate a virtual environment (recommended)

```bash
python -m venv venv
```

* On **Windows**:
```bash
venv\Scripts\activate
```

* On **macOS/Linux**:
```bash
source venv/bin/activate
```

### 3️. Install dependencies
```bash
pip install -r requirements.txt
```

### 4️. Configure secrets

* Create a folder named `.streamlit` in the project root.  
* Inside it, create a file named `secrets.toml`.  
* Add your API keys:
```toml
NEWS_API_KEY = "YOUR_NEWS_API_KEY"
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL"
```

### 5️. Run the Streamlit app
```bash
streamlit run app.py
```

The app will open automatically in your default browser.

---

##  Future Enhancements

* Add support for multiple news APIs  
* Advanced alerting via email/SMS integrations  
* More forecasting models for comparison  

---

##  Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

---

##  License

This project is licensed under the MIT License.

---

