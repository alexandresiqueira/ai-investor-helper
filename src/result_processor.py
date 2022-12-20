# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 19:02:56 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom


@version 1.0"""

import os.path
import pandas as pd
import constants

#Realiza o agrupamento dos arquivos de resultado de trainamento, teste e validação dos
# ativos. O arquivo resultado geeral será o arquivo  descrito por:
# constants.DATA_PATH+constants.FILE_NAME_RESULTADO
def group_res_files():
    dfGlobal = pd.Series(dtype=float)
    for ativo in constants.STOCKS:
        fname = constants.DATA_PATH_RESULTS+ativo+constants.FILE_NAME_RESULTADO
        print("Processando Ativo:", ativo, ". Arquivo:",fname)
        if os.path.isfile(fname):    
            df = pd.read_csv(fname, sep=constants.CSV_SEPARATOR, index_col=0)
            if dfGlobal.size == 0:
                dfGlobal = df
            else:
                dfGlobal = dfGlobal.append(df)
        else:
            print("ALERT: arquivo inexistente:", ativo, ". Arquivo:",fname)
            
    print("Criando arquivo consolidado:", constants.DATA_PATH+constants.FILE_NAME_RESULTADO)

    dfGlobal.to_csv(constants.DATA_PATH_RESULTS+constants.FILE_NAME_RESULTADO, sep=constants.CSV_SEPARATOR, 
                    encoding='utf-8', index=True)


def main():
    print("###############################################################")
    print("##################  CONSOLIDANDO RESULTADOS  ##################")
    group_res_files()
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    
