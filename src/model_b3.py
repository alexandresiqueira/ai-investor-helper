# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:25:10 2022

Script para identificar o melhor resultado por artivo e gravar um arquivo 
/model/<ATIVO>-<PARAMETROS>.joblib
para posterior execução

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""

import ai_investor_b3_trainner as ai_investor
import result_analyse as ra
import coletor_b3 as cb3
import constants
import pandas as pd

pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 2)

#Obtém o melhor resultado praa cada ATIVO contigo em constants.STOCKS conforme 
# critério (atributo) definido no parâmetro by_criteria (SCO_TEST, SCO_VALID, VALID_BAL_PRED, etc )
def save_best_models(by_criteria, n_period_result=constants.DEFAULT_PERIOD_RES, 
                     dt_init=constants.DATA_TRAIN_DATE_INIT, 
                     dt_end=constants.DATA_TRAIN_DATE_END):
    print("############INICIANDO GERAÇÃO DE MODELOS POR " , by_criteria,";n_period_result:",n_period_result, " ###########")
    res = ra.read_resultado()
    ai_investor.create_classifiers()
    for ativo in constants.STOCKS:
        res_ativo = res.loc[(res["ATIVO"] == ativo)]
        res_ativo_sorted = ra.sort_resultado_by_criteria(res_ativo, by_criteria, n_period_result)
        #print(res_ativo_sorted.head(1))
        print(ativo,
              "-MELHOR - ALG:"+res_ativo_sorted["ALG"].iloc[0],
              "VALID_BAL_PRED:",res_ativo_sorted["VALID_BAL_PRED"].iloc[0],
              "VALID_BAL_HOLD:",res_ativo_sorted["VALID_BAL_HOLD"].iloc[0],
              "SCO_VALID:",res_ativo_sorted["SCO_VALID"].iloc[0],
              "SCO_TEST:",res_ativo_sorted["SCO_TEST"].iloc[0],
              "LOG:",res_ativo_sorted["LOG"].iloc[0],
              "N_PER:",res_ativo_sorted["N_PER"].iloc[0],
              "N_RES:",res_ativo_sorted["N_RES"].iloc[0],
              ";test_size:",res_ativo_sorted["TEST_SIZE"].iloc[0])
        #resp = res_ativo_sorted[["ALG", "N_RES", "LOG", "SCO_VALID"]].iloc[0]
        #print(resp.head(1))
        ai_investor.create_and_save_model(ativo, algoritmn=res_ativo_sorted["ALG"].iloc[0], 
                                  normalized=res_ativo_sorted["LOG"].iloc[0], 
                                  n_per=res_ativo_sorted["N_PER"].iloc[0], 
                                  n_per_result = res_ativo_sorted["N_RES"].iloc[0],
                                  dt_init=dt_init, dt_end=dt_end, 
                                  test_size=res_ativo_sorted["TEST_SIZE"].iloc[0])

        
def predic_stocks(ativo, algoritm, normalized, n_per, n_per_result, cotacoes):
    clf = ai_investor.load_model(ativo, algoritmn=algoritm, 
                              normalized=normalized, 
                              n_per=n_per, 
                              n_per_result = n_per_result)
    cotacoes = cb3.calculate_indicators(cotacoes)


def get_best_model_definition(ativo, by_criteria, n_period_result=constants.DEFAULT_PERIOD_RES):
    res = ra.read_resultado()
    res_ativo = res.loc[(res["ATIVO"] == ativo)]
    res_ativo_sorted = ra.sort_resultado_by_criteria(res_ativo, by_criteria, n_period_result)
    return res_ativo_sorted
    

def get_best_model(ativo, by_criteria, n_period_result=constants.DEFAULT_PERIOD_RES):
    res_ativo_sorted = get_best_model_definition(ativo, by_criteria, n_period_result)
    clf = ai_investor.load_model(ativo, algoritmn=res_ativo_sorted["ALG"].iloc[0], 
                              normalized=res_ativo_sorted["LOG"].iloc[0], 
                              n_per=res_ativo_sorted["N_PER"].iloc[0], 
                              n_per_result = res_ativo_sorted["N_RES"].iloc[0])
    return clf
        # break
def predic_best_models():
    res = ra.read_resultado()
    for ativo in constants.STOCKS:
        res_ativo = res.loc[(res["ATIVO"] == ativo)]
        res_ativo_sorted = ra.sort_resultado(res_ativo)
        #print(res_ativo_sorted.head(1))
        #print(ativo,"-melhor:"+res_ativo_sorted["ALG"].iloc[1])
        cotacoes = ai_investor.read_file_stock(ativo,  n_periods=res_ativo_sorted["N_PER"].iloc[0],
                                       normalize=res_ativo_sorted["LOG"].iloc[0], 
                                       half_sample= False,
                                       n_periods_result = res_ativo_sorted["N_RES"].iloc[0], 
                                       dt_init=constants.DATA_TRAIN_DATE_INIT, 
                                       dt_end=constants.DATA_TRAIN_DATE_END)
        
        #print(">>>shape antes de validar:",cotacoes.shape)
        #cotacoes = cotacoes.iloc[cotacoes.shape[0]-1:,0:(cotacoes.shape[1])]
        #cotacoes = cotacoes.iloc[cotacoes.shape[0]-2:,0:(cotacoes.shape[1])]
        end_row = 150
        cotacoes = cotacoes.iloc[(cotacoes.shape[0])-end_row:, 0:(cotacoes.shape[1])]
        #cotacoes = cotacoes.loc[(cotacoes["res-positive-20"] == "False")]
        #print(cotacoes)
        clf = get_best_model(ativo, algoritmn=res_ativo_sorted["ALG"].iloc[0], 
                                  normalized=res_ativo_sorted["LOG"].iloc[0], 
                                  n_per=res_ativo_sorted["N_PER"].iloc[0], 
                                  n_per_result = res_ativo_sorted["N_RES"].iloc[0])
        #X = cotacoes.iloc[cotacoes.shape[0]-1:,0:(cotacoes.shape[1]-1)]
        #print(cotacoes.shape)
        X = cotacoes.iloc[0:end_row-20,0:(cotacoes.shape[1]-1)]
        #y_valid = cotacoes.iloc[0:50,(cotacoes.shape[1])]
        y_valid = (cotacoes.iloc[:end_row-20,(cotacoes.shape[1] - 1)])
        y = clf.predict(X)
        print(">>>>>>>>>>>PREDICT-Y-",ativo,":")
        print(y)
        print(">>>>>>>>>>>PREDICT-Y-valid",ativo,":")
        print(y_valid.iloc[0])
        y_valid = y_valid == "True" 
        y_valid = y_valid.astype(int) 
        y_valid = y_valid.to_numpy()
        print(type(y))
        print(type(y_valid))
        print(y_valid)
        print(">>>>>>>>>>>>>>>>>>>", ativo)
        print((y_valid) -( y))
        qt = ((y_valid) -( y)) != 0
        total_acerto = qt.astype(int).sum()
        print("Resultado - ", ativo, ":",total_acerto, "; de total testes:",qt.size, ";precent:",(total_acerto/qt.size))

        #break

def save_models():
    for criteria in constants.BY_CRITERIA_RANK:
        save_best_models(criteria, None)
    

def main():
    pd.set_option('display.max_columns', 700)
    pd.set_option('display.width', 1000)
    save_models()
    #predic_best_models()
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    
