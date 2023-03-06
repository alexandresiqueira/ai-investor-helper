# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 21:23:47 2023

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import numpy as np
import pandas as pd
import ta
import os.path
import constants
import linear_regression_indicator as lri
import time
import coletor_b3
import ai_investor_b3_trainner as trainner

#funcao responsavel por ler o arquivo e extrair os dados
def read_data(file, path=constants.DATA_PATH_STOCKS):
    colsnames = ['data', 'time', 'open', 'high', 'low', 'close', 'tickvol', 'volume','spread']      
    try:
        print("Carregando arquivo MT5:", file)
        df = pd.read_csv(path+file, sep='\t', names=colsnames, skiprows=1)
        
    except UnicodeDecodeError:
        print("Carregando arquivo MT5 - ISO-8859-1:", file)
        df = pd.read_csv(path+file, sep='\t', names=colsnames, skiprows=1, encoding="ISO-8859-1")
        
    return df

def read_mt5_file_and_convert(ativo, path_stocks):

    df = read_data('WIN@N_M5_202101040900_202302241830.csv','C:\\Users\\ccgov\\Documents\\Pessoal\\Demo\\')
    df['data'] = df['data'].str.replace( '\.', '', regex=True)
    df['time'] = df['time'].str.replace( '\:', '', regex=True)
    df['data'] = df['data'] +"."+df['time']  
    df['data'] = df['data'].astype(float)

    df = df.drop(['time','tickvol','spread'], axis=1)

    df['ativo'] = ativo
    
    df = df[['data', 'ativo', 'open', 'high', 'low', 'close',  'volume']]
    fname = path_stocks+ativo+".csv"
    print("saving:", fname)
    df.to_csv(fname, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)


def generate_indicators(ativo):
    dfAtivo = coletor_b3.read_stock_indicator_file(ativo)
    for applyNormalization in constants.NORMALIZE_OPTIONS:
        dfAtivo = coletor_b3.calculate_indicators(dfAtivo, applyNormalization)
        #print(dfAtivo.tail(1))
        fileOut = coletor_b3.get_file_name_stock_indicator(ativo, applyNormalization)
            
    
        dfAtivo.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
    

def convert_date_time_to_float(ativo, normalized):
    fileOut = constants.DATA_PATH_STOCKS+ativo+"-ind.csv"
    if normalized:
        fileOut = constants.DATA_PATH_STOCKS+ativo+"-log-ind.csv"
    df = pd.read_csv(fileOut, sep=constants.CSV_SEPARATOR)
    df['data'] = (df['data'].str.replace( '\.', '', regex=True).replace( '\:', '', regex=True).replace( ' ', '.', regex=True)).astype(float)
    df.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
    print(df['data'].head(1))

def calc_results(ativo, normalized, targetTakeProfit, targetStopLoss):
    stocks = trainner.read_data_file_stock(ativo, normalized)
    
    stocks = stocks.loc[(stocks['data']%1 < 0.1625)]#remove os candles após às 16:25
    
    for atrib in constants.ATRIBS_RES:
        for per in constants.PERIODS_RESULTS:
            stocks = stocks.drop(atrib+"-"+str(per), axis=1)
    #stocks = coletor_b3.read_stock_indicator_file("PETR4",constants.DATA_PATH_STOCKS)
    stocks = stocks.dropna()
    qtDados = len(stocks.index);
    #stocks["operacao"] = "neutra"
    
    stocks["res-positive-20"] = "neutra"
    stocks["res-perc-20"] = 0.0
    stocks["res-20"] = 0 #targetTakeProfit
    
    for i in range(qtDados):        

        closePrice = stocks["close-orig"].iloc[i]
        #print("data:", str(stocks["data"].iloc[i+lenDataPlot-1]), ";close:", closePrice, ";down:",(closePrice - 2*targetDif), ";up:",(closePrice + 2*targetDif))
        day_trade = stocks["data"].iloc[i].astype(int)
        oper = "neutra"
        resOper = 0
        tryCompra = True
        tryVenda  = True
        for j in range( 7 * 12 + 5): #máximo de candles de 5 minutos das 09 às 16:25
            pos = i+j+1
            if pos >= qtDados:
                break
            if stocks["data"].iloc[pos].astype(int) != day_trade:
                break
            #print(">>data:",stocks["data"].iloc[pos], ";low:", stocks["low"].iloc[pos], ";high:",stocks["high"].iloc[pos])
            if stocks["low"].iloc[pos] <= (closePrice - targetStopLoss): 
                #print("LOSS COMPRA-" + str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["low"].iloc[pos]))
                tryCompra = False
            if stocks["high"].iloc[pos] >= (closePrice + targetStopLoss): 
                #print("LOSS VENDA-" + str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["high"].iloc[pos]))
                tryVenda = False
            if tryVenda:
                if stocks["low"].iloc[pos] <= (closePrice - targetTakeProfit): 
                    oper = "venda" #+ str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["low"].iloc[pos])
                    break
            if tryCompra:
                if stocks["high"].iloc[pos] >= (closePrice + targetTakeProfit): 
                    oper = "compra" #+ str(stocks["data"].iloc[pos]) +";preço:"+str(stocks["high"].iloc[pos])
                    break
        #stocks["operacao"].iloc[i] = oper
        stocks["res-positive-20"].iloc[i]   = oper
        if oper != "neutra":
            stocks["res-perc-20"].iloc[i]   = 100*targetTakeProfit/closePrice
            stocks["res-20"].iloc[i]        = targetTakeProfit/5 #cada ponto vale R$ 0,20
        #if i > 50:
         #   break
    fileOut = constants.DATA_PATH_STOCKS+ativo+"-ind.csv"
    if normalized:
        fileOut = constants.DATA_PATH_STOCKS+ativo+"-log-ind.csv"
    stocks.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)

    print(stocks[["close-orig","res-positive-20","res-20","res-perc-20"]].head(50))




ativo = "WIN@N"


#print()
#read_mt5_file_and_convert(ativo, path_stocks=constants.DATA_PATH_STOCKS)
#print("Gerando indicadores...")
#generate_indicators(ativo)
#print("Calculando resultados...")
#calc_results(ativo, normalized=False, targetTakeProfit=300, targetStopLoss=200)
print("Treinando resultados...")

trainner.create_classifiers()
trainner.train_test_ativo(ativo)

#convert_date_time_to_flat(ativo)
