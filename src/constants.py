# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:03:33 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

#PERIODS_INDICATORS = [5, 10, 20, 50, 200]
#PERIODS_RESULTS = [3, 5, 7, 14, 20]
#TRAIN_TEST_SPLIT_SIZES = [0.15, 0.2, 0.3]
#ALGORITMS = ["SVM", "LREG", "DTC3", "DTC6", "GNB", "KNN", "RFC"]
PERIODS_INDICATORS = [5, 10, 20, 50,200]
PERIODS_RESULTS = [5, 10, 15, 20]
TRAIN_TEST_SPLIT_SIZES = [ 0.1]
ALGORITMS = ["DTC3", "DTC6", "GNB"]
NORMALIZE_OPTIONS = [True, False]

ATRIBS_ORIG = ["data","ativo", "open", "high", "low", "close", "volume", "close-orig"]
ATRIBS_PER = ["EMA", "EMA-dist", "MACD", "MACD-DIFF", "MACD-SIGNAL", "RSI", "SO", "SOS", 
          "TSI", "BBH", "BBHI", "BBL", "BBLI", "BBP", "FI", "SMA-LREG", "BBH-LREG", "BBL-LREG"] 
ATRIBS_RES = ["res",  "res-positive",  "res-perc"]
ATRIBS_REJECT = ["max", "min", "fibo-ret", "SMA", "SMA-dist"]

STOCKS = ["PETR4","VALE3","ITUB4","BBDC4", "BBAS3","PETR3","MGLU3","ITSA4","GGBR4",
           "JBSS3","BRFS3","LREN3","CIEL3","CSNA3","USIM5","RENT3","CCRO3","WEGE3","UGPA3",
           "CMIG4","BRML3","ELET3","RADL3","EQTL3","CSAN3","SBSP3","EMBR3","HYPE3",
           "GOLL4","GOAU4","BBDC3","CYRE3","BRKM5","BRAP4","MULT3","QUAL3","SANB11","MRFG3",
           "MRVE3","ELET6","TOTS3","SULA11","CPFE3","CPLE6","ENBR3","ECOR3","BEEF3","PSSA3"]
#STOCKS = ["ENBR3","CESP6","ECOR3","BEEF3","PSSA3"]
#STOCKS = ["USIM5", "PETR4", "VALE3", "BRKM5", "ITUB4", "BBDC4", "BBAS3"]
#STOCKS = ["PETR4","VALE3","ITUB4","BBDC4","BBAS3","MGLU3","ITSA4","GGBR4"]
#STOCKS = ["BRKM5", "PETR4"]
BY_CRITERIA_RANK = ["SCO_TEST", "VALID_BAL_PRED", "SCO_VALID"]
DATA_YEAR_INIT=2012
DATA_YEAR_END=2023
DATA_TRAIN_DATE_INIT=20190101
DATA_TRAIN_DATE_END=20220101

DEFAULT_INIT_BALANCE=10000
ROOT_PATH="D:/data/b3/"
#ROOT_PATH="../data/"
DATA_PATH=ROOT_PATH
DATA_PATH_RESULTS=DATA_PATH+"results/"
DATA_PATH_STOCKS=DATA_PATH+"timeseries/day/sup/"
DATA_PATH_SERIES=DATA_PATH+"series/"
DATA_PATH_COMPANIES=DATA_PATH+"companies/"
MODEL_PATH=ROOT_PATH+"model/"


#DATA_PATH_STOCKS=DATA_PATH
#DATA_PATH_SERIES=DATA_PATH


CSV_SEPARATOR = ';'
FILE_NAME_RESULTADO = '-resultado.csv'
DEFAULT_PERIOD_IND=20
DEFAULT_PERIOD_RES=7
DEFAULT_NORMALIZED=False
DEFAULT_TEST_SIZE=0.2

#https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2012.ZIP
#urls base64 para json sobre proventos dos ativos
#https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/eyJpc3N1aW5nQ29tcGFueSI6IlBFVFIiLCJsYW5ndWFnZSI6InB0LWJyIn0=
URL_COMPANY_DETAIL="https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetDetail/" #eyJjb2RlQ1ZNIjoiOTUxMiIsImxhbmd1YWdlIjoicHQtYnIifQ==
URL_COMPANY_SUPPLEMENT="https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedSupplementCompany/" #GetListedCashDividends/eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjIwMCwidHJhZGluZ05hbWUiOiJQRVRST0JSQVMifQ==
URL_CASH_DIVIDENDS="https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetListedCashDividends/" #eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjIwMCwidHJhZGluZ05hbWUiOiJQRVRST0JSQVMifQ==
URL_GET_COMPANIES="https://sistemaswebb3-listados.b3.com.br/listedCompaniesProxy/CompanyCall/GetInitialCompanies/" #eyJsYW5ndWFnZSI6InB0LWJyIiwicGFnZU51bWJlciI6MSwicGFnZVNpemUiOjIwfQ==

URL_DOWNLOAD_B3="https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
URL_INTRADAY_DOWNLOAD = "https://arquivos.b3.com.br/apinegocios/tickercsv/"

PATH_B3_INTRADAY_LOCAL = "D:/data/b3/intraday/"
PATH_B3_SERIES_LOCAL = "D:/data/b3/series/"
PATH_B3_TIMESERIES_DAY = "D:/data/b3/timeseries/day/sup/"
FILE_INTRADAY_PREFIX = "TradeIntraday_"
TIMEFRAMES = [1, 2, 5, 15, 30]

GENERATE_TREE_GRAPH = False

#_ativos = [ "BBDC4"]
#PERIODS = [7, 14, 20, 30, 60, 90, 200]

#STOCKS = ["PETR4","VALE3","ITUB4","BBDC4","BOVA11","BBAS3","PETR3","MGLU3","ITSA4","GGBR4","MRVE3","ELET6"]
#STOCKS = ["JBSS3","BRFS3","LREN3","CIEL3","CSNA3","USIM5","RENT3","CCRO3","WEGE3","UGPA3","SULA11","CPFE3","CPLE6","PSSA3"]
#STOCKS = ["LAME4","CMIG4","BRML3","ELET3","RADL3","EQTL3","CSAN3","SBSP3","EMBR3","HYPE3","ENBR3","CESP6","ECOR3"]
#STOCKS = ["GOLL4","GOAU4","BBDC3","CYRE3","BRKM5","BRAP4","MULT3","QUAL3","SANB11","MRFG3","TOTS3","BEEF3"]

