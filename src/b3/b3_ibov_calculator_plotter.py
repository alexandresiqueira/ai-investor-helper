# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 22:04:55 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import pandas as pd
import matplotlib.pyplot as plt
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants
import ta

PATH_B3_INDICES_LOCAL = "D:/data/b3/indices/"

pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 4)
pd.set_option('display.width', 1000)

def plot_ibov_win(date, fator, is_plot_diff=False, time_init=101500, time_end=180500):
    
    data    = pd.read_csv(PATH_B3_INDICES_LOCAL+date+"-ibov.csv", 
                 sep=constants.CSV_SEPARATOR, encoding='utf-8')
    atrib = "IBOV"
    if is_plot_diff:
        atrib   = "PERC"
        
    data    = data.loc[(data["TIME"] > time_init)  & (data["TIME"] < time_end)]
    n_per           = data["IBOV"].count() #50000
    if fator == None:
        fator           = int(data["DIF"].mean())
    data["WIN"]     = data["WIN"] - fator 
    trend_ema       = ta.trend.EMAIndicator(close=data[atrib], window=2000)
    data["EMA"]     = trend_ema.ema_indicator()
    qt = int(data.shape[0]/n_per)
    qt = 1
    for i in range(qt):
        plt.figure(figsize=(30, 16))
        plt.suptitle("Data:"+date+" Fator:"+str(fator))
        plt.grid(axis='y')
        plt.grid(axis='x')
        X = data["TIME"].index[i*n_per:((i+1)*n_per)] 
        X = pd.to_datetime(data['TIME'].iloc[i*n_per:((i+1)*n_per)], format='%H%M%S')
        if (is_plot_diff == False):
            Y = data["IBOV"].iloc[i*n_per:((i+1)*n_per)]
            W = data["WIN"].iloc[i*n_per:((i+1)*n_per)]
            plt.plot(X, Y, color='red')
            plt.plot(X, W)
        else:
            Z = data[atrib].iloc[i*n_per:((i+1)*n_per)]
            plt.plot(X,Z)
            ZE = data["EMA"].iloc[i*n_per:((i+1)*n_per)]
            plt.plot(X,ZE, color='green')
        
        plt.show()

    print(data.describe())




datas = ["20221124", "20221125","20221128", "20221129", "20221130", "20221201","20221202"]
def describe_files():
    for data in datas:    
        data = pd.read_csv(PATH_B3_INDICES_LOCAL+data+"-ibov.csv", 
                     sep=constants.CSV_SEPARATOR, encoding='utf-8')
        print(data.describe())
        
def main():
    data = "20221124"
    fator = 700
    for data in datas:  
        fator = fator - 100
        plot_ibov_win(data, fator, True)  
    #describe_files()    
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()