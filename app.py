import streamlit as st
import chat

# Streamlit app
st.title("Stock Analyzer")
st.write("This is a stock analyzing application that uses OpenAI's gpt-4o model to analyze the stock data.\
         Stock data is fetched using Polygon.io. The frontend is made in streamlit and the application is deployed on AWS EC2 instance.\
         You can ask questions such as - What is Apple's stock price for the last 1 years . Response will be summary of the stock and a plot of stock price trend")
# Input from the user
user_message = st.text_input("Enter your query here:")

if user_message:
    # Process the message
    response, fig = chat.Anazlyze_stock(user_message)
    
    # Display the response
    st.write(response)
    
    # Display the graph
    st.pyplot(fig)
