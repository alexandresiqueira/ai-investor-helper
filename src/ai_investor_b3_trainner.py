# -*- coding: utf-8 -*-
"""
svm_grid.pcc: Avaliação da performance dos diversos classificadores: 
SVM, regressão logística, Gaussian Naive Bayes, KNN, etc.

Os dados dos ativos da B3 a serem classificados são lidos do diretório informado
na variável path, para análise de dados normalizados anteriormente, deve ser utilizado
o parâmetro normalized=True

As informações sobre o resultado da classificação nos diversos Classificadores é
armazenada no arquivo -result.csv, contendo as seguintes informações:
ORDEM: ordem de execução
ALG: Algoritmo de Classificação utilizado, 
ATIVO: ativo da B3 classificado, 
N_PER: período de retorno considerado para o teste (um dos presentes em _periods), 
"LOG": se utilizou o arquivo normalizado por logaritmo, 
"SCO_TRAIN": score do classificador no conjunto de treinamento, 
"SCO_TEST":: score do classificador no conjunto de teste, 
"ATRIBS": quantidade de atributos utilizados no treinamento e teste,
"INST.": quantidade de registros para teste e treinamento, 
"CM00": quantidade de registros na confusion matrix posição (0,0), 
"CM01": quantidade de registros na confusion matrix posição (0,1), 
"CM10": quantidade de registros na confusion matrix posição (1,0), 
"CM11": quantidade de registros na confusion matrix posição (1,1), 
"VP", 
"VN", 
"N_RES": número de períodos para verificação do retorno da operação realizado no 
    fechamento N períodos depois

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom


@date	  17 Outubro 2022
@version 1.0"""
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn import svm
import numpy as np
from joblib import dump, load
import os.path
import constants
import ai_investor_validator

clfs = pd.DataFrame([], columns = ["CLASSIFIER", "ID_CLASSIFIER", "NAME_CLASSIFIER"])

#normalized = True
res_cols_names = ["ALG", "ATIVO", "N_PER", "LOG", "SCO_TRAIN", "SCO_TEST", "ATRIBS",
                  "INST.", "CM00", "CM01", "CM10", "CM11", "VP", "VN", "N_RES", "TEST_SIZE",
                  "PRECISION0", "PRECISION1", "RECALL0",  "RECALL0", "F1-SCORE0",
                  "F1-SCORE1", "SUPPORT0", "SUPPORT1", "VALID_BAL_HOLD", 
                  "SCO_VALID", "VALID_BAL_PRED"]
pd.set_option('display.float_format','{:.2f}'.format)
np.set_printoptions(precision=2)

#Cria array de algoritmos classificadores para o problema proposto
def create_classifiers():
    neigh   = KNeighborsClassifier(n_neighbors=3)
    lreg    = LogisticRegression(max_iter=10000)
    dtc3    = DecisionTreeClassifier(random_state=0, criterion='entropy', max_depth=3)
    dtc6    = DecisionTreeClassifier(random_state=0, criterion='entropy', max_depth=6)
    rdc     = RandomForestClassifier()
    gnb     = GaussianNB()
    svmc    = svm.SVC(C=1)
    
    clfs.loc[len(clfs.index)] = [svmc, "SVM", "Support Vector Machine"]
    clfs.loc[len(clfs.index)] = [neigh, "KNN", "K Nearest Neighbors "]
    clfs.loc[len(clfs.index)] = [lreg, "LREG", "Regressão logística"]
    clfs.loc[len(clfs.index)] = [dtc3, "DTC3", "Arvore de Decisão - 3"]
    clfs.loc[len(clfs.index)] = [dtc6, "DTC6", "Arvore de Decisão - 6"]
    clfs.loc[len(clfs.index)] = [rdc, "RFC", "Arvore de Decisão - Random Forest"]
    clfs.loc[len(clfs.index)] = [gnb, "GNB", "Gaussian Naive Bayes"]
    
    
def read_data_file_stock(ativo, normalized):
    if normalized:
        cotacoes = pd.read_csv(constants.DATA_PATH+ativo+'-log-ind.csv',sep=constants.CSV_SEPARATOR) 
    else:
        cotacoes = pd.read_csv(constants.DATA_PATH+ativo+'-ind.csv',sep=constants.CSV_SEPARATOR) 
    return cotacoes    

