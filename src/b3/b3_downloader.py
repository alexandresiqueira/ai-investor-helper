# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 12:06:35 2022
Funções:
        1. read_last_serie: carrega os dados do último arquivo de series da B3
        2. download_intraday: Faz downlod dos arquivos intraday dos últimos 30 dias, 
                caso não existam no sistema
        3. download_series: Realiza o download da serie B3 de todos exercicios definidos 
                entre constants.DATA_YEAR_INIT, constants.DATA_YEAR_END + 1
        4. update_stock_indicator_file: Atualiza os arquivos contendo os dados dos ativos 
                de constants.STOCKS
                
        
@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
from requests import get  # to make GET request
import os.path
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
import coletor_b3
from datetime import date
import datetime
import pandas as pd

HOUR_MIN_TO_DOWNLOAD_FILES = 19

def download(url, file_name):
    # open in binary mode
    with open(file_name+".tmp", "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)
    if os.path.isfile(file_name):
        os.remove(file_name)
    #if os.stat(file_name).st_size > 0:
     #   print("EMPTY FILE DOWNLOADED: ", file_name)
      #  return
    
    os.rename(file_name+".tmp", file_name)


#carrega os dados do último arquivo de series da B3
def read_last_serie():
    today       = date.today()
    year_today  = today.strftime("%Y")
    file        = 'COTAHIST_A'+year_today+'.ZIP'
    file_name   = constants.PATH_B3_SERIES_LOCAL + file
    if not os.path.isfile(file_name):
        year_today = str(int(year_today)-1)
        print("Reading SERIE ",year_today)
    
    file        = 'COTAHIST_A'+year_today+'.ZIP'
    file_name   = constants.PATH_B3_SERIES_LOCAL + file

    df_serie    = coletor_b3.read_data(file, constants.PATH_B3_SERIES_LOCAL)
    return df_serie
        
    return None


def isBeforeMinHourToDownload():
    now = datetime.datetime.now()
    today_hour = int(now.strftime("%H"))
    #print("hour =", today_hour)
    return (today_hour < HOUR_MIN_TO_DOWNLOAD_FILES)
    
#Faz downlod dos arquivos intraday dos últimos 30 dias, caso não existam no sistema
def download_intraday():
    today = date.today()
        
    start_date = today + datetime.timedelta(days=-3)
    
    for int_day in range(32):
        
        date_download   = (start_date + datetime.timedelta(days=int_day))
        day             = date_download.strftime("%Y-%m-%d")
        day2            = date_download.strftime("%Y%m%d")
        
        if date_download.weekday() in ([5,6]):
            print("WEEKEND DAY:", date_download)
            continue
        if date_download > today:
            print("DOWNLOAD TOMORROW:", day2)
            break
        if ((date_download == today) & (isBeforeMinHourToDownload())):
            print("WAIT AFTER [",HOUR_MIN_TO_DOWNLOAD_FILES,"] HR TO DOWNLOAD TODAY FILE:", day2)
            break
            

        url         = constants.URL_INTRADAY_DOWNLOAD + day
        file_name   = constants.PATH_B3_INTRADAY_LOCAL+ constants.FILE_INTRADAY_PREFIX + day2 + "_1.zip"

        if (os.path.isfile(file_name)):
            if (os.stat(file_name).st_size > 100):
                print("FILE INTRADAY DOWNLOADED BEFORE:",day, "; size:", os.stat(file_name).st_size," - day of week:", date_download.weekday())
                continue

        print("DOWNLOADING INTRADAY:",day, " TO:", file_name)
        download(url, file_name)

#Realiza o download da serie B3 de todos exercicios definidos entre constants.DATA_YEAR_INIT, constants.DATA_YEAR_END + 1
def download_series():
    
    today       = date.today()
    year_today        = today.strftime("%Y")
    
    for year in range (constants.DATA_YEAR_INIT, constants.DATA_YEAR_END + 1):
    
        file        = 'COTAHIST_A'+str(year)+'.ZIP'
        url         = constants.URL_DOWNLOAD_B3 + file
        file_name   = constants.PATH_B3_SERIES_LOCAL+ file
        if (os.path.isfile(file_name) & (year != int(year_today))):
            print("FILE SERIE DOWNLOADED BEFORE:",year, ";year_today:",year_today, ";res:", 
                  (year != int(year_today)), ";ress:",os.path.isfile(file_name) & (year != int(year_today)))
            continue

        print("DOWNLOADING SERIE:",year, " TO:", file_name)
        download(url, file_name)
        
        file_stats = os.stat(file_name)
        if file_stats.st_size < 200:
            print("Remove file (less than 200 bytes) ...", file_name)
            os.remove(file_name)


#Atualiza os arquivos contendo os dados dos ativos constants.STOCKS
#return True se necessário atualizar indicadores de algum ativo
def update_stock_indicator_file():

    df_serie        = read_last_serie()
    max_date_serie  = df_serie["data"].max()
    update_data     = False
    print("max_date in serie:", max_date_serie)

    for ativo in constants.STOCKS:
        fname = constants.PATH_B3_TIMESERIES_DAY+ativo+".csv"
        print("Processando Ativo:", ativo, "; file:", fname)
        
        if os.path.isfile(fname):
            df          = pd.read_csv(fname, sep=';')  
            max_date    = (df["data"].max())
            print("max date:", max_date)

            df_ativo = df_serie.loc[((df_serie['data']) > max_date) & (df_serie['ativo'] == ativo)]

            if df_ativo.shape[0] > 0:
                df_ativo = coletor_b3.extract_stock(df_ativo, ativo)
                df = df.append(df_ativo)
                df.to_csv(fname, sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)
                update_data = True
                print("Ativo Processado:", ativo)
        else:
            update_data = True

    return update_data

    
def main():
    #download_series()    
    download_intraday()
    update_data = update_stock_indicator_file()
    if update_data:
        for applyNormalization in constants.NORMALIZE_OPTIONS:
            coletor_b3.charge_b3_data(applyNormalization, 
                                  path_stocks=constants.PATH_B3_TIMESERIES_DAY, 
                                  path_series=constants.PATH_B3_SERIES_LOCAL)
        
        
        
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()        