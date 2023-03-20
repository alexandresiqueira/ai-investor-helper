# -*- coding: utf-8 -*-
"""
Created on Sat Mar  4 10:16:29 2023

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup
import socket
import codecs
import json
import re
import pandas as pd
import ta
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import date
import datetime
import os
import sys
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
#pd.set_option('precision', 4)
pd.set_option('display.width', 1000)

__page_source = '<html><head></head><body>{"t":[1677873480,1677873540,1677873600,1677873660,1677873720,1677873780,1677873840,1677873900,1677873960,1677874020,1677874080,1677874140,1677874200,1677874260,1677874320,1677874380,1677874440,1677874500,1677874560,1677874620,1677874680,1677874740,1677874800,1677874860,1677874920,1677874980,1677875040,1677875100,1677875160,1677875220,1677875280,1677875340,1677875400,1677875460,1677875520,1677875580,1677875640,1677875700,1677875760,1677875820,1677875880,1677875940,1677876000,1677876060,1677876120,1677876180,1677876240,1677876300,1677876360,1677876420,1677876480,1677876540,1677876600,1677876660,1677876720,1677876780,1677876840,1677876900,1677876960,1677877020,1677877080,1677877140,1677877200,1677877260,1677877320,1677877380,1677877440,1677877500,1677877560,1677877620,1677877680,1677877740,1677877800,1677877860,1677877920,1677877980,1677878040,1677878100,1677878160,1677878220,1677878280,1677878340,1677878400,1677878460,1677878520,1677878580],"c":[5.1989998817444,5.1995000839233,5.200749874115,5.1991000175476,5.1984000205994,5.1995000839233,5.1993999481201,5.1995000839233,5.1991000175476,5.1983499526978,5.1983499526978,5.1986999511719,5.1983499526978,5.1989498138428,5.1988501548767,5.1985998153686,5.1999998092651,5.1988501548767,5.1984000205994,5.1984000205994,5.1993498802185,5.1992001533508,5.1992502212524,5.1989998817444,5.1978998184204,5.197949886322,5.197850227356,5.197850227356,5.197850227356,5.1970000267029,5.197850227356,5.197350025177,5.1985001564026,5.1987500190735,5.1992502212524,5.1991000175476,5.2010002136231,5.2012500762939,5.2013502120972,5.2028999328613,5.2027502059936,5.2034997940064,5.2047500610352,5.2031002044678,5.2028498649597,5.201849937439,5.2037501335144,5.201849937439,5.2014999389648,5.2016000747681,5.2013502120972,5.2012000083923,5.1988501548767,5.1985998153686,5.1999998092651,5.1992001533508,5.1991000175476,5.197850227356,5.1999001502991,5.1988501548767,5.1995000839233,5.197350025177,5.1975998878479,5.1968498229981,5.1971001625061,5.197350025177,5.1971001625061,5.197350025177,5.1968498229981,5.1958498954773,5.1956000328064,5.1963500976562,5.1956000328064,5.1958498954773,5.1971001625061,5.1988501548767,5.1983499526978,5.1975998878479,5.1971001625061,5.1971001625061,5.1961002349853,5.1961002349853,5.1961002349853,5.1953501701355,5.1948499679565,5.1946001052856],"o":[5.198450088501,5.1983499526978,5.1988501548767,5.1994500160217,5.1988501548767,5.1983499526978,5.1991000175476,5.1993498802185,5.1992001533508,5.1993498802185,5.1985001564026,5.1983499526978,5.1986999511719,5.1988000869751,5.1997499465942,5.1999998092651,5.1985998153686,5.1993498802185,5.1999998092651,5.1988501548767,5.198450088501,5.1999998092651,5.1988501548767,5.1984000205994,5.1983499526978,5.1982002258301,5.197850227356,5.1985001564026,5.1979999542236,5.1975002288818,5.1968498229981,5.197850227356,5.1983499526978,5.1985001564026,5.197850227356,5.1988501548767,5.1999998092651,5.2010002136231,5.2003498077393,5.2013502120972,5.2026000022888,5.2021999359131,5.2042498588562,5.2031998634338,5.2031002044678,5.2028498649597,5.2023501396179,5.2030000686645,5.201849937439,5.2013502120972,5.2027502059936,5.2013502120972,5.2022500038147,5.1988501548767,5.2002501487732,5.1993498802185,5.1999998092651,5.1999998092651,5.1981000900269,5.1999998092651,5.197850227356,5.1995000839233,5.197350025177,5.1975998878479,5.197350025177,5.1971001625061,5.197350025177,5.1971001625061,5.197350025177,5.1968498229981,5.1958498954773,5.1958498954773,5.1963500976562,5.1956000328064,5.1965999603272,5.1971001625061,5.1988501548767,5.1985998153686,5.1975998878479,5.1971001625061,5.1971001625061,5.1956000328064,5.1956000328064,5.1958498954773,5.1956000328064,5.1956000328064],"h":[5.1992502212524,5.2002501487732,5.200749874115,5.1994500160217,5.1992502212524,5.1995000839233,5.1999998092651,5.1999998092651,5.1995000839233,5.1995000839233,5.1985001564026,5.1995000839233,5.1988501548767,5.1992001533508,5.1997499465942,5.1999998092651,5.1999998092651,5.1994500160217,5.1999998092651,5.1995000839233,5.1995000839233,5.2005000114441,5.2005000114441,5.1989998817444,5.1983499526978,5.1992502212524,5.1985001564026,5.1987500190735,5.1979999542236,5.1982498168945,5.1982498168945,5.1997499465942,5.1989998817444,5.1987500190735,5.1995000839233,5.1997499465942,5.2010002136231,5.2012500762939,5.2019000053406,5.2032499313355,5.2037501335144,5.2038497924805,5.2052001953125,5.2042498588562,5.2042498588562,5.2037501335144,5.2037501335144,5.2033500671387,5.2023501396179,5.2027502059936,5.2027502059936,5.2022500038147,5.2022500038147,5.2005000114441,5.2005000114441,5.2002501487732,5.1999998092651,5.2002501487732,5.2005000114441,5.2005000114441,5.1997499465942,5.1995000839233,5.197850227356,5.1975998878479,5.197350025177,5.197350025177,5.197350025177,5.197350025177,5.197350025177,5.1968498229981,5.1958498954773,5.1963500976562,5.1963500976562,5.1963500976562,5.1971001625061,5.1988501548767,5.1988501548767,5.1985998153686,5.1975998878479,5.1971001625061,5.1971001625061,5.1961002349853,5.1961002349853,5.1961002349853,5.1956000328064,5.1956000328064],"l":[5.1983499526978,5.1981000900269,5.1988501548767,5.1988501548767,5.1978998184204,5.1978998184204,5.1989498138428,5.1988000869751,5.1988501548767,5.1983499526978,5.197850227356,5.1983499526978,5.1983499526978,5.1988000869751,5.1988000869751,5.1985998153686,5.1985998153686,5.1988501548767,5.1975998878479,5.197850227356,5.198450088501,5.1991000175476,5.1982002258301,5.1984000205994,5.197350025177,5.1975998878479,5.197350025177,5.197350025177,5.1965999603272,5.1970000267029,5.1968498229981,5.197350025177,5.197949886322,5.197850227356,5.197850227356,5.1981000900269,5.1999998092651,5.2000999450684,5.2003498077393,5.2008500099182,5.2016000747681,5.201849937439,5.2033500671387,5.2026000022888,5.2028498649597,5.201849937439,5.2020998001099,5.2012500762939,5.2014999389648,5.2013502120972,5.2013502120972,5.2010998725891,5.1983499526978,5.1985998153686,5.1988501548767,5.1988501548767,5.1988501548767,5.197850227356,5.1981000900269,5.1988501548767,5.197850227356,5.197350025177,5.1971001625061,5.1968498229981,5.1968498229981,5.1968498229981,5.1971001625061,5.1968498229981,5.1968498229981,5.1958498954773,5.1956000328064,5.1958498954773,5.1956000328064,5.1956000328064,5.1965999603272,5.1965999603272,5.1983499526978,5.1975998878479,5.1963500976562,5.1971001625061,5.1961002349853,5.1956000328064,5.1956000328064,5.1953501701355,5.1948499679565,5.1946001052856],"v":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"vo":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],"s":"ok"}</body></html>'

URL_BASE_HISTORY = "https://tvc4.investing.com/285ea8f8f1ddd7b0f74c5f9bbe0ae7e2/0/0/0/0/history?"
URL_BASE_REAL_TIME = "https://tvc4.investing.com/285ea8f8f1ddd7b0f74c5f9bbe0ae7e2/1677870877/30/12/12/quotes?symbols=USD/EUR"
URL_BASE_TICKER_INFO = "https://tvc4.investing.com/285ea8f8f1ddd7b0f74c5f9bbe0ae7e2/1677870877/30/12/12/symbols?symbol="
SYMBOL_BRL_USD = 1516
SYMBOL_USD_BRL = 2103
SYMBOL_USD_EUR = 2124
SYMBOL_EUR_USD = 1
SYMBOL_DX = 8827
dict_symbols = {SYMBOL_BRL_USD: "BRL/USD",SYMBOL_USD_BRL:"USD/BRL", SYMBOL_USD_EUR:"USD/EUR", SYMBOL_DX:"DX"}
installDriver=False

days_history_standard=90


#driver = None
#wait = None

#def __prepare_web_driver():
    
    
#from fake_useragent import UserAgent
#user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
#chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument(f'user-agent={user_agent}')
#driver = webdriver.Chrome(executable_path = f"your_path",chrome_options=chrome_options)

    
def __req_data(val):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    #chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'user-agent={user_agent}')
    if installDriver:
        driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chrome_options)
    else:
        driver=webdriver.Chrome(options=chrome_options)
    #driver.set_window_size(200, 200)
    
    #wait = WebDriverWait(driver, 10)
    wait = WebDriverWait(driver, 10)

        
    driver.get(val)
    
    print("requesting.....:",val)
    get_url = driver.current_url
    wait.until(EC.url_to_be(val))

    if get_url == val:
    
        resp = driver.page_source
        #print("PAGE SOURCE END:", resp)
        #driver.quit()
        #print("url..........END")
        return resp
    #print("depois")
    return None

def __mount_url(symbol, resolution, time_from, time_to):
    req_params = 'symbol='+str(symbol)+'&resolution='+ str(resolution)+  '&from='+str(time_from )+ '&to='+str(time_to)
    url = URL_BASE_HISTORY+req_params
    #print(req_params)
    return url
    


def __save_currency_history(pair, resolution, df, path_pair=constants.DATA_PATH_CURRENCY):
    df.to_csv(path_pair+str(pair)+"-"+str(resolution)+".csv", sep=constants.CSV_SEPARATOR, index=False)

def __save_currency_percent_history(pair, resolution, df, path_pair=constants.DATA_PATH_CURRENCY):
    df.to_csv(path_pair+str(pair)+"-"+str(resolution)+"-percent.csv", sep=constants.CSV_SEPARATOR, index=False)

    
def read_currency_history(pair, resolution, path_pair=constants.DATA_PATH_CURRENCY):
    fname = path_pair+str(pair)+"-"+str(resolution)+".csv"
    df = pd.read_csv(fname, sep=constants.CSV_SEPARATOR)  
    df['date_time'] = pd.to_datetime(df.t, unit='s')  - pd.Timedelta(time_delta)
    return df

def is_pair_saved(pair, resolution, path_pair=constants.DATA_PATH_CURRENCY):
    fname = path_pair+str(pair)+"-"+str(resolution)+".csv"
    return os.path.isfile(fname)
    

def __get_body_data_as_dict(html_text):
    soup = BeautifulSoup(html_text,features='html.parser')
    json_data = soup.find_all('body')    
    data = json_data[0].text
    dict = json.loads(data)
    return dict


def __get_history_data(page_source=__page_source):
    dict = __get_body_data_as_dict(page_source)
    df2 = pd.DataFrame()
    for col in dict.keys():
        df2[col] = dict[col]

    if df2.shape[0] > 0 :
        df2['date_time'] = pd.to_datetime(df2.t, unit='s') - pd.Timedelta(time_delta)

    return df2



def __get_timestamp(days_before, hour, minute=0, second=0, microsecond=0):
    now = datetime.datetime.now()
    last_date = now + datetime.timedelta(days=-days_before)
    #last_date = today + datetime.timedelta(days=-int_day)
    last_date = last_date.replace(hour=hour, minute=minute, second=second, microsecond=microsecond)
    #print(last_date, ';timestamp:', last_date.timestamp())
    return int(last_date.timestamp())
    

def load_history(symbol, resolution=60, days_before_from=3, days_before_to=2, hour_start=18, minute_start=30, hour_end=8):
    return load_history_ts(symbol, resolution=resolution, 
                time_from=__get_timestamp(days_before=days_before_from, hour=hour_start, minute=minute_start), 
                time_to=__get_timestamp(days_before=days_before_to, hour=hour_end))

def load_history_ts(symbol, resolution, time_from, time_to):
    url = __mount_url(symbol, resolution,  time_from,  time_to)
    #print("1 - ##################################PAIR:",ticker_to_string(symbol), " - TIMEFRAME:", resolution)
    resp = __req_data(url)
    #print("2 - ##################################",symbol)
    df2 = __get_history_data(resp)
    #print("4 - ##################################",ticker_to_string(symbol))
    return df2

def load_tick_code(pair="USD/BRL"):
    url = URL_BASE_TICKER_INFO+pair
    text = __req_data(url)
    #text = '{"name":"USD\/BRL","exchange-traded":"C\u00e2mbio em tempo real","exchange-listed":"C\u00e2mbio em tempo real ","timezone":"UTC","minmov":1,"minmov2":0,"pricescale":10000,"pointvalue":1,"has_intraday":true,"has_no_volume":true,"volume_precision":3,"ticker":"2103","description":"USD\/BRL","type":"FX","has_daily":true,"has_weekly_and_monthly":true,"supported_resolutions":["1","5","15","30","60","300","D","W","M","45","120","240"],"intraday_multipliers":["1","5","15","30","60","300"],"session":"2;0000-2359:23456","data_status":"streaming"}'
    #print(text)
    dict = __get_body_data_as_dict(text)
    print("pair:", pair, " - ticker:", dict["ticker"])
    return dict["ticker"]

def calc_percent_from(df, time_start):
    df = df.loc[(df['t'] >= time_start)].copy()
    value_ref = df.iloc[0]["c"]
    print("VALUE-REF:",value_ref)
    df['perc'] = 100*((df['c']/value_ref)-1)
    return df





def calc_percent(dfx, hour_ref, minute_ref):
    #df = df.loc[(df['t'] >= time_start)].copy()
    #df['time'] = datetime.datetime.fromtimestamp(df['t'])
    df = dfx.copy()
    df['perc'] = 0
    df['value-ref'] = -1
    t0 = df.iloc[0]['t']
    
    t1 = 0
    t_fim = df.iloc[df.shape[0]-1]['t']
    dt = datetime.datetime.fromtimestamp(t0)
    t0 = t0 - dt.hour*60*60 - dt.minute*60
    t0 = t0 + hour_ref*60*60 + minute_ref*60
    dfT = df.loc[(df['t']<= t0)]
    #print("shape:",dfT.shape[0])
    value_ref = 0
    if dfT.shape[0] > 0:
        value_ref = dfT.iloc[dfT.shape[0]-1]['c']
    #t_init = t0
    t1 = t0 + 24*60*60 #+ hour_ref*60*60 + minute_ref*60
    
    #print("INICIO CALC:",t0, ";", t1, ";", t_fim, ";dtfim:",datetime.datetime.fromtimestamp(t_fim), ";value_ref:", value_ref)
    while t0 < t_fim:
        #print("INCIO DIA:",t0, ";dt0:",datetime.datetime.fromtimestamp(t0), ";", t1, ";dt1:",datetime.datetime.fromtimestamp(t1))
        dfT = df.loc[((df['t'] >= t0) & (df['t'] <= t1))]
        df.loc[dfT.index, 'value-ref'] = value_ref

        dt1 = datetime.datetime.fromtimestamp(t1)

        if (dt1.weekday() != 5) & (dt1.weekday() != 6) & (dfT.shape[0] > 0):
            #print("shape DFT:",dfT.shape[0], ";date:", dt1)
            value_ref = dfT.iloc[dfT.shape[0]-1]['c']
        
        t0 = t1
        t1 = t0 + 24*60*60 

        dfT = df.loc[((df['t'] >= t0) & (df['t'] <= t1))]

        df.loc[dfT.index, 'value-ref'] = value_ref

    df['perc'] = 100*((df['c']/df['value-ref'])-1)

    return df
    
def calc_percent2(dfx, hour_ref, minute_ref):
    #df = df.loc[(df['t'] >= time_start)].copy()
    #df['time'] = datetime.datetime.fromtimestamp(df['t'])
    df = dfx.copy()
    value_ref = 0
    df['perc'] = 0
    df['value-ref'] = -1
    #print("shape:",df.shape[0])
    for i in range(df.shape[0]):
        timest = df['t'].iloc[i]
        tm = datetime.datetime.fromtimestamp(timest)       
        if ((tm.hour == hour_ref) & (tm.minute == minute_ref)):
            
            value_ref = df['c'].iloc[i]
            #print(df.iloc[i])
            #print("Identificou ref:",df['date_time'].iloc[i] , ";value_ref:",value_ref)
        if value_ref == 0:
            continue
        df['value-ref'].iloc[i] = value_ref
        #print(i, ";",value_ref, )
        #print( df.iloc[i][ 'value-ref'])
        #print( df.loc[i, 'value-ref'])
        
        #df.loc[i, 'value-ref'] = value_ref
        #break
        df['perc'].iloc[i] = 100*((df['c'].iloc[i]/value_ref)-1)
        #df.loc[i, 'perc'] = 100*((df['c'].iloc[i]/value_ref)-1)
    #value_ref = df.iloc[0]["c"]
    #print("VALUE-REF:",value_ref)
    #df['perc'] = 100*((df['c']/value_ref)-1)
    #return df
    #print(df.tail(245))

    return df

def get_and_save_pair(pair, resolution, days_before_from=days_history_standard):
    df1 = load_history(pair, resolution, days_before_from=days_before_from, days_before_to=0, hour_start=0)
    print(df1.shape)
    shape = df1.shape[0]
    dfTemp = df1
    while shape == 5000:#máximo de registros retornados pelo serviço
        print(pair, " - Carregando mais registros - pair:", pair)
        t1      = dfTemp['t'].iloc[4999] 
        
        df2     = load_history_ts(pair, resolution, t1, __get_timestamp(days_before=0, hour=23, minute=59, second=59))
        shape   = df2.shape[0]
        dfTemp  = df2
        df1     = df1.append(df2)
        print(pair, " - Registros carregados:", shape)
    __save_currency_history(pair, resolution, df1)


def check_pairs(pairs, resolution):
    for pair in pairs:
        print("\n########################## INIT CHECK UPDATE - ",ticker_to_string(pair)," - TIMEFRAME["+resolution+"] ########################## - ", datetime.datetime.now())
        check_pair(pair, resolution)
        
def check_pair(pair, resolution):        
    if not is_pair_saved(pair, resolution):
        get_and_save_pair(pair, resolution)
        return True
    else:
        df      = read_currency_history(pair, resolution)
        last_t  = df.tail(1).iloc[0]['t']
        dt      = datetime.datetime.fromtimestamp(last_t)
        ts_now  = datetime.datetime.now().timestamp()
        dif     = ts_now - last_t
        print ("CHECK for pair:", pair, "last:", last_t, "now:", ts_now, "; dif:", dif, "; dt:",dt, ";wd:", dt.weekday())
        
        if (datetime.datetime.now().weekday() == (5)) & (dt.weekday() == 4)  & (dt.hour == 17) :
            #& ((pair == SYMBOL_USD_BRL & dt.minute == 30 - resulotion) | (pair != SYMBOL_USD_BRL & dt.minute == 60 - resolution))                
            print("CHECK for pair [", pair, "] weekend waiting ...")
        
        else:
            df2     = load_history_ts(pair, resolution, time_from=last_t, time_to = __get_timestamp(days_before=0, hour=23, minute=59, second=59))
            print("CHECK for pair [", pair, "] data retried:", df2.shape[0])
            if df2.shape[0] > 0:
                #df     = df.append(df2)
                #df = pd.concat(df, df2)
                if (df.iloc[df.shape[0]-1]['t'] == df2.iloc[0]['t']):
                    #print("cortando...")
                    #print(df.tail(2))
                    df = df.drop(df.shape[0]-1, axis=0)
                    #print(df.tail(2))
                df = pd.concat([df,df2], axis=0)
                #print(df.tail(2))
                print("CHECK for pair [", pair, "] saving resolution [",resolution,"]")
                __save_currency_history(pair, resolution, df)
                return True
    return False

def __check_data(pair, resolution):
    df = read_currency_history(pair, resolution)
    print(df.tail(15))
    #df['date_time'] = pd.to_datetime(df.t, unit='s') - pd.Timedelta(time_delta)
    columns = ['Unnamed: 0','t.1','c.1','o.1','h.1','l.1','v.1','vo.1','s.1','date_time.1']
    columns = ['nextTime']
    #df = df.drop(columns=['Unnamed: 0.4', 'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0'])
    df = df.drop(columns=columns)
    print(df.tail(15))
    __save_currency_history(pair, resolution, df)


def check_for_updates(time_frame, use_random=False):
    if use_random:
        sleep_seconds = random.randint(10, 25)
        print("Waiting .... [",sleep_seconds,"] seconds", datetime.datetime.now())
        time.sleep(sleep_seconds)
    check_pairs(pairs, time_frame)

#########################################################################
#load_tick_code("EUR/USD")
#load_history("USD/BRL")
#df = load_history(SYMBOL_USD_BRL)
path_percent_file_dir="C:/Users/ccgov/AppData/Roaming/MetaQuotes/Terminal/Common/Files/"
resolutions = ["1","5","15","30","60","D","W","M"]
time_delta  = '00:00:00'
resolution  = "1"
hour_ref    = 17
minute_ref  = 0
days_calc_percent=60
hour_open_mkt = 8 + 3 ##consider tmizone diff
hour_close_mkt = 18 + 3 ##consider tmizone diff
pairs       = [SYMBOL_USD_EUR, SYMBOL_USD_BRL, SYMBOL_DX]
#pairs       = [SYMBOL_USD_EUR, SYMBOL_USD_BRL]
#pairs       = [SYMBOL_USD_EUR, SYMBOL_DX]
#pairs       = [SYMBOL_USD_EUR]
sleep_seconds = 15
max_req = 1
#for pair in pairs:

def get_resolution_minutes(resolution):
    if resolution == "D":
        return 24*60
    elif resolution == "W":
        return 7*24*60
    elif resolution == "M":
        return 30*24*60
    return int(resolution)

def ticker_to_string(ticker):
    return str(ticker) + " - "+ dict_symbols[ticker]

def exec_update():
    cont = 0
    
    while cont < max_req:
        cont = cont + 1
        for resol in resolutions:        
            #check_for_updates(resol)
            
            print('reading:', cont, " from:", max_req)
            for pair in pairs:
                try:
                    check_pair(pair, resol)
                    ts_init = __get_timestamp(days_before=days_calc_percent, hour=0)
                    df = read_currency_history(pair, resol)
                    df2 = df.loc[(df['t']>ts_init)].copy()
            
                    df2 = calc_percent(df2, hour_ref, minute_ref)

                    trend_ma = ta.trend.SMAIndicator(close=df2["perc"], window=5)
                    df2["perc-5"] = round(trend_ma.sma_indicator(), 6)
                    trend_ma = ta.trend.SMAIndicator(close=df2["perc"], window=20)
                    df2["perc-20"] = round(trend_ma.sma_indicator(), 6)

                    
                    #df = df.loc[(df['date_time'].dt.hour == 21) | (df['date_time'].dt.hour == 11)]
                    print("\n\n################################## LAST - ",ticker_to_string(pair)," - TIMEFRAME["+resol+"] ##################################")
                    print(df2.tail(20)) 
                    __save_currency_percent_history(pair, resol, df2, path_percent_file_dir)
                    df2 = df2.loc[(df['date_time'].dt.hour == hour_open_mkt) & (df2['date_time'].dt.minute == (60 - get_resolution_minutes(resol)))]
                    print("################################## OPEN - ",ticker_to_string(pair)," - TIMEFRAME["+resol+"] ##################################")
                    print(df2.tail(3))
                    """df2 = df2.loc[( (df['date_time'].dt.hour >= hour_open_mkt) &
                                    (df['date_time'].dt.hour < hour_close_mkt) ) 
                                  | ((df['date_time'].dt.hour == hour_close_mkt) & (df['date_time'].dt.minute < 30)  & (df['date_time'].dt.weekday != 6) & (df['date_time'].dt.weekday != 5))
                                  
                                  ]
                    __save_currency_percent_history(pair, resol, df2, "C:/Users/ccgov/AppData/Roaming/MetaQuotes/Terminal/Common/Files/")
                """
                except PermissionError:
                    print("ALERT: Erro de permissao, ", pair, "resol:",resolution)
                except socket.timeout:
                    print("ALERT: Erro de TimeoutException, ", pair, "resol:",resolution)
        
        print("Waiting .... [",sleep_seconds,"] seconds", datetime.datetime.now())
        
        if cont != (max_req):
            time.sleep(sleep_seconds)



"""
df1 = load_history(SYMBOL_USD_EUR, resolution, days_before_from=3, days_before_to=2, hour_start=17)
df1 = calc_percent_from(df1, 1677706200)

df2 = load_history(SYMBOL_USD_BRL, resolution, days_before_from=3, days_before_to=2, hour_start=17)
df2 = calc_percent_from(df2, 1677706200)

df3 = pd.DataFrame()
df3 = df1[["t","date_time", "c", "perc"]]
df3.columns = ["t", "date_time", "c1",  "perc-1"]
df3.set_index('t')
print(df1)
print(df2)
print(df3)

df4 = pd.DataFrame()
df4 = df2[["t", "c","perc"]]
df4.columns = ["t", "c2","perc-2"]
df4.set_index('t')
print(df4)

#df = pd.concat([df3, df4], axis=1, join="outer")
dfx = pd.merge(df3, df4, on='t', how='outer')
dfx['spread'] = dfx['perc-1'] - dfx['perc-2']
#result = pd.concat([df1, df4], axis=1, join="inner")
"""
#print(df.head(80))
# print(dfx.head(240))


if __name__ == "__main__":
    init = time.time()
    #__check_data(pairs[0], resolution)
    #__check_data(pairs[1], resolution)
    exec_update()    
    end = time.time()
    print("elapsed seconds:", int(end - init))
