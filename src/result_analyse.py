# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:25:57 2022

Script que apresenta gráficos de análise dos diversos modelos executados.

As análises realizadas neste script dependem da existência do arquivo de resultados
consolidado de todos ativos em:
    constants.DATA_PATH+constants.FILE_NAME_RESULTADO

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom


@date	  17 Outubro 2022
@version 1.0"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import constants
import matplotlib.lines as mlines
import os.path
np.set_printoptions(threshold=None, precision=4)
pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 4)
pd.set_option('display.width', 1000)



def read_resultado():
    fname = constants.DATA_PATH+constants.FILE_NAME_RESULTADO
    
    if os.path.isfile(fname):
        resultado = pd.read_csv(fname, sep=constants.CSV_SEPARATOR)
         
        return resultado
    print("ALERT: - ARQUIVO DE RESULTADOS NÃO LOCALIZADO ", fname)

#Faz print dos resultados obtidos para os ativoss, algoritmos, n_res, etc.
def print_res_alg():
    res = read_resultado()
    #ATRIB = "% PRED/HOLD" #
    ATRIB = "SCO_VALID"
    res["% PRED/HOLD"] = ((res["VALID_BAL_PRED"]/res["VALID_BAL_HOLD"])-1)*100

    #res = res.loc[(res["ALG"] != "SVM") & (res["ALG"] != "RFC")]

    #res = res.loc[(res["ATIVO"] != "VALE3") ]
    atributos = [ "ATIVO", "LOG","ALG","N_RES","N_PER", "TEST_SIZE"]
    res2 = res.agg({ATRIB: ['mean', 'min', 'max', 'count', 'std']})
    print(res2)
    for atrib in atributos:
        res2 = res.groupby([atrib]).agg({ATRIB: ['mean', 'min', 'max', 'count', 'std']})
        res2.columns = ['mean', 'min', 'max', 'count', 'std']
        res2 = res2.reset_index()
        res2 = res2.sort_values(by='mean', axis=0, ascending=False, inplace=False,  
                         kind='quicksort', na_position='last')  
        print("---------------------------------------")
        print(res2)
    """
    res2 = res.groupby(["ALG", "LOG"]).agg({ATRIB: ['mean', 'min', 'max', 'count']})
    print(res2)
    """
    res2 = res.groupby(["ATIVO", "ALG", "N_RES", "LOG"]).agg({ATRIB: ['mean', 'min', 'max', 'count', 'std']})
    res2.columns = ['mean', 'min', 'max', 'count', 'std']
    res2 = res2.reset_index()
    res2 = res2.sort_values(by='mean', axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')  
    print(res2.head(50))
    
    res3 = res.groupby(["ALG","N_RES", "LOG"]).agg({ATRIB: ['mean', 'min', 'max', 'count']})
    res3.columns = ['mean', 'min', 'max', 'count']
    res3 = res3.reset_index()
    res3 = res3.sort_values(by='mean', axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')  

    print(res3)



#identifica máximo desempenho por critério: "SCO_TEST", "VALID_BAL_PRED", "SCO_VALID"
def compute_bets_results():
    res = read_resultado()

    bestRes = pd.Series(dtype=float)
    for criteria in constants.BY_CRITERIA_RANK:
        idx = res.groupby(['ATIVO'])[criteria].transform(max) == res[criteria]
        resp = res[idx][["ATIVO", "N_PER", "ALG", "LOG", "N_RES", "TEST_SIZE", 
                         "VALID_BAL_HOLD", "SCO_VALID", 
                         "SCO_TEST", "VALID_BAL_PRED"]]
        
        resp["CRITERIA"] = criteria
        
        for criteria2 in constants.BY_CRITERIA_RANK:
            if criteria == criteria2:
                continue
            idx = resp.groupby(['ATIVO'])[criteria2].transform(max) == resp[criteria2]
            resp = resp[idx]
        
        if bestRes.size == 0:
            bestRes = resp
        else:
            bestRes = bestRes.append(resp)
    bestRes["% PRED/HOLD"] = ((bestRes["VALID_BAL_PRED"]/bestRes["VALID_BAL_HOLD"])-1)*100
    #print(bestRes.loc[(bestRes["CRITERIA"] == "SCO_VALID")]["% PRED/HOLD"].mean())
    
    #Análise apenas por score em base de validação:
    bestRes = bestRes.loc[(bestRes["CRITERIA"] == "SCO_VALID")]
    bestRes = bestRes.drop("CRITERIA", axis=1)
    bestRes = bestRes.sort_values(by='SCO_VALID', axis=0, ascending=False, inplace=False,  
                     kind='quicksort', na_position='last')
    print("\n##########################################  MÁXIMOS DESEMPENHOS POR ATIVO  ########################################\n")
    print(bestRes)
    bestRes.to_excel(constants.DATA_PATH+"report-ativos.xlsx")
    
    bestRes2 = bestRes.agg({"SCO_TEST": ['mean', 'min', 'max', 'count'],"SCO_VALID": ['mean', 'min', 'max', 'count'], "% PRED/HOLD": ['mean', 'min', 'max', 'count']})
    print("\n########### MÉDIA GERAL DOS MELHORES RESULTADOS DE VALIDAÇÃO ##########")
    print(bestRes2)

    atributos = [ "ALG","N_RES","N_PER", "TEST_SIZE", "LOG"]
    for atrib in atributos:

        res3 = bestRes.groupby([atrib]).agg({"SCO_TEST": ['mean', 'min', 'max', 'count'],"SCO_VALID": ['mean', 'min', 'max', 'count'], "% PRED/HOLD": ['mean', 'min', 'max', 'count']})
        """res3.columns = ['mean', 'min', 'max', 'count']
        res3 = res3.reset_index()
        res3 = res3.sort_values(by='mean', axis=0, ascending=False, inplace=False,  
                         kind='quicksort', na_position='last')  
        """
        print("\n\n############### MÉDIA GERAL DOS MELHORES RESULTADOS DE VALIDAÇÃO POR ",atrib," ##################")
        print(res3)
        res3.to_excel(constants.DATA_PATH+"report-"+atrib+".xlsx")

    bestRes2 = bestRes.groupby(["ALG", "LOG"]).agg({"SCO_TEST": ['mean', 'min', 'max', 'count'],"SCO_VALID": ['mean', 'min', 'max', 'count'], "% PRED/HOLD": ['mean', 'min', 'max', 'count']})
    print("\n\n######### MÉDIA GERAL DOS MELHORES RESULTADOS DE VALIDAÇÃO POR ALGORITMO E NORMALIZ. ##########")
    print(bestRes2)


    return bestRes

#Gera histograma do score de test (SCO_TEST) dos resultados obtidos
def plot_resultado(resultados, period, ativo=""):
    resultados.hist(column='SCO_TEST',    # Coluna a ser plotada
                       figsize=(9,6),   # Tamanho do gráfico
                       bins=20)         # Numero de colunas do histogram
    


#Faz o plt de um ativo em um grafico contendo data, preço de fechamento m média exponencial e bandas de bolinger
def plot_ativo(resultado, ativo, normalized=constants.DEFAULT_NORMALIZED, test_size=constants.DEFAULT_TEST_SIZE, 
               period=constants.DEFAULT_PERIOD_RES):
    df = pd.Series(dtype=object)

    df = resultado    
    if ativo != "TOTAL":
        df = resultado.loc[(resultado["ATIVO"] == ativo) ]    
    
    df = df.loc[(resultado["LOG"] == normalized) & (resultado["TEST_SIZE"] == test_size) ]    

    fig, ax = plt.subplots(5, 2, figsize=(10,14))
    plt.suptitle("Acurácia dos algoritmos versus quantidade de atributos, para n períodos \n "+ativo+" - NORMALIZED:"+str(normalized)+"  - TEST SIZE:"+str(test_size))
    
    i = 0
    for i in range(7):
        for per in constants.PERIODS_RESULTS:
            df1 = df.loc[(df["ALG"] == constants.ALGORITMS[i]) ]
            df1 = df1.loc[(df1["N_RES"] == per)]
            #min_reg = df1["INST."].min()
            #df3 = df1.loc[(df1["INST."] != min_reg)]
            df3 = df1
            pos = i
            if i > 3:
                pos = i - 4
    
            ax[pos, int(i/4)].plot(df3["ATRIBS"], df3["SCO_TEST"], label=constants.ALGORITMS[i]+"-"+str(per));
            ax[pos, int(i/4)].legend()
            ax[pos, int(i/4)].title.set_text(constants.ALGORITMS[i])
            ax[pos, int(i/4)].grid(True)
    
    
    ########INICIO PLOT DAS ESTATÍSTICAS TOTAIS DO ATIVO############
    dfx = df
    dfx= dfx.groupby(["ATRIBS"]).agg({'SCO_TEST': ['mean', 'min', 'max']})
    ax[3, 1].plot(dfx["SCO_TEST"].index, dfx["SCO_TEST"]["max"], label="Máxima");
    ax[3, 1].plot(dfx["SCO_TEST"].index, dfx["SCO_TEST"]["mean"], label="Média");
    ax[3, 1].plot(dfx["SCO_TEST"].index, dfx["SCO_TEST"]["min"], label="Mínima");
    ax[3, 1].legend()
    ax[3, 1].title.set_text("Acurácia Total versus Quantidade de atributos")
    ax[3, 1].grid(True)


    
    ########PLOT DA ACURÁCIA MÉDIA POR ALGORITMO ATIVO############
    for alg in constants.ALGORITMS:
        df1 = df
        df1 = df1.loc[(df1["ALG"] == alg)]
        dfx= df1.groupby(["ATRIBS"]).agg({'SCO_TEST': ['mean']})
        ax[4, 0].plot(dfx["SCO_TEST"].index, dfx["SCO_TEST"]["mean"], label=alg);
        ax[4, 0].legend()
    ax[4, 0].title.set_text("Acurácia Média - Atributos versus Algoritmo ")
    ax[4, 0].grid(True)


    ########PLOT DA ACURÁCIA MÉDIA POR TEMPO DE HOLD ATIVO############
    for per in constants.PERIODS_RESULTS:
        df1 = df
        df1 = df1.loc[(df1["N_RES"] == per)]
        dfx= df1.groupby(["ATRIBS"]).agg({'SCO_TEST': ['mean', 'min', 'max']})
        ax[4, 1].plot(dfx["SCO_TEST"].index, dfx["SCO_TEST"]["mean"], label="TH-"+str(per));
        ax[4, 1].legend()
    ax[4, 1].title.set_text("Acurácia Média - Atributos versus Tempo de Hold")
    ax[4, 1].grid(True)


    plt.legend()
    plt.show()


"""
"""
def plot_global_result(resultado, atrib_res):

    fig, ax = plt.subplots(3, 1, figsize=(6,10))
    plt.suptitle("Acurácia versus quantidade de atributos, para n períodos\n"+ atrib_res)

    ########INICIO PLOT DAS ESTATÍSTICAS TOTAIS############
    df = resultado
    dfx = resultado
    dfx= dfx.groupby(["ATRIBS"]).agg({atrib_res: ['mean', 'min', 'max']})
    ax[0].plot(dfx[atrib_res].index, dfx[atrib_res]["max"], label="Máxima");
    ax[0].plot(dfx[atrib_res].index, dfx[atrib_res]["mean"], label="Média");
    ax[0].plot(dfx[atrib_res].index, dfx[atrib_res]["min"], label="Mínima");
    ax[0].legend()
    ax[0].title.set_text("Acurácia Total versus Quantidade de atributos")
    ax[0].grid(True)


    
    ########PLOT DA ACURÁCIA MÉDIA POR ALGORITMO ATIVO############
    df_alg = pd.Series(dtype=(float))
    for alg in constants.ALGORITMS:
        df1 = df
        df1 = df1.loc[(df1["ALG"] == alg)]
        dfx= df1.groupby(["ATRIBS"]).agg({atrib_res: ['mean', 'min', 'max']})
        ax[1].plot(dfx[atrib_res].index, dfx[atrib_res]["mean"], label=alg);
        ax[1].legend()
        dfx["ALG"] = alg
        if df_alg.size == 0:
            df_alg = dfx
        else:
            df_alg = df_alg.append(dfx)
    
    print("\n#####",atrib_res,":ACURACIA MÉDIA MÁXIMA \nPOR PERÍODOS E ALGORITMOS ####")
    print_max_sco_test(df_alg, True, atrib_res)

    ax[1].title.set_text("Acurácia Média - Atributos versus Algoritmo ")
    ax[1].grid(True)


    ########PLOT DA ACURÁCIA MÉDIA POR TEMPO DE HOLD ATIVO############
    df_time_hold = pd.Series(dtype=(float))
    for per in constants.PERIODS_RESULTS:
        df1 = df
        df1 = df1.loc[(df1["N_RES"] == per)]
        dfx= df1.groupby(["ATRIBS"]).agg({atrib_res: ['mean', 'min', 'max']})
        dfx["N_RES"] = per
        if df_time_hold.size == 0:
            df_time_hold = dfx
        else:
            df_time_hold = df_time_hold.append(dfx)
        ax[2].plot(dfx[atrib_res].index, dfx[atrib_res]["mean"], label="TH-"+str(per));
        ax[2].legend()
        
    ax[2].title.set_text("Acurácia Média - Atributos versus Tempo de Hold")
    ax[2].grid(True)

    print("\n#####",atrib_res,":ACURACIA MÉDIA MÁXIMA \nPOR PERÍODOS E TEMPO OPERAÇÃO (N_RES) ####")
    print_max_sco_test(df_time_hold, True, atrib_res)

    print("\n#####ACURACIA PARA RESULTADO EM ",constants.DEFAULT_PERIOD_RES," PERÍODOS E ATRIBUTOS - GLOBAL####")
    df1 = df
    max_df = df1["ATRIBS"].max()
    df1 = df1.loc[(df1["N_RES"] == constants.DEFAULT_PERIOD_RES) & (df1["ATRIBS"] == max_df)]
    #print(df1)
    df1= df1.groupby(["N_RES", "ALG"]).agg({atrib_res: ['mean', 'min', 'max']})
    print_max_sco_test(df1, False, atrib_res)

    plt.legend()
    plt.show()

def print_max_sco_test(df, filter_max=True, atrib_res="SCO_TEST"):  
    max_df = df.index.max()
    if filter_max:
        df = df.loc[(df.index == max_df)].copy()
    if len(df.columns) == 4:
        df.columns = ["MEAN", "MIN","MAX", df.columns[3][0]]
    else:
        df.columns = ["MEAN", "MIN","MAX"]
        
    df = df.reset_index()
    """
    df["MEAN"] = df[atrib_res]["mean"]
    df["MAX"] = df[atrib_res]["max"]
    df["MIN"] = df[atrib_res]["min"]
    #df.drop(2, axis=1)
    df = df.drop([atrib_res], axis=1)
    """
    df = df.sort_values(by='MEAN', axis=0, ascending=False, inplace=False,  
                          kind='quicksort', na_position='last')    
    print(df.head(15))
    
#deprecated: plota scatter registros por resultado
def __plot_scatter(normalized,test_size, res):
    res = read_resultado()
    for ativo in constants.STOCKS:
        #res_ativo = res.loc[(res["ATIVO"] == ativo) & (res["LOG"] == normalized) & (res["CM01"] == 0) ]
        res_ativo = res.loc[(res["ATIVO"] == ativo) & (res["LOG"] == normalized) ]
        # Plotting point using sactter method
        fig, ax = plt.subplots(4, 2, figsize=(10,14))
        plt.suptitle(ativo)
        for i in range(len(constants.ALGORITMS)):
            X = res_ativo["INST."]
            Y = res_ativo["N_RES"]
            #ax[int(i\2), int(i\4)].plot(X, Y, label=algoritms[i])
            ax[int(i%4), int(i/4)].scatter(X, Y, label=constants.ALGORITMS[i]);
            ax[int(i%4), int(i/4)].title.set_text(constants.ALGORITMS[i])
            #plt.scatter(X,Y)
        X = res_ativo["INST."]
        Y = res_ativo["N_RES"]
        ax[3, 1].scatter(X, Y);
        ax[3, 1].title.set_text("TODOS ALGORITMOS - NORMALIZADO:"+str(normalized)+"TEST_SIZE"+str(test_size))
        plt.show()

#Inicia o processo de apresentação de boxplot para o conjunto de dados exitente em res
# por ATIVO. As análises geradas por ativo são:
# 1. N_RES x ALGORITMO
# 2. N_RES x N_PER
# 3. N_RES x TEST_SIZE
#
def plot_boxplots(res, normalized = True, test_size=constants.DEFAULT_TEST_SIZE):

    if test_size != None:
        res = res.loc[(res["TEST_SIZE"] == test_size)]
    
    for ativo in constants.STOCKS:
        res_ = res.loc[(res["ATIVO"] == ativo)]
        plot_boxplot(ativo, res_, normalized, "ALG", constants.ALGORITMS)
        plot_boxplot(ativo, res_,normalized, "N_PER", range(1,len(constants.PERIODS_INDICATORS)+1))
        plot_boxplot(ativo, res_,normalized, "TEST_SIZE", constants.TRAIN_TEST_SPLIT_SIZES)
        plot_boxplot(ativo, res_,normalized, "LOG", constants.NORMALIZE_OPTIONS)
    #res = res.loc[(res["TEST_SIZE"] == constants.DEFAULT_TEST_SIZE) & (res["ATIVO"] != "VALE3")]
    plot_boxplot("TODOS ATIVOS", res, normalized, "ALG", constants.ALGORITMS)
    plot_boxplot("TODOS ATIVOS", res,normalized, "N_PER", range(1,len(constants.PERIODS_INDICATORS)+1))
    plot_boxplot("TODOS ATIVOS", res,normalized, "TEST_SIZE", constants.TRAIN_TEST_SPLIT_SIZES)
    plot_boxplot("TODOS ATIVOS", res,normalized, "LOG", constants.NORMALIZE_OPTIONS)


#função auxiliar para criar subplot
def plot_subplot(ax, pos_1, pos_2, value_red, value_green, data, title):
    ax[pos_1, pos_2].boxplot(data);
    ax[pos_1, pos_2].set_xticklabels(constants.PERIODS_RESULTS)    
    
    line = mlines.Line2D([0, len(constants.PERIODS_RESULTS)+1], [value_red, value_red], color='red')
    lineg = mlines.Line2D([0, len(constants.PERIODS_RESULTS)+1], [value_green, value_green], color='green')
    ax[pos_1, pos_2].add_line(line)
    ax[pos_1, pos_2].add_line(lineg)

    ax[pos_1, pos_2].title.set_text(title)
    
#gera bloxplot de ativo por período de hold analisando o atributo informado em main_atrib
def plot_boxplot(ativo, res, normalized, main_atrib, atribs):
    res_ativo = res
    if normalized != None:
        res_ativo = res.loc[(res["LOG"] == normalized) ]
    
    hold             = res_ativo["VALID_BAL_HOLD"].iloc[0]
    if ativo == "TODOS ATIVOS":
        hold = res_ativo["VALID_BAL_HOLD"].mean()
    
    count = res_ativo["VALID_BAL_HOLD"].count()
    qt_subplot_lines = int((len(atribs)+1)/2)
    fig, ax = plt.subplots(qt_subplot_lines, 2, figsize=(10,qt_subplot_lines*3))
    plt.suptitle("RETORNO FINAN. (VALIDAÇÃO) NORM:"+str(normalized)+" PERÍODO HOLD POR "+main_atrib+" - "+ativo+"-QT:"+str(count))
    
    data = pd.Series(dtype=int)
    for i in range(len(atribs)):
        res_alg = res_ativo.loc[(res_ativo[main_atrib] == atribs[i] )]

        for n in constants.PERIODS_RESULTS:
            data["N_RES"+str(n)] = res_alg.loc[(res_alg["N_RES"] == n)]["VALID_BAL_PRED"]
        
        count2 = res_alg[main_atrib].count()
        title = str(atribs[i]) +"/"+str(count2)
        plot_subplot(ax, int(i%qt_subplot_lines), int(i/qt_subplot_lines), 
                     constants.DEFAULT_INIT_BALANCE, hold, data, title)

    data = pd.Series(dtype=int)
    for n in constants.PERIODS_RESULTS:
        data["N_RES"+str(n)] = res_ativo.loc[(res_ativo["N_RES"] == n)]["VALID_BAL_PRED"]
    
    count2 = res_ativo[main_atrib].count()
    title = "TODOS/"+str(count2)
    plot_subplot(ax, qt_subplot_lines-1, 1, constants.DEFAULT_INIT_BALANCE, hold, data, title)
    plt.show()
        

#faz plot do scatter do retorno financeiro por algoritmo e tempo de hold para cada ativo
#UTILIZAR PREFERENCIALMENTE A FUNÇÃO PLOT_BOXPLOTS
def plot_scatter_balance(res, normalized):
    for ativo in constants.STOCKS:
        res_ativo = res.loc[(res["ATIVO"] == ativo) & (res["LOG"] == normalized) ]

        hold = res_ativo["VALID_BAL_HOLD"].iloc[0]
        fig, ax = plt.subplots(4, 2, figsize=(10,14))
        plt.suptitle("RETORNO FINANCEIRO EM BASE DE VALIDAÇÃO POR N_RES E ALG - "+ativo)
        for i in range(len(constants.ALGORITMS)):
            X = res_ativo["N_RES"]
            Y = res_ativo["VALID_BAL_PRED"]
            #ax[int(i\2), int(i\4)].plot(X, Y, label=algoritms[i])
            ax[int(i%4), int(i/4)].scatter(X, Y, label=constants.ALGORITMS[i]);
            ax[int(i%4), int(i/4)].title.set_text(constants.ALGORITMS[i])
            #plt.scatter(X,Y)
            line = mlines.Line2D([0, 20], [hold, hold], color='red')
            lineg = mlines.Line2D([0, 20], [constants.DEFAULT_INIT_BALANCE, constants.DEFAULT_INIT_BALANCE], color='green')
            ax[int(i%4), int(i/4)].add_line(line)
            ax[int(i%4), int(i/4)].add_line(lineg)

        X = res_ativo["N_RES"]
        Y = res_ativo["VALID_BAL_PRED"]
        ax[3, 1].scatter(X, Y);
        
        
        line = mlines.Line2D([0, 20], [hold, hold], color='red')
        lineg = mlines.Line2D([0, 20], [constants.DEFAULT_INIT_BALANCE, constants.DEFAULT_INIT_BALANCE], color='green')
        ax[3, 1].add_line(line)
        ax[3, 1].add_line(lineg)

        ax[3, 1].title.set_text("TODOS ALGORITMOS - NORMALIZADO:"+str(normalized))
        plt.show()



#Ordena os resultados de processamento pelo campo especificado em by_criteria
def sort_resultado_by_criteria(resultado, by_criteria, n_period_result=constants.DEFAULT_PERIOD_RES):
    if n_period_result != None:
        df = resultado.loc[(resultado["N_RES"] == n_period_result)]   
        
    else:
        df = resultado

    df = df.drop(["CM00","CM10","CM01","CM11", "SCO_TRAIN"], axis=1)

    df = df.sort_values(by=by_criteria, axis=0, ascending=False, inplace=False, 
                          kind='quicksort', na_position='last')    

    return df

#######################INICIO ANALISE DE RESULTADOS#####################
#Plota gráfico em linha da acurácia obtida na base de teste
def analyse_results():

    res = read_resultado()
    #res = res.loc[(res["LOG"] == constants.DEFAULT_NORMALIZED) & 
     #         (res["TEST_SIZE"] == constants.DEFAULT_TEST_SIZE)]
    for ativo in constants.STOCKS:
        res_ativo = res.loc[(res["ATIVO"] == ativo)]# & (res["LOG"] == constants.DEFAULT_NORMALIZED)]
        #res_ativo = sort_resultado(res_ativo)

        plot_resultado(res_ativo, period=constants.DEFAULT_PERIOD_RES, ativo=ativo)
        for t in constants.TRAIN_TEST_SPLIT_SIZES:
            plot_ativo(res_ativo, ativo, True, t)
            plot_ativo(res_ativo, ativo, False, t)
        break
    plot_global_result(res, "SCO_TEST")
    plot_global_result(res, "SCO_VALID")

def main():
    print_res_alg()    
    #compute_bets_results()
    analyse_results()#gera histograma de SCO_TEST
    #plot_scatter(constants.DEFAULT_NORMALIZED, constants.DEFAULT_TEST_SIZE, read_resultado())
    #plot_scatter_balance(read_resultado(), constants.DEFAULT_NORMALIZED)
    plot_boxplots(read_resultado(), normalized=None, test_size=None)    

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    
