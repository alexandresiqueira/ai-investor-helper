# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 22:11:57 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import os.path
import pandas as pd
import constants
import model_b3
import coletor_b3
import ai_investor_b3_trainner as ai_investor

def predict(ativo, data=None, open=None, high=None, low=None, close=None, volume=None):
    fname = constants.PATH_B3_TIMESERIES_DAY+ativo+".csv"
    #print("Predict Ativo:", ativo)
    by_criteria="SCO_VALID"
    if os.path.isfile(fname):
        #1 - obter dados do ativo
        df = pd.read_csv(fname, sep=constants.CSV_SEPARATOR)  
        
        if data!= None:
            df.loc[len(df.index)] = [data, ativo, open, high, low, close, volume]
    
        #2 - localiza especificacao do melhor modelo
        res = model_b3.get_best_model_definition(ativo, by_criteria, n_period_result=None)
        
        normalyzed = res["LOG"].iloc[0]

        #3- calcula os indicadores de acordo com as constantes de períodos
        dfAtivo  = coletor_b3.calculate_indicators(df.copy(), applyNormalization=normalyzed)
        
        #4 - carrega o modelo do classificador
        clf = ai_investor.load_model(ativo, algoritmn=res["ALG"].iloc[0], 
                          normalized=res["LOG"].iloc[0], 
                          n_per=res["N_PER"].iloc[0], 
                          n_per_result = res["N_RES"].iloc[0])
        if clf == None:
            print("abortando ativo sem classificador:",ativo)
            return

        #5- limpar todos indicadores que não sao utilizados pelo modelo
        dfAtivo = ai_investor.adjust_technical_indicators(ativo, 
                                                     n_periods=res["N_PER"].iloc[0],  
                                                     normalize=res["LOG"].iloc[0], 
                                                     n_periods_result = res["N_RES"].iloc[0], 
                                                     cotacoes=dfAtivo)
        #6 - remove os dados originais
        dfAtivo = dfAtivo.drop(columns=['data', 'ativo','open', 'close', 'close-orig', 'high', 
                                          'low', 'volume'], axis=1)

        #faz predict do último registro
        dfAtivo = dfAtivo[dfAtivo.shape[0]-1:]

        X = dfAtivo.iloc[0:,0:(dfAtivo.shape[1] - 1)]
        y = clf.predict(X)
        #print("###################",ativo, y)
        return y

def main():
    buy = []
    for ativo in constants.STOCKS:
        y = predict(ativo)        
        print(ativo, y)
        if y[0] == 1:
            buy.append(ativo)
        #break
    print(buy)


print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()        