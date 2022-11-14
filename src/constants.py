# -*- coding: utf-8 -*-
"""
Created on Tue Nov  1 20:03:33 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

PERIODS_INDICATORS = [5, 10, 20, 50, 200]
PERIODS_RESULTS = [3, 5, 7, 14, 20]
TRAIN_TEST_SPLIT_SIZES = [0.15, 0.2, 0.3]
STOCKS = ["USIM5", "PETR4", "VALE3", "BRKM5", "ITUB4", "BBDC4", "BBAS3"]
ALGORITMS = ["SVM", "LREG", "DTC3", "DTC6", "GNB", "KNN", "RFC"]
BY_CRITERIA_RANK = ["SCO_TEST", "VALID_BAL_PRED", "SCO_VALID"]
DATA_YEAR_INIT=2012
DATA_YEAR_END=2022
DATA_TRAIN_DATE_INIT=20120101
DATA_TRAIN_DATE_END=20170101

DEFAULT_INIT_BALANCE=10000

DATA_PATH="../data/"
MODEL_PATH="../model/"
CSV_SEPARATOR = ';'
FILE_NAME_RESULTADO = '-resultado.csv'
DEFAULT_PERIOD_IND=20
DEFAULT_PERIOD_RES=7
DEFAULT_NORMALIZED=False
DEFAULT_TEST_SIZE=0.2

#https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2012.ZIP
DATA_URL_DOWNLOAD_B3="https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"



#_ativos = [ "BBDC4"]
#PERIODS = [7, 14, 20, 30, 60, 90, 200]