def read_file_stock_and_adjust(ativo, n_periods, normalize, half_sample, n_periods_result):
    cotacoes = read_data_file_stock(ativo, normalize)

    cotacoes = adjust_technical_indicators(ativo, n_periods, normalize, half_sample, 
                                           n_periods_result, cotacoes)
    return cotacoes 
   
#lê o arquivo e retira as colunas que não farão parte do índice
def prepare_for_fit(cotacoes, ativo, n_periods, normalize, half_sample, n_periods_result, dt_init, dt_end):
    
    cotacoes = cotacoes.loc[(cotacoes["data"] > dt_init) & (cotacoes["data"] < dt_end)]

    cotacoes = cotacoes.drop(columns=['data', 'ativo','open', 'close', 'close-orig', 'high', 
                                      'low', 'volume'], axis=1)
    
    cotacoes = cotacoes.dropna()

    return cotacoes    


#A partir dos dados de um ativo contendo todos indicadores, remove atributos e 
# indicadores referentes a períodos maiores que n_periods os quais 
# não serão utilizados e mantém apenas o atributo da classe a ser inferida de acordo 
# com o período de retorno definido em n_periods_result
def adjust_technical_indicators(ativo, n_periods, normalize, half_sample, n_periods_result, cotacoes):

    count_periods = 0
    for period in constants.PERIODS_RESULTS:
        cotacoes = cotacoes.drop("res-"+str(period), axis=1)
        cotacoes = cotacoes.drop("res-perc-"+str(period), axis=1)
        if period != n_periods_result:
            cotacoes = cotacoes.drop("res-positive-"+str(period), axis=1)

    for period in constants.PERIODS_INDICATORS:
        count_periods = count_periods + 1        
            
        if count_periods > n_periods:
            #cotacoes = cotacoes.drop("fibo-ret-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-DIFF-"+str(period), axis=1)
            cotacoes = cotacoes.drop("MACD-SIGNAL-"+str(period), axis=1)
            cotacoes = cotacoes.drop("SO-"+str(period), axis=1)
            cotacoes = cotacoes.drop("SOS-"+str(period), axis=1)
            cotacoes = cotacoes.drop("RSI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("TSI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBH-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBHI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBL-"+str(period), axis=1)
            cotacoes = cotacoes.drop("BBLI-"+str(period), axis=1)
            cotacoes = cotacoes.drop("EMA-"+str(period), axis=1)
            cotacoes = cotacoes.drop("EMA-dist-"+str(period), axis=1)
            
        cotacoes = cotacoes.drop("min-"+str(period), axis=1)
        cotacoes = cotacoes.drop("max-"+str(period), axis=1)
        cotacoes = cotacoes.drop("SMA-dist-"+str(period), axis=1)
        cotacoes = cotacoes.drop("SMA-"+str(period), axis=1)
        cotacoes = cotacoes.drop("fibo-ret-"+str(period), axis=1)
        
    
    cotacoes["res-positive-"+str(n_periods_result)] = cotacoes["res-positive-"+str(n_periods_result)].astype(str)
    
    cotacoes.to_csv(constants.DATA_PATH+ativo+str(normalize)+"-train.csv", sep=constants.CSV_SEPARATOR, encoding='utf-8', index=False)

    return cotacoes


def create_and_save_model(ativo, algoritmn, normalized, n_per, n_per_result, dt_init, dt_end, test_size):
    cotacoes = read_file_stock_and_adjust(ativo, n_periods = n_per, normalize=normalized, 
                   half_sample=False, n_periods_result=n_per_result)
    cotacoes = prepare_for_fit(cotacoes, ativo, n_periods = n_per, 
                                         normalize=normalized, 
                   half_sample=False, n_periods_result=n_per_result, 
                   dt_init=dt_init, 
                   dt_end=dt_end)#ler todos registros
    
    clf_ = clfs.loc[(clfs["ID_CLASSIFIER"] == algoritmn)]
    clf = clf_["CLASSIFIER"].iloc[0]

    X = cotacoes.iloc[0:,0:(cotacoes.shape[1] - 1)]
    
    #ultima coluna contem resultados
    le = LabelEncoder()
    y = le.fit_transform(cotacoes.iloc[:,(cotacoes.shape[1] - 1)])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    #print("Criando modelo com:", cotacoes.shape, ";X:",X.shape,";X_train:",X_train.shape)

    clf.fit(X_train, y_train)
    save_model(clf, ativo, algoritmn, normalized, n_per, n_per_result)


def get_job_file_name(ativo, algoritmn, normalized, n_per, n_per_result):
    return constants.MODEL_PATH+ativo+'-'+str(n_per)+'-'+algoritmn+'-'+str(normalized)+'-'+str(n_per_result)+'.joblib'

def save_model(clf, ativo, algoritmn, normalized, n_per, n_per_result):
    dump(clf, get_job_file_name(ativo, algoritmn, normalized, n_per, n_per_result))

def load_model(ativo, algoritmn, normalized, n_per, n_per_result):
    file_name = get_job_file_name(ativo, algoritmn, normalized, n_per, n_per_result) 
    print("LOADING MODEL FILE:", file_name)
    if os.path.isfile(file_name):
        clf = load(file_name)
    else:
        print("ALERT - MODEL:", algoritmn, " FOR STOCK:", ativo, " AND PERIOD:", n_per_result, " DOESN'T EXISTS")
    return clf

#Funcao responsavel por realizar o treinamento, teste e validação de um classificador especifico (clf)
#o resultado da classificacao eh armazenado na varíavel global resDf com as informações conforme res_cols_names
def fit_and_predict(X_train, X_test, y_train, y_test, clf, cotacoes, ativo, 
                    class_names, clf_name, n_per_features, normalize, n_periods_result, 
                    test_size, resDf, cotacoesValidation, cotacoesValidClose):
    instances = cotacoes.shape[0]

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    y_pred_train = clf.predict(X_train)
    
    balanceHold = cotacoesValidation["bal-hold"].iloc[cotacoesValidation.shape[0]-1]
    le = LabelEncoder()
    
    y_valid = le.fit_transform(cotacoesValidation.iloc[:,(cotacoesValidation.shape[1] - 2)])
    #print(X_validation.shape)
    X_validation = cotacoesValidation.iloc[:,0:(cotacoesValidation.shape[1] - 2)]#remove bal-hol e res-positive
    y_pred_validation = clf.predict(X_validation)
    X_validation["close-orig"] = cotacoesValidClose #valores necessários para cálculo do retorno esperado financeiro

    X_validation = ai_investor_validator.calc_return_predic(X_validation, y_pred_validation, 
                                                  constants.DEFAULT_INIT_BALANCE, n_periods_result)

    balanceValidPred = X_validation["bal-pred-"+str(n_periods_result)].iloc[X_validation.shape[0]-1]
    acc_score_valid = accuracy_score(y_valid, y_pred_validation)

    print(classification_report(y_test, y_pred, target_names=class_names))
    cnf_matrix      = confusion_matrix(y_test, y_pred)
    acc_score       = accuracy_score(y_test, y_pred)
    acc_score_train = accuracy_score(y_train, y_pred_train)
    num_atribs      = cotacoes.shape[1] - 1
    print("Acurácia da base de treinamento: {:.2f}".format(acc_score_train))
    print("Acurácia da base de teste: {:.2f}".format(acc_score))
    
    VP          = cnf_matrix[0,0] / (cnf_matrix[0,0] + cnf_matrix[0,1])
    VN          = cnf_matrix[1,1] / (cnf_matrix[1,1] + cnf_matrix[1,0])
    precision0  = cnf_matrix[0,0] / (cnf_matrix[0,0] + cnf_matrix[1,0])
    precision1  = cnf_matrix[1,1] / (cnf_matrix[1,1] + cnf_matrix[0,1])
    recall0     = cnf_matrix[0,0] / (cnf_matrix[0,0] + cnf_matrix[0,1])
    recall1     = cnf_matrix[1,1] / (cnf_matrix[1,1] + cnf_matrix[1,0])
    f1_score0   = 2 * precision0 * recall0 / (precision0 + recall0)
    f1_socre1   = 2 * precision1 * recall1 / (precision1 + recall1)
    
    support0    = (cnf_matrix[0,0] + cnf_matrix[0,1])
    support1    = (cnf_matrix[1,1] + cnf_matrix[1,0])
    
    resDf.loc[len(resDf.index)] = [clf_name, ativo, n_per_features, normalize, acc_score_train, 
                                   acc_score, num_atribs, instances, cnf_matrix[0,0], 
                                   cnf_matrix[0,1], cnf_matrix[1,0], cnf_matrix[1,1], 
                                   VP, VN, n_periods_result, test_size, 
                                   precision0, precision1, 
                                   recall0, recall1, f1_score0, f1_socre1,
                                   support0, support1, balanceHold, acc_score_valid, balanceValidPred]    

    print(cnf_matrix)
    
    return resDf
    
"""
Realiza teste e treino de um conjunto de cotacoes de um ativo, em diversos modelos de ML.
Os modelos estão configurados e armazenados no array clfs.
Recebe o conjunto de dados para validação
"""
def process_ativo(cotacoes, ativo, n_per_features, normalize, n_per_result, 
                  test_size, resDf, cotacoesValidation, cotacoesValidClose):

    X = cotacoes.iloc[:,0:(cotacoes.shape[1] - 1)]
    
    #ultima coluna contem resultados
    le = LabelEncoder()
    y = le.fit_transform(cotacoes.iloc[:,(cotacoes.shape[1] - 1)])
    class_names = le.classes_
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=0)
    
    for i in range (clfs.shape[0]):
        print("---------------------------------------")
        print(clfs["NAME_CLASSIFIER"].iloc[i])
        print("---------------------------------------")
        
        resDf = fit_and_predict(X_train, X_test, y_train, y_test, clfs["CLASSIFIER"].iloc[i], 
                                cotacoes, ativo, class_names, clfs["ID_CLASSIFIER"].iloc[i],
                                n_per_features, normalize, n_per_result, test_size, 
                                resDf, cotacoesValidation, cotacoesValidClose)
    
    return resDf

