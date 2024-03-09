# -*- coding: utf-8 -*-
"""Stock_Volume.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BNJ-cwdT4tfOhKCuDo_91I-H0Igbz9Xt
"""

import yfinance as yf
from datetime import datetime,timedelta
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

sto='^NSEI'

start_date=datetime.now()-timedelta(days=500)
end_date=datetime.now()-timedelta(days=5)

stock_data=yf.download(sto,start=start_date,end=end_date)

stock_data.head()

data=pd.DataFrame(stock_data)
datanew=data.iloc[:,[0,4,-1]]
datanew.head()

datanew['avg vol']=datanew['Volume'].shift(1).rolling(window=3).mean()
datanew=datanew.dropna().reset_index(drop=True)

datanew

datan=datanew[datanew['Volume']!=0]

datan.shape

datan['next close']=datan['Adj Close'].shift(-1)
datan=datan.dropna().reset_index(drop=True)

datan

datan['result']=(datan['Volume']>datan['avg vol'])&(datan['next close']>datan['Adj Close'])

datan

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Layer,Input
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from tensorflow.keras.optimizers import Adam

model=Sequential()
model.add(Dense(10,input_dim=3,kernel_initializer='uniform',activation='sigmoid'))
model.add(Dense(1,kernel_initializer='uniform',activation='sigmoid'))
optimizer=Adam(learning_rate=0.001)
model.compile(optimizer=optimizer,loss='binary_crossentropy',metrics=['accuracy'])

x=datan.iloc[:,[1,2,3]]
y=datan.iloc[:,5]

xtest,xtrain,ytest,ytrain=train_test_split(x,y,test_size=0.20)

history=model.fit(xtrain,ytrain,validation_data=(xtest,ytest),epochs=20,batch_size=20)
plt.plot(history.history[ "accuracy" ])
plt.plot(history.history[ "val_accuracy" ])
plt.title( "model accuracy" )
plt.ylabel( "accuracy" )
plt.xlabel( "epoch" )
plt.legend([ "train" , "test" ], loc= "upper left" )
plt.show()
# summarize history for loss
plt.plot(history.history[ "loss" ])
plt.plot(history.history[ "val_loss" ])
plt.title( "model loss" )
plt.ylabel( "loss" )
plt.xlabel( "epoch" )
plt.legend([ "train" , "test" ], loc= "upper left" )
plt.show()

scores = model.evaluate(xtest, ytest)
print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))