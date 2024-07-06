# Stock Analyzer Bot

This is a stock analyzing application that uses OpenAI's GPT-4o model to analyze stock data. Stock data is fetched using Polygon.io. The frontend is made in Streamlit, and the application is deployed on an AWS EC2 instance.

You can ask questions such as, "What is Apple's stock price for the last 1 year?" The response will include a summary of the stock and a plot of the stock price trend.


## Setup

### Prerequisites
- Python 3.10
- Git

### Steps to Run the Application

1. **Clone the repository:**
    ```bash
    git clone https://github.com/anubhav-think/StockAnalyzerBot.git
    ```

2. **Navigate to the project directory:**
    ```bash
    cd StockAnalyzerBot
    ```

3. **Create a virtual environment:**
    ```bash
    python3.10 -m venv venv
    ```

4. **Activate the virtual environment:**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS and Linux:
        ```bash
        source venv/bin/activate
        ```

5. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Usage

Once the application is running, you can interact with the chatbot to ask questions about stock prices. For example:
- "What is Apple's stock price for the last 1 year?"

The application will provide a summary of the stock and display a plot of the stock price trend.


## Acknowledgments
- [OpenAI](https://www.openai.com/) for the GPT-4 model.
- [Polygon.io](https://polygon.io/) for stock data.
- [Streamlit](https://streamlit.io/) for the frontend framework.