def exec_stock_train(ativo, normalize, n_per, n_per_result, test_size, resDf):
    print("########### INICIO "+ativo+" - PER: "+str(n_per)+" - PER_RES: "+
          str(n_per_result)+" TSIZE:",test_size,"- NORMALIZED:",normalize," ##########")
    
    #ler todos registros
    cotacoes = read_file_stock_and_adjust(ativo, n_periods = n_per+1, normalize=normalize, 
                   half_sample=False, n_periods_result=n_per_result)#ler todos registros
    cotacoesValidation = cotacoes.loc[(cotacoes["data"] > constants.DATA_TRAIN_DATE_END)].copy()
    df = ai_investor_validator.calc_buy_and_hold(cotacoesValidation, constants.DEFAULT_INIT_BALANCE)

    cotacoesValidClose = cotacoesValidation["close-orig"]
    cotacoesValidation = prepare_for_fit(cotacoesValidation, ativo, n_periods = n_per+1, 
                                         normalize=normalize, 
                   half_sample=False, n_periods_result=n_per_result, 
                   dt_init=constants.DATA_TRAIN_DATE_END, 
                   dt_end=99999999)#ler todos registros
    cotacoesForFit = prepare_for_fit(cotacoes, ativo, n_periods = n_per+1, normalize=normalize, 
                   half_sample=False, n_periods_result=n_per_result, 
                   dt_init=constants.DATA_TRAIN_DATE_INIT, 
                   dt_end=constants.DATA_TRAIN_DATE_END)#ler todos registros
    resDf = process_ativo(cotacoesForFit, ativo, n_per+1,  normalize, n_per_result, 
                          test_size, resDf, cotacoesValidation, cotacoesValidClose)
    #print(cotacoesValidation.tail(5))
    

