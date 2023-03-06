# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 20:28:55 2023

@author: Alexandre Medeiros
"""

import pandas as pd
import matplotlib.pyplot as plt
import constants 
import coletor_b3
import time
import ai_investor_b3_trainner as trainner
import os.path

# DataFrame to represent opening , closing, high
# and low prices of a stock for a week
"""stock_prices = pd.DataFrame({'open': [36, 56, 45, 29, 65, 66, 67],
							'close': [29, 72, 11, 4, 23, 68, 45],
							'high': [42, 73, 61, 62, 73, 56, 55],
							'low': [22, 11, 10, 2, 13, 24, 25]},
							index=pd.date_range(
							"2021-11-10", periods=7, freq="d"))
"""
def plot_candle_stick_graph(stock_prices, fname=None):

    fig = plt.figure()
    
    # "up" dataframe will store the stock_prices
    # when the closing stock price is greater
    # than or equal to the opening stock prices
    up = stock_prices[stock_prices.close >= stock_prices.open]
    
    # "down" dataframe will store the stock_prices
    # when the closing stock price is
    # lesser than the opening stock prices
    down = stock_prices[stock_prices.close < stock_prices.open]
    
    # When the stock prices have decreased, then it
    # will be represented by blue color candlestick
    col1 = 'green'
    
    # When the stock prices have increased, then it
    # will be represented by green color candlestick
    col2 = 'red'
    
    # Setting width of candlestick elements
    width = .3
    width2 = .05
    
    # Plotting up prices of the stock
    plt.bar(up.index, up.close-up.open, width, bottom=up.open, color=col1)
    plt.bar(up.index, up.high-up.close, width2, bottom=up.close, color=col1)
    plt.bar(up.index, up.low-up.open, width2, bottom=up.open, color=col1)
    
    # Plotting down prices of the stock
    plt.bar(down.index, down.close-down.open, width, bottom=down.open, color=col2)
    plt.bar(down.index, down.high-down.open, width2, bottom=down.open, color=col2)
    plt.bar(down.index, down.low-down.close, width2, bottom=down.close, color=col2)
    
    plt.plot(stock_prices["BBH-20"])
    plt.plot(stock_prices["SMA-200"])
    plt.plot(stock_prices["EMA-20"])
    plt.plot(stock_prices["BBL-20"])
    #plt.plot(stock_prices["BBH-50"])
    #plt.plot(stock_prices["SMA-200"])
    #plt.plot(stock_prices["EMA-200"])
    #plt.plot(stock_prices["BBL-50"])
    
    # rotating the x-axis tick labels at 30degree
    # towards right
    plt.xticks(rotation=30, ha='right')
    plt.xticks([])
    plt.yticks([])
    plt.box(False)
    """
    fig.spines['top'].set_visible(False)
    fig.spines['right'].set_visible(False)
    fig.spines['bottom'].set_visible(False)
    fig.spines['left'].set_visible(False)
    """
    #plt.legend('', frameon=False)
    # displaying candlestick chart of stock data
    # of a week
    if (fname != None):
        print("Gravando:",fname)
        plt.savefig(fname)
        plt.close(fig)
    else:
        plt.show()

def getCandleStickFileName(stock, candle_start, tipo, quantCandles):
    
    fdir = constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/"+stock+"/"+tipo+"/"
    
    if not os.path.exists(constants.DATA_PATH_STOCKS+"/graphs/"):
        print("criou:", constants.DATA_PATH_STOCKS+"/graphs/")
        os.mkdir(constants.DATA_PATH_STOCKS+"/graphs/")
    if not os.path.exists(constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/"):
        print("criou:", constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/")
        os.mkdir(constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/")
    if not os.path.exists(constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/"+stock):
        print("criou:", constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/"+stock)
        os.mkdir(constants.DATA_PATH_STOCKS+"/graphs/"+str(quantCandles)+"/"+stock)
    if not os.path.exists(fdir):
        print("criou:", fdir)
        os.mkdir(fdir)
    fname = fdir + candle_start+".png"
    return fname




def save_figures_classifieds(ativo, normalized, quantCandles, percentTarget):
    stocks = trainner.read_data_file_stock(ativo, normalized)
    for atrib in constants.ATRIBS_RES:
        for per in constants.PERIODS_RESULTS:
            stocks = stocks.drop(atrib+"-"+str(per), axis=1)
    #stocks = coletor_b3.read_stock_indicator_file("PETR4",constants.DATA_PATH_STOCKS)
    stocks = stocks.dropna()
    qtDados = len(stocks.index);
    
    for i in range(qtDados-quantCandles):        
        sub_stocks = stocks.iloc[i:i+quantCandles]
        closePrice = stocks["close"].iloc[i+quantCandles-1]
        targetDif = closePrice * percentTarget
        #print("data:", str(stocks["data"].iloc[i+lenDataPlot-1]), ";close:", closePrice, ";down:",(closePrice - 2*targetDif), ";up:",(closePrice + 2*targetDif))
        oper = "neutra"
        tryCompra = True
        tryVenda  = True
        for j in range( quantCandles):
            pos = i+quantCandles+j-1
            if pos >= qtDados:
                break
            #print(">>data:",stocks["data"].iloc[pos], ";low:", stocks["low"].iloc[pos], ";high:",stocks["high"].iloc[pos])
            if stocks["low"].iloc[pos] <= (closePrice - targetDif): 
                #print("LOSS COMPRA-" + str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["low"].iloc[pos]))
                tryCompra = False
            if stocks["high"].iloc[pos] >= (closePrice + targetDif): 
                #print("LOSS VENDA-" + str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["high"].iloc[pos]))
                tryVenda = False
            if tryVenda:
                if stocks["low"].iloc[pos] <= (closePrice - 2*targetDif): 
                    oper = "venda" #+ str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["low"].iloc[pos])
                    break
            if tryCompra:
                if stocks["high"].iloc[pos] >= (closePrice + 2*targetDif): 
                    oper = "compra" #+ str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["high"].iloc[pos])
                    break
        #print(oper)
        fname = getCandleStickFileName(ativo, str(stocks["data"].iloc[i]), oper, quantCandles)
        #fname = None
        plot_candle_stick_graph(sub_stocks, fname)
        #if i > 2:
         #   break




def main():
    
    """
    for stock in constants.STOCKS:
        update_indicators(stock)
        """
    ativo = 'ITUB4'

    normalized = False;
    quantCandles = 20
    percentTarget = 0.03
    save_figures_classifieds(ativo, normalized, quantCandles, percentTarget)
    #stocks = stocks.loc[(stocks["data"] > 20230125) & (stocks["data"] < 20230208)]
    #print(stocks.describe())
    #plot_candle_stick_graph(stocks)
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    init = time.time()
    print(init)
    main()    
    end = time.time()
    print(end)
    print("elapsed seconds:", int(end - init))


