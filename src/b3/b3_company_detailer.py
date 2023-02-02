# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 09:58:12 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import pandas as pd
import base64
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import constants


pd.set_option('display.max_columns', 700)
pd.set_option('display.max_rows', 500)
pd.set_option('precision', 4)
pd.set_option('display.width', 1000)

def request_json(url):
    headers = {'Accept': 'application/json'}
    print("call url:", url)
    r = requests.get(url, headers=headers)
    
    #print(f"Response: {r.json()}")
    return r

def __write_file(text, file_name):
    # open in binary mode
    file_name = constants.DATA_PATH_COMPANIES + file_name
    text = text.replace("\'", "\"")
    text = text.replace("\\", "\\\\")
    text = text.replace(" None", " \"\"")
    if (text[0] == '[') & (text[-1] == ']'):
        text = text[1:-1]
        
    with open(file_name+".tmp", "w") as file:
        file.write(text)
    if os.path.isfile(file_name):
        os.remove(file_name)
    os.rename(file_name+".tmp", file_name)
    print(file_name)

def base64Encode(message):
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    return base64_message

def encode_req_json(url, message):
    msg = base64Encode(message)
    url = url + msg
    req = request_json(url)
    return req.json()


def req_json_paged(url, req_complement):
    message = '{"language":"pt-br","pageNumber":1,"pageSize":200}'
    if req_complement != None:
        message = '{"language":"pt-br","pageNumber":1,"pageSize":200, '+req_complement+'}'
        
    data = encode_req_json(url, message)
    #page_number = data["page"]["pageNumber"]
    totalPages = data["page"]["totalPages"]
    cont_pages_request = 1
    #print("page:",page_number, "total:", totalPages, ";len:",len(data["results"]))
    for cur_page in range(1,totalPages):
        cont_pages_request = cont_pages_request + 1
        if cont_pages_request > 50:
            break
        message = '{"language":"pt-br","pageNumber":'+str(cont_pages_request)+',"pageSize":200}'
        if req_complement != None:
            message = '{"language":"pt-br","pageNumber":'+str(cont_pages_request)+',"pageSize":200, '+req_complement+'}'
        data2 = encode_req_json(url, message)
        data["results"] = data["results"] + data2["results"] 
        print("page:",cont_pages_request, "total:", totalPages, ";len:",len(data["results"]))

    print("total:", totalPages, len(data["results"]))
    return data    

def __load_json(file_name):
    #file_name = constants.DATA_PATH_COMPANIES + "companies.json"
    #print("loading companies:", file_name)
    f = open(file_name)
    data = json.load(f)
    return data

def __load_companies():
    file_name = constants.DATA_PATH_COMPANIES + "companies.json"
    return __load_json(file_name)

def __load_company(codeCVM):
    file_name = constants.DATA_PATH_COMPANIES +codeCVM+ ".json"
    return __load_json(file_name)

def __load_dividends(company):
    if company == None:
        return None
    file_name = constants.DATA_PATH_COMPANIES +company+ "-dividends.json"
    return __load_json(file_name)

def __load_supplement(stock):
    if stock == None:
        return None
    file_name = constants.DATA_PATH_COMPANIES +stock[0:4]+ "-supplement.json"
    data = __load_json(file_name)
    """if (data[0] == '[') & (data[-1] == ']'):
        data = data[1:-1]"""
    return data

def get_companies():
    data = __load_companies()
    df = pd.DataFrame(data["results"])
    return df

def get_company_info_value(stock, field):
    df = get_companies()
    dfA = df.loc[(df["issuingCompany"] == stock[0:4])]
    if len(dfA) > 0:
        return dfA.iloc[0][field]

def get_isin(stock, codeCVM):
    cp = __load_company(codeCVM)
    otherCodes = cp["otherCodes"]
    
    otherCodesDf = pd.DataFrame(otherCodes)
    dfA = otherCodesDf.loc[(otherCodesDf["code"] == stock)]
    if len(dfA) > 0:
        isin = dfA.iloc[0]["isin"]
    return isin

def get_pn_on(stock, codeCVM):
    
    isin = get_isin(stock, codeCVM)
    tp = isin[8:10]
    if tp == "NP":
        tp = "PN"
    elif tp == "NO":
        tp = "ON"
    #print("TP:",tp)
    return tp

