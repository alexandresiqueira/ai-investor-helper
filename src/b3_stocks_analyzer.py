
# -*- coding: utf-8 -*-
"""
Analisa os arquivos da B3 e gera uma saída contendo os ativos que estiveram presentes
o máximo de vezes (dias) nos pregões, os dados apresentados estão ordenados pelo volume financeiro
negociado em todo período analisado.

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import coletor_b3
import pandas as pd
import constants


#Extrai os dados dos ativos do mercado à vista obtido da B3
def extract_stocks(df):
    df2 = df.loc[(df['tp-reg'] == 1) & (df['tp-merc'] == 10)]

    df2 = df2.sort_values(by='data', axis=0, ascending=True, inplace=False, 
                          kind='quicksort', na_position='last')
    #df2 = df2.drop('tp-merc', axis=1)
    df2 = df2.drop('tp-reg', axis=1)
    
    return df2    



###############################################################

def extract_top_b3_stocks(n_stocks):
    dfGlobal = pd.Series(dtype=float)
    for year in range (constants.DATA_YEAR_INIT, constants.DATA_YEAR_END):
    #for year in range (2021, constants.DATA_YEAR_END):
        dfYear = coletor_b3.read_data('COTAHIST_A'+str(year)+'.ZIP')
        dfYear = extract_stocks(dfYear)
        #print(dfYear.describe())
        if dfGlobal.size == 0:
            dfGlobal = dfYear
        else:
            dfGlobal = dfGlobal.append(dfYear)
    
    print(dfGlobal.count())
    res = dfGlobal.groupby(["ativo", 'tp-merc']).agg({"volume": ['mean', 'min', 'max', 'count', 'sum']})
    res.columns = ['mean', 'min', 'max', 'count', 'sum']
    res = res.reset_index()
    res = res.sort_values(by='sum', axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')  

    max_at = res["count"].max()
    res = res.loc[(res["count"] == max_at)]

    print(res.head(n_stocks))
    
    stocks =     res["ativo"].head(n_stocks)
    str_stocks = ""
    for stock in stocks:
        str_stocks = str_stocks +",\""+stock+"\""
    print(">>>>>>>>>>>>51 ATIVOS MAIS NEGOCIADOS EM TODOS PREGOES -> alimentar constants.py -> STOCKS:")
    print(str_stocks)


def main():

    extract_top_b3_stocks(n_stocks=51)

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    