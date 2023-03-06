# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 20:06:09 2023

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import pandas as pd
import base64
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants
from investiny import historical_data
from investiny import search_assets
#data = historical_data(investing_id=6408, from_date="09/01/2022", to_date="10/01/2022") # Returns AAPL historical data as JSON (without date)
results = search_assets(query="AAPL", limit=1, type="Stock", exchange="NASDAQ")

pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
#pd.set_option('precision', 4)
pd.set_option('display.width', 1000)

def request_json(url):
    #headers = {'Accept': 'application/json'}
    headers = {
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        #, 'Accept-Encoding':'gzip, deflate, br'
        #, 'Accept-Language': 'pt-BR,pt;q=0.9'
        #, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        #, 'cookie':'browser-session-counted=true; user-browser-sessions=1; adBlockerNewUserDomains=1677816663; udid=e6e580bfb32900142b4eeb4e5b8db3b2; _gid=GA1.2.449053324.1677816667; _fbp=fb.1.1677816668482.1295667215; panoramaId_expiry=1677903075426; _cc_id=c8b58b206279843bded0533bbf9344cc; __gads=ID=fc4cecbf16fb8092-227d71eacd7f0091:T=1677816666:S=ALNI_MahgExekVznNuVNYWMCxASQCvVuLQ; OptanonAlertBoxClosed=2023-03-03T04:11:23.926Z; pm_score=clear; _hjSessionUser_174945=eyJpZCI6IjhkMjYwNDFmLTE0NGEtNWZkOC1iNDc4LWY4ZjBlMWViMDFjZCIsImNyZWF0ZWQiOjE2Nzc4MTY2OTY1NjksImV4aXN0aW5nIjp0cnVlfQ==; __gpi=UID=000009c65236f7cb:T=1677816666:RT=1677867963:S=ALNI_MZDQHCdMrRH7wBtc4CbR-n4_E6Cmg; invpc=9; OptanonConsent=isIABGlobal=false&datestamp=Fri+Mar+03+2023+15:48:29+GMT-0400+(Horário+Padrão+do+Amazonas)&version=202209.2.0&hosts=&consentId=1adb9bd2-de49-4401-9359-94c4c79d5c74&interactionCount=2&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0002:1,C0004:1,BG41:1&AwaitingReconsent=false&geolocation=BR;AM; _ga=GA1.2.1316973240.1677816666; page_view_count=16; _ga_C4NDLGKVMK=GS1.1.1677888287.6.0.1677888287.60.0.0; __cf_bm=Ko1oN.S2xCKYf4P.KgF6rPDyN3q_zqtj9RvSTFvlmq0-1677932683-0-AX6syjvyXO8oJ1uCZ/VJ/QTdSxKXFTWv+4+fmAgDyZVsmCvgHPDa0Ez++dreR1CPnK+Lmhng773DLYYSnx9YFMg='
        #, 'cookie':'__cf_bm=P_7VnfGVnXFKgK6G1SrUeZ1XvViVAHLkVFCTUURiTGI-1677935397-0-ARj4rf9MYddsVQCCMf1LDBQmhEdLxzTx1sILvCYIQPffBM6W5AOOyWHTmJhLXGSxuHV5ScD6q5WS3rR6np5igVA=; path=/; expires=Sat, 04-Mar-23 13:39:57 GMT; domain=.investing.com; HttpOnly; Secure; SameSite=None'
        }
    print("call url:", url)
    s = requests.Session()
    res = s.get("https://tvc4.investing.com/285ea8f8f1ddd7b0f74c5f9bbe0ae7e2/", headers=headers)
    cookies = dict(res.cookies)
    print(res)
    print(res.text)
    print("###################")
    print("###################")
    print("###################")
    print("###################")
    r = s.get(url, headers=headers, cookies=cookies)
    #r = requests.get(url, headers=headers)
    #r = requests.get(url)
    #print(f"Response: {r.json()}")
    print(r.text)
    print(r)
    print(r.headers)
    return r

