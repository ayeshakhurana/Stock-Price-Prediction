import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

model = load_model("Stock Prediction Model.keras")

st.header("Stock Market Sentiment Analysis & Predictor")
stock=st.text_input("Enter Stock Synbol","GOOG")
start='2015-01-01'
end='2025-03-01'

data=yf.download(stock,start,end)


st.subheader("Stock Data")
st.write(data)


st.subheader("ORIGINAL PRICE VS MOVING AVERAGE OF 50 DAYS")
ma_50=data.Close.rolling(50).mean()
fig1=plt.figure(figsize=(15,10))
plt.style.use('dark_background')
plt.plot(ma_50,'yellow')
plt.xlabel('Time',color='white')
plt.ylabel('Price',color='white')
plt.plot(data.Close,'purple')
st.pyplot(fig1)


st.subheader("ORIGINAL PRICE VS MOVING AVERAGE OF 50 DAYS VS MOVING AVERAGE 100 DAYS")
ma_100=data.Close.rolling(100).mean()
fig2=plt.figure(figsize=(15,10))
plt.style.use('dark_background')
plt.plot(ma_50,'b')
plt.plot(ma_100,'r')
plt.plot(data.Close,'g')
st.pyplot(fig2)

st.subheader("ORIGINAL PRICE VS MOVING AVERAGE OF 100 DAYS VS MOVING AVERAGE 200 DAYS")
ma_200=data.Close.rolling(200).mean()
fig3=plt.figure(figsize=(15,10))
plt.style.use('dark_background')
plt.plot(ma_100,'r')
plt.plot(ma_200,'yellow')
plt.plot(data.Close,'pink')
st.pyplot(fig3)


data_train=data.Close[0:int(len(data)*0.8)]
data_test=data.Close[int(len(data)*0.8): int(len(data))]

scaler=MinMaxScaler(feature_range=(0,1))
past100=data.Close.tail(100)
data_test=pd.concat([past100,data_train],ignore_index=True)
data_test_scale=scaler.fit_transform(data_test)

x=[]
y=[]
for i in range(100,len(data_test_scale)):
    x.append(data_test_scale[i-100:i])
    y.append(data_test_scale[i,0])

x,y=np.array(x),np.array(y)
y_pred=model.predict(x)
scale=1/scaler.scale_

y_pred=y_pred * scale
y=y * scale


st.header("OUTPUT")
st.subheader("ORIGINAL CLOSING PRICE VS PREDICTED CLOSING PRICE")
fig4=plt.figure(figsize=(35,25))
plt.style.use('dark_background')
plt.plot(y_pred,color='r',label='predicted price')
plt.plot(y,color='yellow',label='original price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.show()
st.pyplot(fig4)