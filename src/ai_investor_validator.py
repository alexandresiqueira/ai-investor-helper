# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 20:05:32 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import ai_investor_b3_trainner as ai_trainner
import result_analyse as ra
import coletor_b3 as cb3
import model_b3
import pandas as pd
import matplotlib.pyplot as plt
import constants
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score



pd.set_option('display.max_columns', 700)
pd.set_option('display.width', 1000)

def my_rolling_dif(x):
    return x.iloc[-1] - x.iloc[0]

def read_data_predic_and_compare(ativo, res_ativo_sorted, by_criteria, n_period_result, 
                                 date_exec_init = constants.DATA_TRAIN_DATE_END):

    dfStock = cb3.read_stock_indicator_file(ativo)
    #print(dfStock.tail(1))
    n_period_result = res_ativo_sorted["N_RES"].iloc[0]
    
    y, df2C = __predict(ativo, dfStock, res_ativo_sorted, by_criteria, n_period_result, date_exec_init)

    dfStock = dfStock.drop(columns=["volume", "low","high", "open"])
    dfStock = dfStock.loc[(dfStock["data"] > date_exec_init)]
    dfStock["close-orig"] = df2C["close-orig"]
    #le = LabelEncoder()
    #y_valid = le.fit_transform(df2C["res-positive-"+str(n_period_result)].to_numpy())
    #acc_score_valid = accuracy_score(y_valid, y)
    #print(">>>score:",acc_score_valid)
    dfStock = calc_buy_and_hold(dfStock, constants.DEFAULT_INIT_BALANCE, "close-orig")

    dfStock = calc_return_predic(dfStock, y, constants.DEFAULT_INIT_BALANCE, n_period_result, "close-orig")

    return  dfStock, n_period_result

def calc_buy_and_hold(dfStock, init_balance, col_close_name="close-orig"):    
    close_init = dfStock[col_close_name].iloc[0]
    quant_stock = init_balance / close_init
    dfStock["bal-hold"] = dfStock[col_close_name] * quant_stock
    return dfStock

def calc_irrf_operation(result):
    if result > 0:
        return result*0.0005
    
    return 0;
    
#Calcula o retorno financeiro após obter os resultados 
def calc_return_predic(dfStock, res_period_pred, init_balance, n_per_operation, col_close_name="close-orig"):
    #print("cotacoes antes:", dfStock.shape)
    
    dfStock = dfStock.iloc[dfStock.shape[0]- len(res_period_pred):,:].copy()

    close = dfStock[col_close_name].to_numpy()
    dfStock.loc[:,"pred-"+str(n_per_operation)] = res_period_pred
    dfStock.loc[:,"exec-"+str(n_per_operation)] = 0
    dfStock.loc[:,"res-"+str(n_per_operation)] = 0
    dfStock.loc[:,"irrf-"+str(n_per_operation)] = 0
    dfStock.loc[:,"bal-pred-"+str(n_per_operation)] = res_period_pred
    #print("length close:", len(close), ";length pred:",len(res_period_pred))
    isInOperation = False
    balance = init_balance
    operPeriods = 0
    quant_stock = 0
    
    for pos in range(len(res_period_pred)):
        pred = res_period_pred[pos]
        if ((pred == 1) & (isInOperation == False) ): #inicia operacao
            isInOperation = True
            quant_stock = balance / close[pos]
            dfStock.iloc[[pos], dfStock.columns.get_loc("exec-"+str(n_per_operation))] = 1
        if isInOperation:
            operPeriods = operPeriods + 1
            balance = quant_stock * close[pos]
        if isInOperation & (operPeriods > n_per_operation):
            isInOperation = False
            dfStock.iloc[[pos], dfStock.columns.get_loc("exec-"+str(n_per_operation))] = 2

            result_oper = balance - dfStock["bal-pred-"+str(n_per_operation)].iloc[pos - n_per_operation]
            dfStock.iloc[[pos], dfStock.columns.get_loc("res-"+str(n_per_operation))] = result_oper
            dfStock.iloc[[pos], dfStock.columns.get_loc("irrf-"+str(n_per_operation))] = calc_irrf_operation(quant_stock * close[pos])
            
            operPeriods = 0
            quant_stock = 0
        
        #dfStock["bal-pred-"+str(n_per_operation)].iloc[pos] = balance 
        dfStock.iloc[[pos], dfStock.columns.get_loc("bal-pred-"+str(n_per_operation))] = balance
        
    return dfStock


