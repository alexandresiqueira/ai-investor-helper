# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 21:36:12 2022

Organiza os dados intraday em timeframes

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import numpy as np
import pandas as pd
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants

np.set_printoptions(threshold=None, precision=4)
pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 4)
pd.set_option('display.width', 1000)



#carrega os dados do arquivo intraday completo
def read_intraday_file_full(data, path=constants.DATA_PATH):
    df = pd.read_csv(path+constants.FILE_INTRADAY_PREFIX+data+'_1.zip', 
                     compression='zip', header=0, sep=constants.CSV_SEPARATOR)

    return df

#Carrega os dados diarios do arquivo intraday dos ativos informados em constants.STOCKS
def read_intraday_file(data, path=constants.DATA_PATH):
    df = read_intraday_file_full(data, path)
    df = df.loc[(df['TckrSymb'].isin(constants.STOCKS)) ]

    return df


#Agrupa os registros dos arquivos intraday por segundo
def agregate_intraday_second(df):
    

    df["GrssTradAmt"] = (df["GrssTradAmt"].str.replace(',','.')).astype(float)
    df["S"] = (df["NtryTm"]/1000).astype(int)

    atributos = [ "RptDt","S", "TckrSymb","UpdActn","TradgSsnId"]
        
    df = df.groupby(atributos).agg({"GrssTradAmt": ['first', 'max' , 'min', 'last'], "TradQty": ['sum']})
    df.columns = [ 'open', 'high', 'low', 'close', 'volume']
    df = df.reset_index()
    
    return df

#Agrupa os registros de um dia em vários timeframes
def process(date, stock):
    df = read_intraday_file(date, constants.PATH_B3_INTRADAY_LOCAL)
    

    df["GrssTradAmt"] = (df["GrssTradAmt"].str.replace(',','.')).astype(float)
    df["M"] = (df["NtryTm"]/1000).astype(int)
    df["H1"] = (df["M"] - df["M"]%(100*100)).astype(int)

    atributos = [ "RptDt", "TckrSymb","UpdActn","TradgSsnId","M", "H1"]
    for tm in constants.TIMEFRAMES:
        df["M"+str(tm)] = df["M"] - df["H1"] 
        df["M"+str(tm)] = (df["M"+str(tm)] - df["M"+str(tm)]%(tm*100) +  df["H1"]).astype(int)
        atributos = atributos + ["M"+str(tm)]
        
    d = df.copy()
    if (stock != None):
        d = df.loc[(df["TckrSymb"] == stock)]

    d = d.groupby(atributos).agg({"GrssTradAmt": ['first', 'max' , 'min', 'last'], "TradQty": ['sum']})
    d.columns = [ 'open', 'high', 'low', 'close', 'volume']
    d = d.reset_index()

    """atributos = [ "RptDt", "TckrSymb","UpdActn"]
    res2 = df.groupby(atributos).agg({"GrssTradAmt": ['first', 'max' , 'min', 'last'], "TradQty": ['sum']})
    res2.columns = [ 'open', 'high', 'low', 'close', 'volume']
    res2 = res2.reset_index()
    """
    return d


def main():
    d = process("20221027", "VALE3")
    print(d.head(200))


print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()        