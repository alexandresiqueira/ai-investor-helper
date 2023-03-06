# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 21:33:07 2023

@author: ccgov
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow import keras
import seaborn as sns
import os
from datetime import datetime

import warnings
warnings.filterwarnings("ignore")


from sklearn.preprocessing import MinMaxScaler
import constants

ativo = "WIN@N"
n_steps = 50
train_split=.8



def read_data(plot=True):
    data = pd.read_csv(constants.DATA_PATH_STOCKS+ativo+'.csv', sep=';')
    #print(data.shape)
    #print(data.sample(7))
    
    #data.info()
    
    data['date'] = pd.to_datetime(data['data'], format='%Y%m%d')
    
    data = data.loc[(data['date'] > datetime(2021,1,1))
                            & (data['date']<datetime(2023,1,1))]
    
    #data.info()
    
    
    
    #data['date'] = pd.to_datetime(data['date'])
    # date vs open
    # date vs close
    """
    plt.figure(figsize=(15, 8))
    for index, company in enumerate(companies, 1):
    	plt.subplot(3, 3, index)
    	c = data[data['Name'] == company]
    	plt.plot(c['date'], c['close'], c="r", label="close", marker="+")
    	plt.plot(c['date'], c['open'], c="g", label="open", marker="^")
    	plt.title(company)
    	plt.legend()
    	plt.tight_layout()
    """
    
    
    
    apple = data[data['ativo'] == ativo]
    if plot:
        prediction_range = apple.loc[(apple['date'] > datetime(2021,1,1))
        & (apple['date']<datetime(2022,1,1))]
        plt.figure(figsize=(29, 4))
        plt.plot(apple['date'],apple['close'])
        plt.xlabel("Date")
        plt.ylabel("Close")
        plt.title(f"{ativo} Stock Prices")
        plt.show()

    return apple


def split_data(dataset, training, scaled_data):
    
    
    train_data = scaled_data[0:int(training), :]
    
    
    # prepare feature and labels
    x_train = []
    y_train = []
    
    for i in range(n_steps, len(train_data)):
    	x_train.append(train_data[i-n_steps:i, 0])
    	y_train.append(train_data[i, 0])
    
    x_train, y_train = np.array(x_train), np.array(y_train)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train


def create_model(x_train, y_train):
    model = keras.models.Sequential()
    model.add(keras.layers.LSTM(units=64,
    							return_sequences=True,
    							input_shape=(x_train.shape[1], 1)))
    model.add(keras.layers.LSTM(units=64))
    model.add(keras.layers.Dense(32))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(1))
    model.summary
    #print(model.summary)
    model.summary()
    
    
    model.compile(optimizer='adam',
    			loss='mean_squared_error')
    history = model.fit(x_train,
    					y_train,
    					epochs=10)
    return model





def test_model(stock_data, dataset, scaled_data, training, scaler, model):
    test_data = scaled_data[training - n_steps:, :]
    x_test = []
    y_test = dataset[training:, :]
    for i in range(n_steps, len(test_data)):
    	x_test.append(test_data[i-n_steps:i, 0])
    
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    
    # predict the testing data
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    
    # evaluation metrics
    mse = np.mean(((predictions - y_test) ** 2))
    print("MSE", mse)
    print("RMSE", np.sqrt(mse))



    train = stock_data[:training]
    test = stock_data[training:]
    test['Predictions'] = predictions
    
    plt.figure(figsize=(29, 16))
    plt.plot(train['close'])
    plt.plot(test[['close', 'Predictions']])
    plt.title(f'{ativo} Stock Close Price')
    plt.xlabel('Date')
    plt.ylabel("Close")
    plt.legend(['Train', 'Test', 'Predictions'])



def main():
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    stock_data = read_data()
    close_data = stock_data.filter(['close'])
    dataset = close_data.values
    training = int(np.ceil(len(dataset) * train_split))
    
    print(training)

    scaled_data = scaler.fit_transform(dataset)
    
    x_train, y_train = split_data(dataset, training, scaled_data)
    
    
    modelo = create_model(x_train, y_train)
    
    test_model(stock_data, dataset, scaled_data, training, scaler, modelo)
    

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()            