def get_dividends(stock):
    tradingName = get_company_info_value(stock, "tradingName")
    codeCVM     = get_company_info_value(stock, "codeCVM")

    data = __load_dividends(tradingName)
    if data == None:
        return pd.DataFrame()
    df = pd.DataFrame(data["results"])
    
    tp = get_pn_on(stock, codeCVM)
    
    df = df.loc[(df["typeStock"] == tp)]
    
    df = df.loc[(df["corporateActionPrice"] != "")]

    #df['dateApproval'] = pd.to_datetime(df['dateApproval'], format='%d/%m/%Y')
    df['lastDatePriorEx']               = pd.to_datetime(df['lastDatePriorEx'], format='%d/%m/%Y')
    #df['dateClosingPricePriorExDate']   = pd.to_datetime(df['dateClosingPricePriorExDate'], format='%d/%m/%Y')
    df['corporateActionPrice']          = (df["corporateActionPrice"].str.replace(',','.')).astype(float)
    df['closingPricePriorExDate']       = (df["closingPricePriorExDate"].str.replace(',','.')).astype(float)
    df['valueCash']                     = (df["valueCash"].str.replace(',','.')).astype(float)

    return df

def get_supplements(stock):
    codeCVM     = get_company_info_value(stock, "codeCVM")

    data = __load_supplement(stock)
    #print (">>>>>>:",len(data["stockDividends"]))
    if (data == None) | (len(data["stockDividends"])==0):
        return pd.DataFrame(columns=["label", "factor","lastDatePrior"])

    df = pd.DataFrame(data["stockDividends"])
    
    isin = get_isin(stock, codeCVM)
    
    df = df.loc[(df["isinCode"] == isin)]
    df['lastDatePrior'] = pd.to_datetime(df['lastDatePrior'], format='%d/%m/%Y')
    df['factor']        = (df["factor"].str.replace('.','', regex=False).str.replace(',','.', regex=False)).astype(float)

    return df


def __get_company_all_detail(stock, codeCVM, tradingName, force=False):
    if (not os.path.exists(constants.DATA_PATH_COMPANIES+codeCVM+".json")) | (force):
        __get_company_detail(codeCVM)
    if (not os.path.exists(constants.DATA_PATH_COMPANIES + stock[0:4]+"-supplement.json")) | (force):
        __get_list_supplement(stock[0:4])
    if (not os.path.exists(constants.DATA_PATH_COMPANIES+tradingName+"-dividends.json")) | (force):
        __get_cash_dividends(tradingName)

def __get_companies_details(force=False):
    df = get_companies()
    for stock in constants.STOCKS:
        dfA = df.loc[(df["issuingCompany"] == stock[0:4])]
        if len(dfA) > 0:
            print(stock,":",dfA.iloc[0]["codeCVM"])
            __get_company_all_detail(stock=stock[0:4], codeCVM=dfA.iloc[0]["codeCVM"], 
                                     tradingName=dfA.iloc[0]["tradingName"], force=force)
        else:
            print(stock,": NÃO LOCALIZADO")

#lista todas empresas da B3
def __get_companies():
    data = req_json_paged(constants.URL_GET_COMPANIES, req_complement=None)
    __write_file(str(data), "companies.json")
    return data    

def __get_company_detail(codeCVM="9512"):
    message = '{"codeCVM":"'+codeCVM+'","language":"pt-br"}'
    data = encode_req_json(constants.URL_COMPANY_DETAIL, message)
    __write_file(data, codeCVM+".json")
    return data    

def __get_list_supplement(company="PETR"):
    message = '{"issuingCompany":"'+company+'","language":"pt-br"}'
    data = encode_req_json(constants.URL_COMPANY_SUPPLEMENT, message)
    __write_file(data, company+"-supplement.json")
    return data    

#lista os últimos dividendos pagos em dinheiro
def __get_cash_dividends(tradingName="PETROBRAS"):
    data = req_json_paged(constants.URL_CASH_DIVIDENDS, req_complement='"tradingName":"'+tradingName+'"')
    __write_file(str(data), tradingName+"-dividends.json")
    return data    



def main():
    #print (__get_cash_dividends("PETROBRAS"))
    print("############################################")
    #print(get_list_supplement("BBDC"))
    #print(get_company_detail("906"))
    #print(get_companies())
    #print (get_cash_dividends("PETROBRAS"))
    #__get_companies()
    #load_companies()
    #df = get_companies()
    #print(df.head())
    #__get_companies_details(force=True)
    df = get_dividends("BBDC4")
    print(df.head(20))
    #__get_list_supplement(company="BBDC")
    df = get_supplements("BBDC4")
    print(df.head(20))

print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()