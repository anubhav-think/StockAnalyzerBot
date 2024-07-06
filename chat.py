import json
from openai import OpenAI
from langchain_openai import ChatOpenAI
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import requests

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
polygon_api_key = os.getenv('POLYGON_API_KEY')

llm=ChatOpenAI(temperature=0,
           model_name="gpt-4o",
           openai_api_key=openai_api_key)

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch stock data from Polygon API for a given ticker and date range.

    :param ticker: Stock ticker symbol (e.g., 'AAPL')
    :param start_date: Start date in YYYY-MM-DD format
    :param end_date: End date in YYYY-MM-DD format
    :return: Pandas Dataframe
    """
    url = f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{start_date}/{end_date}"
    params = {
        'adjusted': 'true',
        'sort': 'asc',
        'apiKey': polygon_api_key
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        df = pd.DataFrame(response.json()["results"])
        return df
    else:
        response.raise_for_status()
        return ""


function=[
        {
        "name": "get_company_Stock_ticker",
        "description": "This will get the stock ticker of the company",
        "parameters": {
            "type": "object",
            "properties": {
                "company_name": {
                    "type": "string",
                    "description": "This is the name of the company given in query",
                },
                "ticker_symbol": {
                    "type": "string",
                    "description": "This is the stock symbol of the company.",
                },
                "start_date": {
                    "type": "string",
                    "description": "This is the start date of the time window in YYYY-MM-DD format",
                },
                "end_date": {
                    "type": "string",
                    "description": "This is the end date of the time window in YYYY-MM-DD format",
                }
            },
            "required": ["company_name","ticker_symbol","start_date","end_date"],
        },
    }
]

def get_stock_ticker(query):
    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0,
            messages=[{
                "role":"user",
                "content":f"Given the user request, what is the comapany name, company stock ticker, start date and end date? start and end dates are the time window dates of the stock in in YYYY-MM-DD format. Today's date is 2024-07-05: {query}?"
            }],
            functions=function,
            function_call={"name": "get_company_Stock_ticker"},
    )

    arguments = json.loads(response.choices[0].message.function_call.arguments)
    company_name = arguments["company_name"]
    company_ticker = arguments["ticker_symbol"]
    start_date = arguments["start_date"]
    end_date = arguments["end_date"]
    return company_name,company_ticker,start_date,end_date

def Anazlyze_stock(query):
    #agent.run(query) Outputs Company name, Ticker
    Company_name,ticker,start_date,end_date=get_stock_ticker(query)
    print({"Query":query,"Company_name":Company_name,"Ticker":ticker, "start_date":start_date,"end_date":end_date})
    stock_data_df=fetch_stock_data(ticker,start_date, end_date)

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot(stock_data_df.index, stock_data_df['o'], marker='o', linestyle='-', label='Open')
    ax.plot(stock_data_df.index, stock_data_df['c'], marker='o', linestyle='-', label='Close')
    ax.plot(stock_data_df.index, stock_data_df['h'], marker='o', linestyle='-', label='High')
    ax.plot(stock_data_df.index, stock_data_df['l'], marker='o', linestyle='-', label='Low')
    ax.set_title(f'{Company_name} Stock Data ({start_date} to {end_date})')
    ax.set_xlabel('Days')
    ax.set_ylabel('Value')
    ax.grid(True)
    ax.legend()

    stock_data = stock_data_df.to_string()

    print("\n\nAnalyzing.....\n")
    analysis=llm(f"Give detail stock analysis, Use the available data and provide investment recommendation. \
             The user is fully aware about the investment risk, dont include any kind of warning like 'It is recommended to conduct further research and analysis or consult with a financial advisor before making an investment decision' in the answer \
             User question: {query} \
             You have the following information available about {Company_name}. Write (5-8) pointwise investment analysis to answer user query, At the end conclude with proper explaination.Try to Give positives and negatives  : \
                {stock_data}"
             )

    return analysis.content, fig