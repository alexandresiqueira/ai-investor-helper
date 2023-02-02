# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 13:46:01 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants
import coletor_b3
import b3_company_detailer

pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 8)
pd.set_option('display.width', 1000)


def supplement_apply(stock):
    dfS                 = coletor_b3.read_stock_indicator_file(stock)
    dfS["factor"]       = 1
    dfS["close-factor"] = dfS["close"] 
    dfD                 = b3_company_detailer.get_dividends(stock)
    dfB                 = b3_company_detailer.get_supplements(stock)
    dfB                 = dfB.loc[(dfB["label"] == "BONIFICACAO")]
    
    
    if dfD.shape[0] > 0:
        dfD.lastDatePriorEx = dfD.lastDatePriorEx.apply(lambda x: x.strftime('%Y%m%d')).astype(int)
    #if stock == "MGLU3":
    print(dfB.head(3))
    if dfB.shape[0] > 0:
        dfB.lastDatePrior = dfB.lastDatePrior.apply(lambda x: x.strftime('%Y%m%d')).astype(int)
    
    dfD["closeAdjusted"] = (1-(dfD['corporateActionPrice']/100)) * dfD['closingPricePriorExDate']
    
    for i in range(dfD.shape[0]):
        new_factor  = 1 - (dfD.iloc[i]["corporateActionPrice"]/100)
        data_       = dfD.iloc[i]["lastDatePriorEx"]
    
        new_df = dfS.apply(lambda x: x.factor*new_factor if x.data <= data_ else x.factor, axis = 1)
        dfS["factor"] = new_df
    
        dfS["close-factor"] = dfS["close"] * dfS["factor"]

    for i in range(dfB.shape[0]):
        new_factor  = 1 / (1 + dfB.iloc[i]["factor"]/100)#regra do manual de opções para bonificação
        new_factor  = round(new_factor, 8)
        data_       = dfB.iloc[i]["lastDatePrior"]
    
        new_df = dfS.apply(lambda x: x.factor*new_factor if x.data <= data_ else x.factor, axis = 1)
        dfS["factor"] = new_df
    
        dfS["close-factor"] = (dfS["close"] * dfS["factor"]).astype(int)


    return dfS


def supplement_apply_all():
    for stock in constants.STOCKS:
        if stock in ["BOVA11", "LAME4", "CESP6"]: #ativos fora da BOVESPA
            print("########## ABORTANDO AJUSTE PARA:",stock)
            continue
        print("AJUSTANDO DIVIDENDOS, JCP E BONIFICACAO:",stock)

        dfS = supplement_apply(stock)
        
        dfS.to_csv(constants.DATA_PATH_STOCKS+stock+"-sup.csv", sep=constants.CSV_SEPARATOR)
        """
        dfS = dfS.loc[(dfS["data"]>=20210701)]
        
        #print(dfS.shape[0])
        print(dfS.head(10))
        print(dfS.tail(20))
        """
def organize_stock_files():
    for stock in constants.STOCKS:
        file_name = constants.DATA_PATH_STOCKS + stock+"-sup.csv"
        if os.path.isfile(file_name):
            df = pd.read_csv(file_name, sep=constants.CSV_SEPARATOR)  
            print(df.columns)
            print(len(df.columns))
            if (len(df.columns) == 10):
                df["close"] = df["close-factor"].astype(int)
                df = df.drop(["factor","close-factor"], axis=1)
            else:
                df = df.drop(["factor"], axis=1)
            df.to_csv(constants.DATA_PATH_STOCKS+"sup/"+stock+".csv", sep=constants.CSV_SEPARATOR)
            
            print(file_name)
        
"""
pd.Series([
    eisenhower_action(priority == 'HIGH', due_date <= cutoff_date)
    for (priority, due_date) in zip(df['priority'], df['due_date'])
  ])
"""

def main():

    organize_stock_files()

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    