def req2():
    url = "https://www.investing.com/instruments/HistoricalDataAjax"
    headers = {
        #'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
         #'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        #, 'Accept-Encoding':'gzip, deflate, br'
        #, 'Accept-Language': 'pt-BR,pt;q=0.9'
        #, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
        #, 'cookie':'browser-session-counted=true; user-browser-sessions=1; adBlockerNewUserDomains=1677816663; udid=e6e580bfb32900142b4eeb4e5b8db3b2; _gid=GA1.2.449053324.1677816667; _fbp=fb.1.1677816668482.1295667215; panoramaId_expiry=1677903075426; _cc_id=c8b58b206279843bded0533bbf9344cc; __gads=ID=fc4cecbf16fb8092-227d71eacd7f0091:T=1677816666:S=ALNI_MahgExekVznNuVNYWMCxASQCvVuLQ; OptanonAlertBoxClosed=2023-03-03T04:11:23.926Z; pm_score=clear; _hjSessionUser_174945=eyJpZCI6IjhkMjYwNDFmLTE0NGEtNWZkOC1iNDc4LWY4ZjBlMWViMDFjZCIsImNyZWF0ZWQiOjE2Nzc4MTY2OTY1NjksImV4aXN0aW5nIjp0cnVlfQ==; __gpi=UID=000009c65236f7cb:T=1677816666:RT=1677867963:S=ALNI_MZDQHCdMrRH7wBtc4CbR-n4_E6Cmg; invpc=9; OptanonConsent=isIABGlobal=false&datestamp=Fri+Mar+03+2023+15:48:29+GMT-0400+(Horário+Padrão+do+Amazonas)&version=202209.2.0&hosts=&consentId=1adb9bd2-de49-4401-9359-94c4c79d5c74&interactionCount=2&landingPath=NotLandingPage&groups=C0003:1,C0001:1,C0002:1,C0004:1,BG41:1&AwaitingReconsent=false&geolocation=BR;AM; _ga=GA1.2.1316973240.1677816666; page_view_count=16; _ga_C4NDLGKVMK=GS1.1.1677888287.6.0.1677888287.60.0.0; __cf_bm=Ko1oN.S2xCKYf4P.KgF6rPDyN3q_zqtj9RvSTFvlmq0-1677932683-0-AX6syjvyXO8oJ1uCZ/VJ/QTdSxKXFTWv+4+fmAgDyZVsmCvgHPDa0Ez++dreR1CPnK+Lmhng773DLYYSnx9YFMg='
        #, 'cookie':'__cf_bm=P_7VnfGVnXFKgK6G1SrUeZ1XvViVAHLkVFCTUURiTGI-1677935397-0-ARj4rf9MYddsVQCCMf1LDBQmhEdLxzTx1sILvCYIQPffBM6W5AOOyWHTmJhLXGSxuHV5ScD6q5WS3rR6np5igVA=; path=/; expires=Sat, 04-Mar-23 13:39:57 GMT; domain=.investing.com; HttpOnly; Secure; SameSite=None'
        
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*,Accept-Encoding: gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46',
        'Origin': 'https://www.investing.com',
        'x-requested-with': 'XMLHttpRequest'
        }
    
    payload = {'header': 'BTC/USD Kraken Historical Data', 'st_date': '12/01/2018', 'end_date': '12/01/2018', 'sort_col': 'date', 'action': 'historical_data', 'smlID': '145284', 'sort_ord': 'DESC', 'interval_sec': 'Daily', 'curr_id': '49799'}
    
    res = requests.post(url, data=payload, headers=headers)    
    print(res)


url = "https://tvc4.investing.com/285ea8f8f1ddd7b0f74c5f9bbe0ae7e2/0/0/0/0/history?symbol=2103&resolution=1&from=1677873442&to=1677878600"
#request_json(url)
req2()