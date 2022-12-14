# -*- coding: utf-8 -*-
"""To get MACD crossover signal of stocks of NSE.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/100stE0phFSAplDMxip2ikaptuF5yJYUV
"""

pip install yfinance  ## installing yfinance

import yfinance as yf ## intalling required libraries 
import pandas as pd 
import datetime as dt
from pytz import timezone

date_time=dt.datetime.now(timezone("Asia/Kolkata"))  ## current time of india

date_time

d=yf.download("TCS.NS",period="1mo") ## to download price data of a stock

d

stocks=["TCS.NS","INFY.NS","PIDILITIND.NS","NAUKRI.NS","ASIANPAINT.NS","ABCAPITAL.NS","PIIND.NS","MINDACORP.NS","BAJAJFINSV.NS","BORORENEW.NS","ESCORTS.NS"] ## for getting data of multiple stocks

start=dt.datetime.today()-dt.timedelta(30)  # to get price data of last 30 days ,it can be more than 30 days 
end=dt.datetime.today()
cl_price=pd.DataFrame()
ohlcv_data={}

for ticker in stocks:
    cl_price[ticker]=yf.download(ticker,start,end)["Adj Close"]  ## to get  adjustive price of  slected stocks

for ticker in stocks :
    ohlcv_data[ticker]=yf.download(ticker,start,end)  ##  to get open-high-low-close-volume of selected stocks

ohlcv_data

cl_price

tickers=["TCS.NS","INFY.NS","PIDILITIND.NS","NAUKRI.NS","ASIANPAINT.NS","ABCAPITAL.NS","PIIND.NS","MINDACORP.NS","BAJAJFINSV.NS","BORORENEW.NS","ESCORTS.NS"] ## for getting data of multiple stocks 
o_data={}

for ticker in tickers:
    temp=yf.download(ticker,period="1mo",interval="15m")   ## to get data  of selected stocks for 1 months  at a interval of 15 minute
    temp.dropna(how="any",inplace=True)
    o_data[ticker]=temp

def MACD(DF,a=12,b=26,c=9):   ## MACD (moving average crossover divergence  )
    df=DF.copy()
    df["ma_fast"]=df["Adj Close"].ewm(span=a,min_periods =a).mean()
    df["ma_slow"]=df["Adj Close"].ewm(span=b,min_periods =b).mean()
    df["macd"]=df["ma_fast"]-df["ma_slow"]
    df["signal"]=df["macd"].ewm(span=c,min_periods=c).mean()
    return df.loc[:,["macd","signal"]]

for ticker in o_data:
    o_data[ticker][["MACD","SIGNAL"]]=MACD(o_data[ticker])

o_data # to get open-high-low-close-Adj close-volume-MACD-SIGNAL    ## to obtain MACD signal as final  output