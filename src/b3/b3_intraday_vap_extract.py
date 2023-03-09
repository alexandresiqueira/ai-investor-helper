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
from datetime import date
import datetime 
import b3_downloader

np.set_printoptions(threshold=None, precision=4)
pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
#pd.set_option('precision', 4)
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
def agregate_intraday(df, round_price=False):
    

    df["PrecoNegocio"] = (df["PrecoNegocio"].str.replace(',','.')).astype(float)
    if (round_price):
        df["PrecoNegocio"] = (df["PrecoNegocio"]).astype(int)#retira casas decimais 
    #df["S"] = (df["NtryTm"]/1000).astype(int)

    #atributos = [ "RptDt","S", "TckrSymb","UpdActn","TradgSsnId"]
    atributos = [ "DataReferencia", "CodigoInstrumento", "AcaoAtualizacao","PrecoNegocio"]
        
    #df = df.groupby(atributos).agg({"GrssTradAmt": ['first', 'max' , 'min', 'last'], "TradQty": ['sum']})
    df = df.groupby(atributos).agg({"HoraFechamento": ['first', 'last'], "QuantidadeNegociada": ['sum']})
    df.columns = [ 'time-first', 'time-last', 'volume']
    df = df.reset_index()
    
    return df


def calc_top_volume_day(stocks, day, number_top, round_price=False):

    if day == None:    
        day = calc_last_day()
    print("DAY ANALISED:", day)

    d = read_intraday_file_full(day, constants.PATH_B3_INTRADAY_LOCAL);
    if (stocks != None):
        d = d.loc[(d["CodigoInstrumento"].isin(stocks) )] # stock)]
    
    d = agregate_intraday(d, round_price)

    d = d.sort_values(by=["CodigoInstrumento", 'volume'], axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')  

    d["rank"] = d.groupby("CodigoInstrumento")["volume"].rank(method="dense", ascending=False)

    #print(d.head(10))

    d = d.loc[(d["rank"] <= number_top)]
    return d    

def calc_last_day():
    date_analyse = date.today()
    if b3_downloader.isBeforeMinHourToDownload():
        date_analyse = date_analyse + datetime.timedelta(days=-1)

    day = date_analyse.strftime("%Y%m%d")
    return day

def main():

    stocks = ["WDOJ23", "WINJ23"]
    number_top=10
    round_price=False
    day = None
    if day == None:
        day = calc_last_day()
    d = calc_top_volume_day(stocks, day, number_top, round_price)

    print(d)


print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()        