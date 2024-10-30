import math
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm
import streamlit as st

# title the plot
st.write("Black Scholes is cool!")

# getting user inputs for option parameters
stockPrice = st.number_input("Enter Current Stock Price",value=None)
strikePrice = st.number_input("Enter Option Strike Price", value=None)
timeExp = st.number_input("Enter Time to Maturity(In Years)",value=None)
volatility = st.number_input("Enter Volatility",value=None)
riskFree = st.number_input("Enter Risk Free Rate",value=None)

# input desired purchase price for call and desired purchase price for put
st.write("Define desired call and put purchase price")
put_desired = st.number_input("Enter desired put price", value = None)
call_desired = st.number_input("Enter desired call price", value = None)
# Adding more input fields for stock price and volatility ranges
if stockPrice and volatility:
    st.write("Define ranges for stock price and volatility heatmaps")
    stock_low = st.number_input("Enter lower bound for stock price range", value = stockPrice * 0.8)
    stock_high = st.number_input("Enter upper bound for stock price range", value = stockPrice * 1.2)
    volatility_low = st.number_input("Enter lower bound for volatility range", value = volatility * 0.5)
    volatility_high = st.number_input("Enter upper bound for volatility range", value = volatility * 1.5)

# black scholes funtion which takes inputs and calculates values
def blackScholes(r, S, K, T, sigma, option_type):
    d1 = (math.log(S/K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - (sigma * math.sqrt(T))

    callPrice = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    putPrice = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return [float(callPrice), float(putPrice)]
if stockPrice and strikePrice and timeExp and riskFree and volatility and stock_low and stock_high and volatility_low and volatility_high and put_desired and call_desired:
    result = blackScholes(riskFree, stockPrice, strikePrice, timeExp, volatility, 'C') 
    st.write("Call Price: ", round(result[0]))
    st.write("Put Price: ", round(result[1]))

    # generate heatmap for call and put prices

    # step 1 - define ranges for stock price and volatility for the heatmap.
    # these ranges have values that 
    stock_prices = np.linspace(stockPrice * 0.8, stockPrice * 1.2, 50)
    volatilities = np.linspace(volatility * 0.5, volatility * 1.5, 50)

    # create arrays columns of the correct dimensions of stock prices and volatilites 
    call_prices = np.zeros((len(stock_prices), len(volatilities)))
    put_prices = np.zeros((len(stock_prices), len(volatilities)))

    # calculate option prices for each combination of stock price and volatility
    # outer loop iterates through stock prices with var S
    for i, S in enumerate(stock_prices):
        # inner loop iterates through volatilties with var sigma
        for j, sigma in enumerate(volatilities):
            # calculate blackScholes value
            call, put = blackScholes(riskFree, S, strikePrice, timeExp, sigma, 'C')
            # store call and put in respective matrices
            call_prices[i, j] = call
            put_prices[i, j] = put
    
    # create dataframe for heatmap visualization
    call_df = pd.DataFrame(call_prices, index = stock_prices, columns = volatilities)
    put_df = pd.DataFrame(put_prices, index=stock_prices, columns=volatilities)

    col1, col2 = st.columns(2)
    with col1:
        # plot the first heatmap for call prices
        st.subheader("Call Option Prices Heatmap")
        fig, ax = plt.subplots(figsize = (10,8))
        sns.heatmap(call_df, cmap = "RdYlGn", ax = ax, annot = False)
        ax.set_title("Call Option Price vs Stock Price and Volatility")
        ax.set_xlabel("Volatility")
        ax.set_ylabel("Stock Price")
        st.pyplot(fig)
    with col2:
        # Plot the heatmap for put prices
        st.subheader("Put Option Prices Heatmap")
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(put_df, cmap="RdYlGn", ax=ax, annot=False)
        ax.set_title("Put Option Price vs Stock Price and Volatility")
        ax.set_xlabel("Volatility")
        ax.set_ylabel("Stock Price")
        st.pyplot(fig)


    # Generate heatmaps for Profit and Loss for call and put prices

    # define the ranges for the stock price and volatility for heatmap
    stock_prices = np.linspace(stock_low, stock_high, 50)
    volatilities = np.linspace(volatility_low, volatility_high, 50)

    # create arrays for the dimensions of stock prices and volatilities
    call_pnl = np.zeros(len(stock_prices), len(volatilities))
    put_pnl = np.zeros(len(stock_prices), len(volatilities))

    # calculate option prices and PNL for each combination of stock price and volatility
    for i, S in enumerate(stock_prices):
        for j, sigma in enumerate(volatilities):
            # calculate black scholes value for call and put options
            call, put = blackScholes(riskFree, S, strikePrice, timeExp, sigma, 'C')
            # Calculate PNL for call and put options
            call_pnl[i,j] = call - call_desired
            put_pnl[i,j] = put - put_desired
    
    # after populating values, create dataframes for PNL heatmap visualization
    call_pnl_df = pd.DataFrame(call_pnl, index = stock_prices, columns = volatilities)
    put_pnl_df = pd.DataFrame(put_pnl, index = stock_prices, columns = volatilities)

    # define columns
    col1, col2 = st.columns(2)
    # make plots
    with col1:
        st.subheader("Call Option PNL Heatmap")
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(call_pnl_df, cmap = "RdYlGn", ax=ax, annot=False, center = 0)
        ax.set_title("Call Option PNL vs Stock Price and Volatility")
        ax.set_xlabel("Volatility")
        ax.set_ylabel("Stock Price")
        st.pyplot(fig)
    with col2:
        st.subheader("Put Option PNL Heatmap")
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(put_pnl_df, cmap = "RdYlGn", ax = ax,annot = False, center = 0)
        ax.set_title("Put Option PNL vs Stock Price and Volatility")
        ax.set_xlabel("Volatility")
        ax.set_ylabel("Stock Price")
        st.pyplot(fig)

