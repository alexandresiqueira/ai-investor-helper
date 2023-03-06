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
import linear_regression_indicator as lri
import time

#funcao responsavel por ler o arquivo e extrair os dados
def read_data(file, path=constants.DATA_PATH_STOCKS):
    colspecs = [(0, 2), (2, 10), (12, 24), (24, 27), (56, 69), (69, 82),
                (82, 95), (108, 121) , (170, 188)]#posicao dos atributos desejados
    colsnames = ['tp-reg','data', 'ativo', 'tp-merc', 'open', 'high', 'low', 
                 'close', 'volume']      
    try:
        print("Carregando arquivo B3:", file)
        df = pd.read_fwf(path+file, skiprows=1, skipfooter=1, colspecs=colspecs, 
                    names=colsnames, compression='zip')
        
    except UnicodeDecodeError:
        print("Carregando arquivo B3 - ISO-8859-1:", file)
        df = pd.read_fwf(path+file, skiprows=1, skipfooter=1, colspecs=colspecs, 
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
# - Bandas de Bollinger Percentual - BBP
# - Índice de Força Relativa - RSI
# - Indicador de Força Verdadeira - TSI
# - Oscilador Estocástico - SO
# - Sinal do Oscilador Estocástico - SOS
# - MACD - MACD
# - Diferença MACD - MACD-DIFF
# - Sinal MACD - MACD-SIGNAL
# - ForceIndexIndicator - FI
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
    round_factor_0 = 0
    round_factor_2 = 2
    round_factor_4 = 4
    if applyNormalization:
        #print('>>>>>>>>>Normalizando os preços por LOGARITMO do ativo')
        df["open"] = np.log(df["open"])
        df["high"] = np.log(df["high"])
        df["low"] = np.log(df["low"])
        df["close"] = np.log(df["close"])
        round_factor_0 = 4
        round_factor_2 = 6
        round_factor_4 = 8

    for period in constants.PERIODS_INDICATORS:
        trend_ema = ta.trend.EMAIndicator(close=df["close"], window=period)
        df["EMA-"+str(period)] = round(trend_ema.ema_indicator(), round_factor_0)
        df["EMA-dist-"+str(period)] = df["EMA-"+str(period)] - df["close"]

    #for period in constants.PERIODS_INDICATORS:
        trend_macd = ta.trend.MACD(close=df["close"], window_slow=period, 
                                   window_fast=period/2)
        df["MACD-"+str(period)] = round(trend_macd.macd(), round_factor_2)
        df["MACD-DIFF-"+str(period)] = round(trend_macd.macd_diff(), round_factor_2)
        df["MACD-SIGNAL-"+str(period)] = round(trend_macd.macd_signal(), round_factor_2)

    #for period in constants.PERIODS_INDICATORS:
        rsi = ta.momentum.RSIIndicator(close=df["close"], window=period)
        df["RSI-"+str(period)] = round(rsi.rsi(), round_factor_2)

    #for period in constants.PERIODS_INDICATORS:
        so = ta.momentum.StochasticOscillator(high=df["high"], low=df["low"], 
                                              close=df["close"], window=period)
        df["SO-"+str(period)] = round(so.stoch(), round_factor_2)
        df["SOS-"+str(period)] = round(so.stoch_signal(), round_factor_2)

    #for period in constants.PERIODS_INDICATORS:
        tsi = ta.momentum.TSIIndicator(close=df["close"], window_slow=period, 
                                       window_fast=period/2)
        df.loc[:,"TSI-"+str(period)] = round(tsi.tsi(), round_factor_2)

    #for period in constants.PERIODS_INDICATORS:
        bb = ta.volatility.BollingerBands(close=df["close"], window=period)
        df.loc[:,"BBH-"+str(period)] = round(bb.bollinger_hband(), round_factor_0)
        df.loc[:,"BBHI-"+str(period)] = bb.bollinger_hband_indicator()
        df.loc[:,"BBL-"+str(period)] = round(bb.bollinger_lband(), round_factor_0)
        df.loc[:,"BBLI-"+str(period)] = bb.bollinger_lband_indicator()
        df.loc[:,"BBP-"+str(period)] = round(bb.bollinger_pband(), round_factor_4) #percentual da banda 
        
        #df.loc[:,"BBH-dist-"+str(period)] = df["BBH-"+str(period)] - df["close"]
        #df.loc[:,"BBL-dist-"+str(period)] = df["close"] - df["BBL-"+str(period)]
        df.loc[:,"BBH-BBL-dist-"+str(period)] = df["BBH-"+str(period)] - df["BBL-"+str(period)]
            
    #for period in constants.PERIODS_INDICATORS:
        fi = ta.volume.ForceIndexIndicator(close=df["close"], volume=df["volume"], window=period)
        df.loc[:,"FI-"+str(period)] = round(fi.force_index(), round_factor_0)
        
        """
        for period in constants.PERIODS_INDICATORS:
            obv = ta.volume.OnBalanceVolumeIndicator(close=df["close"], volume=df["volume"])
            df.loc[:,"OBV-"+str(period)] = obv.on_balance_volume()
    
        """
    #for period in constants.PERIODS_INDICATORS:
        max_period = df['high'].rolling(period).max()
        min_period = df['low'].rolling(period).min()
        df["max-"+str(period)] = max_period
        df["min-"+str(period)] = min_period
        df["fibo-ret-"+str(period)] = round(((df["close"] - min_period)/ 
                                       (max_period - min_period) ) * 100, round_factor_2)
        
    #for period in constants.PERIODS_INDICATORS:
        trend_ma = ta.trend.SMAIndicator(close=df["close"], window=period)
        a = pd.DataFrame(dtype=float)
        a["SMA-"+str(period)] = round(trend_ma.sma_indicator(), round_factor_0)
        a["SMA-dist-"+str(period)] = a["SMA-"+str(period)] - df["close"]
        #df = pd.concat([df,a], axis=1)
        
    #for period in constants.PERIODS_INDICATORS:
        #a = pd.DataFrame(dtype=float)
        a["SMA-LREG-"+str(period)] = round(lri.lreg(a["SMA-"+str(period)], period), round_factor_4)
        a["BBH-LREG-"+str(period)] = round(lri.lreg(df["BBH-"+str(period)], period), round_factor_4)
        a["BBL-LREG-"+str(period)] = round(lri.lreg(df["BBL-"+str(period)], period), round_factor_4)
        a["SO-LREG-"+str(period)] = round(lri.lreg(df["SO-"+str(period)], period), round_factor_4)
        df = pd.concat([df,a], axis=1)

        
    for period in constants.PERIODS_RESULTS:
        diff = df['close-orig'].rolling(period).apply(my_rolling_dif)
        df.loc[:,"res-"+str(period)] = diff.shift(-1*period + 1)
        df.loc[:,"res-positive-"+str(period)] = (diff.shift(-1*period + 1) > 0).astype(str)
        df.loc[:,"res-perc-"+str(period)] = round((df["res-"+str(period)]/df['close-orig'])*100, round_factor_2)
        
    return df

def __read_stock(stock):
    fname = constants.DATA_PATH_STOCKS+stock+".csv"
    #print("Processando Ativo:", ativo, ";LOGARITM:",applyNormalization)
    if os.path.isfile(fname):
        dfAtivo = read_sotck_file(fname)
    return dfAtivo


def __read_stock_indicators(stock, applyNormalization):
    fname = get_file_name_stock_indicator(stock, applyNormalization)
    #print("Processando Ativo:", ativo, ";LOGARITM:",applyNormalization)
    if os.path.isfile(fname):
        dfAtivo = pd.read_csv(fname, sep=constants.CSV_SEPARATOR)
    return dfAtivo



#def add_data(data, stock, open, high, low, close, volume):
def update_indicators(stock, path_stocks=constants.DATA_PATH_STOCKS):
    
    df          = __read_stock(stock)
    for applyNormalization in constants.NORMALIZE_OPTIONS:
        dfAtivoInd  = __read_stock_indicators(stock, applyNormalization)
        
        max_date    = (dfAtivoInd["data"].max())
        
        ##df = df.drop(len(df.index)-1, axis=0)####remover
        df_ = df.loc[df["data"] > max_date]
        if df_.shape[0] == 0:
            print("STOCK:", stock, ";NORMALIZE:", applyNormalization, " UPDATED ")
            continue
    
        periods = constants.PERIODS_INDICATORS.copy()
        periods.sort(reverse=True)
        dfN = df.loc[df.tail(2*periods[0] - 1).index].copy()
        dfN = calculate_indicators(dfN, applyNormalization)
        df_ = dfN.loc[dfN["data"] > max_date]
        dfAtivoInd  = dfAtivoInd.append(df_)
    
        fileOut = get_file_name_stock_indicator(stock, applyNormalization, path_stocks)
                
        dfAtivoInd.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
        print("saving ...:",fileOut)

def read_sotck_file(fname):
    df = pd.read_csv(fname, sep=';')  
    return df

def read_stock_indicator_file(ativo, path_stocks=constants.DATA_PATH_STOCKS):
    df = pd.read_csv(path_stocks+ativo+".csv", sep=constants.CSV_SEPARATOR)  
    return df

def get_file_name_stock_indicator(stock, applyNormalization, path_stocks=constants.DATA_PATH_STOCKS):
    fileOut = path_stocks+stock+"-ind.csv"
    if applyNormalization:
        fileOut = path_stocks+stock+"-log-ind.csv"
    return fileOut
###############################################################

def charge_b3_data(applyNormalization, path_stocks=constants.DATA_PATH_STOCKS, path_series=constants.DATA_PATH_SERIES):
    if not os.path.exists(path_stocks):
        os.mkdir(path_stocks)
    dfGlobal = pd.Series(dtype=float)
    for ativo in constants.STOCKS:
        fname = path_stocks+ativo+".csv"
        print("Processando Ativo:", ativo, ";LOGARITM:",applyNormalization)
        if os.path.isfile(fname):
            dfAtivo = read_sotck_file(fname)
        else:
            if dfGlobal.size == 0:
                for year in range (constants.DATA_YEAR_INIT, constants.DATA_YEAR_END):
                    dfYear = read_data('COTAHIST_A'+str(year)+'.ZIP', path_series)
                    #print(dfYear.describe())
                    if dfGlobal.size == 0:
                        dfGlobal = dfYear
                    else:
                        dfGlobal = dfGlobal.append(dfYear)
    
                #dfGlobal = pd.concat([dfGlobal, df0, df1, df2])
            dfAtivo = extract_stock(dfGlobal, ativo)
            dfAtivo.to_csv(path_stocks+ativo+".csv", sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
    
        dfAtivo = calculate_indicators(dfAtivo, applyNormalization)
        #print(dfAtivo.tail(1))
        fileOut = get_file_name_stock_indicator(ativo, applyNormalization, path_stocks)
            
    
        dfAtivo.to_csv(fileOut, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
        
#()
def main():
    
    for stock in constants.STOCKS:
        update_indicators(stock)
    """
    charge_b3_data(applyNormalization = True)
    charge_b3_data(applyNormalization = False)
    """
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    init = time.time()
    print(init)
    main()    
    end = time.time()
    print(end)
    print("elapsed seconds:", int(end - init))
    