def plot_operation(ativo, df, n_per_operation, title):
    
    plt.figure(figsize=(12, 5))
    ax = plt.axes()
    plt.title(title)
    df["date"] = pd.to_datetime(df['data'], format='%Y%m%d')
    plt.xlabel("date")
    #plt.ylabel("close");
    
    #x = np.linspace(0, 10, 1000)
    #ax.plot(df["data"], df[ "close"], label="close" );
    ax.grid(axis='y')
    ax.plot(df["date"], df[ "bal-hold"], label="Buy Hold" );
    ax.plot(df["date"], df[ "bal-pred-"+str(n_per_operation)], label="bal-pred-"+str(n_per_operation) );
    #ax.plot(df["data"], df[ "EMA-30"], label="EMA-30" );
    plt.legend()
    plt.show()
    
    
def __predict(ativo, dfStock, res_ativo_sorted, by_criteria, n_period_result, date_exec_init = constants.DATA_TRAIN_DATE_END):


    #1 - Calcular todos indicadores
    dfPred = cb3.calculate_indicators(dfStock.copy(), 
                                      applyNormalization=res_ativo_sorted["LOG"].iloc[0])
    

    #4 - ler o modelo já treinado
    clf = model_b3.get_best_model(ativo, by_criteria, None)

    #3- limpar todos indicadores que não sao utilizados pelo modelo
    dfPred = ai_trainner.adjust_technical_indicators(ativo, 
                                                     n_periods=res_ativo_sorted["N_PER"].iloc[0],  
                                                     normalize=res_ativo_sorted["LOG"].iloc[0], 
                                                     half_sample=False, 
                                                     n_periods_result = res_ativo_sorted["N_RES"].iloc[0], 
                                                     cotacoes=dfPred)
    return __predict_for_validation(dfStock, dfPred, date_exec_init, 
                                  res_ativo_sorted["N_RES"].iloc[0], clf)

def __predict_for_validation(dfStock, dfPred, date_exec_init, n_per_operation, clf):    
    dfPred = dfPred.loc[(dfStock["data"] > date_exec_init)]
    #print(dfPred.head(1))
    dfPred = dfPred.drop(columns=["data", "ativo", "close", "volume", "low","high", 
                                  "open"])
    #print("cotacoes antes - predict:", dfPred.shape)
    dfPred = dfPred.dropna()
    
    #manter dados para validacao posterior do modelo utilizado:
    df2C = pd.Series(dtype=float)
    df2C["close-orig"] = dfPred["close-orig"]
    df2C["res-positive-"+str(n_per_operation)] = dfPred["res-positive-"+str(n_per_operation)]
    dfPred = dfPred.drop(columns=["close-orig", "res-positive-"+str(n_per_operation)])
    
    #print("\nCampos de Resultado:\n{0}\n".format(list(dfPred.keys())))
    res_period_pred = clf.predict(dfPred)
    
    return res_period_pred, df2C



def main():
    
    for ativo in constants.STOCKS:
        for criteria in constants.BY_CRITERIA_RANK:
            #2-identificar e carregar o modelo que melhor se adequou ao ativo nos treinos
            res_ativo_sorted = model_b3.get_best_model_definition(ativo, criteria,
                                                                  n_period_result=None)
            title = ativo +" - ALGOR.:"+res_ativo_sorted["ALG"].iloc[0] + " - PERIOD:"+ str(res_ativo_sorted["N_PER"].iloc[0]) + " - NORM:" + str(res_ativo_sorted["LOG"].iloc[0])+" - CRIT:"+criteria
            
            print(res_ativo_sorted.head(1))
            dfStock, n_period_result = read_data_predic_and_compare(ativo, res_ativo_sorted, criteria, None)        
            plot_operation(ativo, dfStock, n_period_result, title)

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    
