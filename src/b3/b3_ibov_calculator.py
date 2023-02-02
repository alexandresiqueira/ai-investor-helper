# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 18:21:04 2022
Funcoes:
        1. load_composicao: Ler o arquivo que define a composicao do IBOV
        2. calc_ibov_win: Obtem os dados agregados diario e calcula o ibov intraday
                            baseado na composicao existente
        
@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

import numpy as np
import pandas as pd
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
from datetime import date
import datetime
import b3_intraday_organizer
import b3_downloader
np.set_printoptions(threshold=None, precision=4)
pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 4)
pd.set_option('display.width', 1000)



def __read_composicao_file(path=constants.DATA_PATH):
    file = "IBOVDia_01-12-22.csv"
    #file = 'IBOVQuad_9-2022.csv'
    df = pd.read_csv(path+file, 
                     header=1, sep=constants.CSV_SEPARATOR, encoding="ISO-8859-1")

    return df



def filter_serie(df_serie, data):
    df_serie = df_serie.loc[(df_serie["data"] == data)]
    return df_serie

#calcula o ibov de uma serie já filtrada conforme composicao
def calc_ibov(df_serie, composicao):
    if df_serie.shape[0] == 0:
        return None
    ibov = 0
    redutor = composicao["Tipo"].iloc[composicao.shape[0]-1] *100
    for i in range(composicao.shape[0]- 2):
        ativo = composicao.index[i]
        df = df_serie.loc[(df_serie["ativo"] == ativo)]
        if df.shape[0] == 0:
            print("ALERT: ATIVO NAO LOCALIZADO PARA CALCULO IBOV:",ativo)
            return ibov
        close = df.iloc[0]["close"]
        qtd = composicao.iloc[i]["Tipo"]
        ibov = ibov + (close * qtd  / redutor)

    return ibov

#Carrega a composicao IBOV e ajusta os dados numéricos
def load_composicao():
    
    df = __read_composicao_file(constants.PATH_B3_INDICES_LOCAL)
    df["Qtde. Teórica"] = (df["Qtde. Teórica"].str.replace(',','.')).astype(float)
    df["Tipo"] = (df["Tipo"].str.replace('.','', regex=False).str.replace(',','.')).astype(float)

    return df

#Agrega os dados de todos ativos por segundo
def agregate_intraday_second(data):
    df_intra    =  b3_intraday_organizer.read_intraday_file_full(data, 
                                b3_intraday_organizer.PATH_B3_INTRADAY_LOCAL)
    df          = b3_intraday_organizer.agregate_intraday_second(df_intra)
    return df

#calcula o ibv de fechamento dos últimos n_days na composicao informada
def calc_ibov_last_days(composicao, n_days=30):

    df_serie    = b3_downloader.read_last_serie()
    today       = date.today()
    start_date  = today + datetime.timedelta(days=-1*n_days)
    
    for int_day in range(n_days):
        
        date_   = (start_date + datetime.timedelta(days=int_day))
        data    = int(date_.strftime("%Y%m%d"))
        df      = filter_serie(df_serie, data)
        ibov    = calc_ibov(df, composicao)
        print(data,":",ibov)
    
def write_ibov_file(resDf, data):
    resDf.to_csv(constants.PATH_B3_INDICES_LOCAL+data+"-ibov.csv", 
         sep=constants.CSV_SEPARATOR, encoding='utf-8', index=True)

#Obtem os dados agregados diario e calcula o ibov baseado na composicao existente
def calc_ibov_win(data, cod_win, start_hour=100700):
    
    res_cols_names  = ["TIME", "ATIVO", "CLOSE", "IBOV", "WIN", "DIF", "PERC"]
    resDf           = pd.DataFrame([], columns = res_cols_names)
    composicao      = load_composicao()
    redutor         = composicao["Tipo"].iloc[composicao.shape[0]-1] *100
    df              = agregate_intraday_second(data)
    ibov            = 0
    win             = 0
    composicao["last"] = 0.0

    for i in range(df.shape[0]):
        updated         = False
        if df.iloc[i]['S'] <start_hour:
            continue
        
        ativo       = df.iloc[i]['TckrSymb']
        dfa         = composicao[(composicao.index == ativo)]
    
        if ativo == cod_win:
            win         = df.iloc[i]['close']
            updated     = True
        
        if dfa.shape[0] >= 1:
            ibov        = 0
            composicao["last"][ativo] = df.iloc[i]['close']*100
            composicao["ibov"] = composicao["last"] * composicao["Tipo"] / redutor
            ibov        = int(composicao["ibov"].sum())
            updated     = True

        if updated:
            resDf.loc[len(resDf.index)] = [df.iloc[i]['S'], ativo, df.iloc[i]['close'], 
                                           ibov, win, (win -ibov), (win -ibov)/ibov]
        if i%10000 == 0:
            print('x',i, ";ativo: ",ativo, ";ibov:",ibov, "win", win,"dif:",(win -ibov),";perc:",(win -ibov)/ibov,  "S:", df.iloc[i]['S'])
            write_ibov_file(resDf, data)
    

    write_ibov_file(resDf, data)
    print(composicao)
    
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    data = "20221124"
    calc_ibov_win(data, "WINZ22", 100700)  