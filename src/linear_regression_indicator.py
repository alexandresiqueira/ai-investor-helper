# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 19:05:20 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
import coletor_b3
import constants

pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
#pd.set_option('precision', 8)
pd.set_option('display.width', 1000)

def __rolling_log_reg(rol_df):
    linear_regressor = LinearRegression()
    X = rol_df.index[:].values.reshape(-1, 1)
    Y = rol_df[:].values.reshape(-1, 1)
    linear_regressor.fit(X, Y)
    return linear_regressor.coef_

def __read_data_example():
    PATH_B3_TIMESERIES_DAY = "D:/data/b3/timeseries/day/"
    PATH_B3_TIMESERIES_DAY = "../data/"
    
    data = pd.read_csv(PATH_B3_TIMESERIES_DAY+'PETR4.csv', sep=';')
    data = coletor_b3.calculate_indicators(data, False)
    data["data2"] = pd.to_datetime(data['data'], format='%Y%m%d')
    # print(data.head(5))
    data = data[["data", "data2", "close", "SMA-5",
                 "SMA-10", "SMA-20", "SMA-50", "SMA-200"]]
    """X = data["data"].iloc[:].values.reshape(-1, 1)
    X2 = data["data2"].iloc[:].values.reshape(-1, 1)
    Y = data["open"].iloc[:].values.reshape(-1, 1)
    """
    # X = data.iloc[:, 0].values.reshape(-1, 1) # values converts it into a numpy array
    # Y = data.iloc[:, 2].values.reshape(-1, 1) # -1 means that calculate the dimension of rows, but have 1 column
    data = data.dropna()
    return data

def __plot_linear_regression(data):
    
    linear_regressor = LinearRegression()
    for n_per in constants.PERIODS_INDICATORS:
    #n_per = 200
        plt_1 = plt.figure(figsize=(22, 9))
        plt.suptitle("N_PER:"+str(n_per))
        qt = int(data.shape[0]/n_per)
        #data["LN-"+str(n_per)] = data["SMA-"+str(n_per)]
        for i in range(qt):
            #data_
            X = data.index[i*n_per:((i+1)*n_per)].values.reshape(-1, 1)
            #X2 = data["data2"].iloc[:].values.reshape(-1, 1)
            #X = data["data"].iloc[i*n_per:((i+1)*n_per)].values.reshape(-1, 1)
            Y = data["SMA-"+str(n_per)].iloc[i*n_per:((i+1)*n_per)].values.reshape(-1, 1)
            linear_regressor.fit(X, Y)
            Y_pred = linear_regressor.predict(X)
            #data["LN-200"].iloc[i*n_per:((i+1)*n_per)] = Y_pred[:]
            plt.scatter(X, Y)
            plt.plot(X, Y_pred, color='red')
            print(linear_regressor.coef_)
            print("###")
            print(np.exp(linear_regressor.coef_))
            
            
        plt.show()
    

def lreg(data, window):
    lReg = data.rolling(window).apply(__rolling_log_reg)
    return lReg

def main():

    data = __read_data_example()
    for n_per in constants.PERIODS_INDICATORS:
        lReg = data["SMA-"+str(n_per)].rolling(n_per).apply(__rolling_log_reg)
        data["SMA-LREG-"+str(n_per)] = lReg
    
    print(data.tail(15))

    data = __read_data_example()
    for n_per in constants.PERIODS_INDICATORS:
        lReg = lreg(data["SMA-"+str(n_per)], n_per)
        data["SMA-LREG-"+str(n_per)] = lReg
    
    print(data.tail(15))


print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    