# -*- coding: utf-8 -*-
"""
Created on Tue Oct 18 20:25:57 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom


@date	  17 Outubro 2022
@version 1.0"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import constants
"""
np.set_printoptions(threshold=None, precision=2)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 2)
"""



#ativo = "PETR4"

cols = ["ativo", "per", "days", "count", "mean", "std", "min", "max"]
stat = pd.DataFrame(columns=cols)


def read_ativo(ativo):
    cotacoes = pd.read_csv(constants.DATA_PATH+ativo+'-ind.csv',sep=constants.CSV_SEPARATOR)    
    
    return cotacoes

#Elimina as colunas que não fazem parte do estudo
def drop_columns(cotacoes):
    
    cotacoes = cotacoes.drop(columns=['data', 'ativo','open', 'close','close-orig', 'high', 'low', 'volume'], axis=1)
    for period in constants.PERIODS_INDICATORS:
        cotacoes = cotacoes.drop("SMA-"+str(period), axis=1)
        cotacoes = cotacoes.drop("EMA-"+str(period), axis=1)
        cotacoes = cotacoes.drop("SMA-dist-"+str(period), axis=1)
        cotacoes = cotacoes.drop("EMA-dist-"+str(period), axis=1)
        cotacoes = cotacoes.drop("min-"+str(period), axis=1)
        cotacoes = cotacoes.drop("max-"+str(period), axis=1)
    for period in constants.PERIODS_RESULTS:
        if period != constants.DEFAULT_PERIOD_RES:
            cotacoes = cotacoes.drop("res-positive-"+str(period), axis=1)
    return cotacoes

#Armazena os daddos referente ao retorno dos ativos para os periodos _periods
def compute_stat(ativo, cotacoes):
    dfAtivo = cotacoes
    tot_days = cotacoes.shape[0] - 1
    for period in constants.PERIODS_RESULTS:
        dfAtivo = cotacoes.iloc[:cotacoes.shape[0]-period+1,]
        tot_days = dfAtivo.shape[0] - 1
        dfAtivo1 = dfAtivo.loc[(dfAtivo["res-"+str(period)] > 0)]
        dfAtivo1 = dfAtivo1[ ["res-"+str(period), "res-perc-"+str(period)]]
        stat.loc[len(stat.index)] = [ativo, period,  tot_days, 
                                     dfAtivo1["res-perc-"+str(period)].count(), 
                                     dfAtivo1["res-perc-"+str(period)].mean(), 
                                     dfAtivo1["res-perc-"+str(period)].std(), 
                                     dfAtivo1["res-perc-"+str(period)].min(), 
                                     dfAtivo1["res-perc-"+str(period)].max()]


#faz um print dos dados estatísticos de retorno de um período específico
def compute_stat_period(stat):
    for period in constants.PERIODS_RESULTS:
        stat2= stat.loc[(stat["per"] == period)]
        print("---------- PERÍODO:",period," DIAS -----------")
        print(stat2.describe())



def plot_cotacoes(ativo, cotacoes):
    print("################ ANÁLISE - "+ativo+" ################")
    X = cotacoes.iloc[:,1:(cotacoes.shape[1] - 2)]
    atributos = list(cotacoes)[1:(cotacoes.shape[1] - 2)]
    
    fig, ax = plt.subplots(7, 3, figsize=(12, 20))
    plt.suptitle("Histograma dos atributos - "+ativo)
    
    for i in range(7):
        for j in range(3):
            ax[i, j].hist(X.iloc[:,(i*3 + j)], label=atributos[i*3+j], bins=30)
            ax[i, j].legend()
    plt.show()
    
    
#faz o plot de matriz scatter de 8 atributos das séries temporais
def plot_variables_scatter(ativo, cotacoes):

    for period in constants.PERIODS_RESULTS:
        cotacoes = cotacoes.drop("res-"+str(period), axis=1)
        cotacoes = cotacoes.drop("res-perc-"+str(period), axis=1)
    for period in constants.PERIODS_INDICATORS:
        if period != constants.DEFAULT_PERIOD_IND:
            cotacoes = cotacoes.drop("fibo-ret-"+str(period), axis=1)
            cotacoes = cotacoes.drop("RSI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("SO-"+str(period), axis=1)
            cotacoes = cotacoes.drop("SOS-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-DIFF-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-SIGNAL-"+str(period), axis=1)
            cotacoes = cotacoes.drop("TSI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBH-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBHI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBL-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBLI-"+str(period), axis=1)
    cotacoes = cotacoes.dropna()
    y = cotacoes["res-positive-"+str(constants.DEFAULT_PERIOD_RES)] #cotacoes.iloc[:,(cotacoes.shape[1] - 1)]   
    #print(iris_dataframe.iloc[:,10:14])
    pd.plotting.scatter_matrix(cotacoes.iloc[:,:8], figsize=(14,14), c=y, marker='o',
                                     hist_kwds={'bins':20}, s=60,alpha=.8)
    plt.title(ativo)
    
    plt.figure()
    
    ##As linhas do gráfico são numeradas de acordo com a ordem alfabética
    #ax3 = pd.plotting.parallel_coordinates(cotacoes, 'res-positive-'+str(constants.DEFAULT_PERIOD_RES), cols=["SO-20", "TSI-20"])


#Faz o plt de um ativo em um grafico contendo data, preço de fechamento m média exponencial e 
#bandas de bolinger
def plot_ativo(cotacoes, ativo, normalize=False):
    df = pd.Series(dtype=(float))
    #df = cotacoes.iloc[700:,[0,5,49, 118,120]]
    df = cotacoes.iloc[int(cotacoes.shape[0]*0.75):,:].copy() #.iloc[700:,:]

    df = df.dropna()
    df["data"] = pd.to_datetime(df['data'], format='%Y%m%d')
    if normalize:
        df.iloc[:,1:6] = np.log(df.iloc[:,1:6])
    
    plt.figure(figsize=(16, 8))
    ax = plt.axes()
    plt.title("Histórico de Fechamento e Bandas de Bollginger - "+ativo)
    plt.xlabel("data")
    #plt.ylabel("close");
    
    #x = np.linspace(0, 10, 1000)
    ax.plot(df["data"], df[ "close"], label="close" );
    ax.plot(df["data"], df[ "BBH-"+str(constants.DEFAULT_PERIOD_IND)], label="BBH-"+str(constants.DEFAULT_PERIOD_IND) );
    ax.plot(df["data"], df[ "BBL-"+str(constants.DEFAULT_PERIOD_IND)], label="BBL-"+str(constants.DEFAULT_PERIOD_IND) );
    ax.plot(df["data"], df[ "EMA-"+str(constants.DEFAULT_PERIOD_IND)], label="EMA-"+str(constants.DEFAULT_PERIOD_IND) );
    plt.legend()
    plt.show()

#gera informaçoes estatísticas sobre o retorno financeiro dos ativos para as operações
# de compra
def print_stats_return(stat):
    stat["count"] = stat["count"].astype(int)
    print(stat)
    print(stat.describe())
    
    fig, ax = plt.subplots()
    #plt.figure(figsize=(16, 8))
    fig.patch.set_visible(False)
    ax.axis('off')
    #ax.set_title('Estatística de retorno dos ativos por período de hold')
    stat.update(stat[['mean', 'std', 'min', 'max']].applymap('{:,.2f}'.format))
    table = ax.table(stat.values, colLabels=stat.columns, loc='center', rowLabels=stat.index)
    table.scale(1,2)
    plt.show()

    #print(stat.info())
    compute_stat_period(stat)

def plot_subplot(ax, pos_1, pos_2, data, title):
    ax[pos_1, pos_2].boxplot(data);
    ax[pos_1, pos_2].set_xticklabels(constants.PERIODS_RESULTS)    
    
    ax[pos_1, pos_2].title.set_text(title)

def plot_boxplot(stat):
    qt_subplot_lines = int((len(constants.STOCKS)+1)/2)
    fig, ax = plt.subplots(qt_subplot_lines, 2, figsize=(10,qt_subplot_lines*3))
    plt.suptitle("Boxplot - Resultado Ativos")
    for i in range(len(constants.STOCKS)):
        stat_ativo = stat.loc[(stat["ATIVO"] == constants.STOCKS[i] )]

        plot_subplot(ax, int(i%qt_subplot_lines), int(i/qt_subplot_lines), 
                      stat_ativo["res-perc-"+str(constants.DEFAULT_PERIOD_IND)], 
                      constants.STOCKS[i])
    plt.show()


def main():
    
    for ativo in constants.STOCKS:
        cotacoes = read_ativo(ativo)
        plot_ativo(cotacoes, ativo)
    
    for ativo in constants.STOCKS:
        cotacoes = read_ativo(ativo)
        cotacoes = drop_columns(cotacoes)
        plot_variables_scatter(ativo, cotacoes)
        compute_stat(ativo, cotacoes)
        plot_cotacoes(ativo, cotacoes)

    print_stats_return(stat)




    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    