def train_test_ativo(ativo):
    resDf = pd.DataFrame([], columns = res_cols_names)
    
    print("########### INÍCIO TESTE E TREINAMENTO: "+ativo+" ################")
    for n_per in range(len(constants.PERIODS_INDICATORS)):

        for n_per_result in constants.PERIODS_RESULTS:
            for test_size in constants.TRAIN_TEST_SPLIT_SIZES:
                
                exec_stock_train(ativo, True, n_per, n_per_result, test_size, resDf)
                exec_stock_train(ativo, False, n_per, n_per_result, test_size, resDf)

                resDf.to_csv(constants.DATA_PATH+ativo+constants.FILE_NAME_RESULTADO, 
                             sep=constants.CSV_SEPARATOR, encoding='utf-8', index=True)
        
    
    print("########################### FIM "+ativo+" ###############################")
    return 1


#FUNCAO PRINCIPAL: para cada ativo em constants.STOCKS dispara teste e treinamento
def train_test():

    for ativo in constants.STOCKS:
        train_test_ativo(ativo)

def main():
    print("###############################################################")
    print("############################ B3 TRAIN #########################")
    print("###############################################################")
    stock = ""
    create_classifiers()
    #train_test_ativo(stock)
    for i in range(1, len(sys.argv)):
        print('argument:', i, 'value:', sys.argv[i])
        stock = sys.argv[i]
        break
    
    if stock != "":
        train_test_ativo(stock)
    else:
        train_test()
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    

