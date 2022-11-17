
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

#Extrai os dados dos ativos do mercado à vista obtido da B3
def extract_stocks(df):
    df2 = df.loc[(df['tp-reg'] == 1) & (df['tp-merc'] == 10)]

    df2 = df2.sort_values(by='data', axis=0, ascending=True, inplace=False, 
                          kind='quicksort', na_position='last')
    #df2 = df2.drop('tp-merc', axis=1)
    df2 = df2.drop('tp-reg', axis=1)
    
    return df2    



###############################################################

def analyze_b3_data():
    dfGlobal = pd.Series(dtype=float)
    for year in range (constants.DATA_YEAR_INIT, constants.DATA_YEAR_END):
    #for year in range (2021, constants.DATA_YEAR_END):
        dfYear = read_data('COTAHIST_A'+str(year)+'.ZIP')
        dfYear = extract_stocks(dfYear)
        #print(dfYear.describe())
        if dfGlobal.size == 0:
            dfGlobal = dfYear
        else:
            dfGlobal = dfGlobal.append(dfYear)
    
    print(dfGlobal.count())
    res = dfGlobal.groupby(["ativo", 'tp-merc']).agg({"volume": ['mean', 'min', 'max', 'count', 'sum']})
    #print(res.head(20))
    res.columns = ['mean', 'min', 'max', 'count', 'sum']
    res = res.reset_index()
    #print(res.head(20))
    res = res.sort_values(by='sum', axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')  

    max_at = res["count"].max()
    print(">>>>>",max_at)
    print(res.head(70))
    res = res.loc[(res["count"] == max_at)]

    print(res.head(51))
    print(res["ativo"].head(51))
    
        
#()
def main():

    analyze_b3_data()

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    