# -*- coding: utf-8 -*-
"""
Analisa os arquivos da B3 e gera arquivos com os dados de cada um dos ativos 
a serem analisados em arquivos com o nome <ativo>.csv

Caso já exista um arquivo com o nome <ativo>.csv no diretório de dados, não faz 
nova leitura do arquivo da B3.

Se o atributo applyNormalization for True, então, é gerado um arquivo 
<ativo>-log-ind.csv, no qual os dados open, high, low e close estão com valores
com valores calculados do logaritmo natural.

Created on Wed Oct 12 12:07:03 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import numpy as np
import pandas as pd
import ta
import os.path
import constants


#funcao responsavel por ler o arquivo e extrair os dados
def read_data(file):
    colspecs = [(0, 2), (2, 10), (12, 24), (24, 27), (56, 69), (69, 82),
                (82, 95), (108, 121) , (170, 188)]#posicao dos atributos desejados
    colsnames = ['tp-reg','data', 'ativo', 'tp-merc', 'open', 'high', 'low', 
                 'close', 'volume']      
    try:
        print("Carregando arquivo B3:", file)
        df = pd.read_fwf(constants.DATA_PATH+file, skiprows=0, skipfooter=0, colspecs=colspecs, 
                    names=colsnames, compression='zip')
        
    except UnicodeDecodeError:
        print("Carregando arquivo B3 - ISO-8859-1:", file)
        df = pd.read_fwf(constants.DATA_PATH+file, skiprows=0, skipfooter=0, colspecs=colspecs, 
                    names=colsnames, compression='zip', encoding="ISO-8859-1")
        
    return df

#Extrai os dados de um ativo do DataFrame obtido da B3
def extract_stock(df, ativo):
    df2 = df.loc[(df['ativo'] == ativo) & (df['tp-reg'] == 1)]

    df2 = df2.sort_values(by='data', axis=0, ascending=True, inplace=False, 
                          kind='quicksort', na_position='last')
    df2 = df2.drop('tp-merc', axis=1)
    df2 = df2.drop('tp-reg', axis=1)
    
    return df2    

#Calcula a diferença entre dois registros consecutivos da lista
"""
"""
def my_rolling_dif(x):
    return x.iloc[-1] - x.iloc[0]

#enriquece os dados com indicadores como: 
# - Média Móvel Simples - SMA
# - Média Móvel Exponecial - EMA
# - Bandas de Bollinger de Alta - BBH
# - Bandas de Bollinger de Alta Indicador - BBHI
# - Bandas de Bollinger de Baixa - BBL
# - Bandas de Bollinger de Baixa Indicador - BBLI
# - Índice de Força Relativa - RSI
# - Indicador de Força Verdadeira - TSI
# - Oscilador Estocástico - SO
# - Sinal do Oscilador Estocástico - SOS
# - MACD - MACD
# - Diferença MACD - MACD-DIFF
# - Sinal MACD - MACD-SIGNAL
# Cada um dos indicadores é calculado nos diversos períodos definidos no
#   vetor _periods, por exemplo, SMA-7, SMA-14, SMA-20, BBH-7, BBH-14,etc. 
# Além dos indicadores, são geradas informações de resultado entre o fechamento 
#   de um dia D e o fechamento de N dias posteriores:
# - res: diferença entre close de D e close de D+N
# - res-positive: True se res for positivo e False se res for negativo
# - res-perc: percentual referente a res/(close de D)    
# Esses três últimos atributos também são calculados para cada
def calculate_indicators(df, applyNormalization):

    df["close-orig"] = df["close"]
    if applyNormalization:
        print('>>>>>>>>>>>>>>>>>Normalizando os preços por LOGARITMO do ativo')
        df["open"] = np.log(df["open"])
        df["high"] = np.log(df["high"])
        df["low"] = np.log(df["low"])
        df["close"] = np.log(df["close"])
        
    
    for period in constants.PERIODS_INDICATORS:
        max_period = df['high'].rolling(period).max()
        min_period = df['low'].rolling(period).min()
        df["max-"+str(period)] = max_period
        df["min-"+str(period)] = min_period
        df["fibo-ret-"+str(period)] = ((df["close"] - min_period)/ 
                                       (max_period - min_period) ) * 100
        
    for period in constants.PERIODS_INDICATORS:
        trend_ma = ta.trend.SMAIndicator(close=df["close"], window=period)
        df["SMA-"+str(period)] = trend_ma.sma_indicator()
        df["SMA-dist-"+str(period)] = df["SMA-"+str(period)] - df["close"]

    for period in constants.PERIODS_INDICATORS:
        trend_ema = ta.trend.EMAIndicator(close=df["close"], window=period)
        df["EMA-"+str(period)] = trend_ema.ema_indicator()
        df["EMA-dist-"+str(period)] = df["EMA-"+str(period)] - df["close"]

    for period in constants.PERIODS_INDICATORS:
        trend_macd = ta.trend.MACD(close=df["close"], window_slow=period, 
                                   window_fast=period/2)
        df["MACD-"+str(period)] = trend_macd.macd()
        df["MACD-DIFF-"+str(period)] = trend_macd.macd_diff()
        df["MACD-SIGNAL-"+str(period)] = trend_macd.macd_signal()

    for period in constants.PERIODS_INDICATORS:
        rsi = ta.momentum.RSIIndicator(close=df["close"], window=period)
        df["RSI-"+str(period)] = rsi.rsi()

    for period in constants.PERIODS_INDICATORS:
        so = ta.momentum.StochasticOscillator(high=df["high"], low=df["low"], 
                                              close=df["close"], window=period)
        df["SO-"+str(period)] = so.stoch()
        df["SOS-"+str(period)] = so.stoch_signal()

    for period in constants.PERIODS_INDICATORS:
        tsi = ta.momentum.TSIIndicator(close=df["close"], window_slow=period, 
                                       window_fast=period/2)
        df.loc[:,"TSI-"+str(period)] = tsi.tsi()

    for period in constants.PERIODS_INDICATORS:
        bb = ta.volatility.BollingerBands(close=df["close"], window=period)
        df.loc[:,"BBH-"+str(period)] = bb.bollinger_hband()
        df.loc[:,"BBHI-"+str(period)] = bb.bollinger_hband_indicator()
        df.loc[:,"BBL-"+str(period)] = bb.bollinger_lband()
        df.loc[:,"BBLI-"+str(period)] = bb.bollinger_lband_indicator()

    for period in constants.PERIODS_RESULTS:
        diff = df['close-orig'].rolling(period).apply(my_rolling_dif)
        df.loc[:,"res-"+str(period)] = diff.shift(-1*period + 1)
        df.loc[:,"res-positive-"+str(period)] = (diff.shift(-1*period + 1) > 0).astype(str)
        df.loc[:,"res-perc-"+str(period)] = (df["res-"+str(period)]/df['close-orig'])*100

    return df

def read_sotck_file(fname):
    df = pd.read_csv(fname, sep=';')  
    return df

def read_stock_indicator_file(ativo):
    df = pd.read_csv(constants.DATA_PATH+ativo+".csv", sep=constants.CSV_SEPARATOR)  
    return df



###############################################################

def charge_b3_data(applyNormalization):
    dfGlobal = pd.Series(dtype=float)
    for ativo in constants.STOCKS:
        fname = constants.DATA_PATH+ativo+".csv"
        print("Processando Ativo:", ativo)
        if os.path.isfile(fname):
            dfAtivo = read_sotck_file(fname)
        else:
            if dfGlobal.size == 0:
                for year in range (constants.DATA_YEAR_INIT, constants.DATA_YEAR_END):
                    dfYear = read_data('COTAHIST_A'+str(year)+'.ZIP')
                    #print(dfYear.describe())
                    if dfGlobal.size == 0:
                        dfGlobal = dfYear
                    else:
                        dfGlobal = dfGlobal.append(dfYear)
    
                #dfGlobal = pd.concat([dfGlobal, df0, df1, df2])
            dfAtivo = extract_stock(dfGlobal, ativo)
            dfAtivo.to_csv(constants.DATA_PATH+ativo+".csv", sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
    
        df = calculate_indicators(dfAtivo, applyNormalization)
        #print(df)
        fileOut = constants.DATA_PATH+ativo+"-ind.csv"
        if applyNormalization:
            fileOut = constants.DATA_PATH+ativo+"-log-ind.csv"
            
    
        dfAtivo.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
        
#()
def main():

    charge_b3_data(applyNormalization = True)
    charge_b3_data(applyNormalization = False)

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    