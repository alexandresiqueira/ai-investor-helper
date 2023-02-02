# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:05:47 2022

@author: ccgov
"""
import itertools as it
import constants

features = ["MACD-", "MACD-DIFF-", "MACD-SIGNAL-", "SO-", "SOS-", "RSI-", "TSI-", "BBH-", "BBHI-", "BBL-", "BBLI-",
            "EMA-", "EMA-dist-", "min-", "max-", "SMA-dist-", "SMA-", "fibo-ret-"]

def combinate_features():
    #x = list(it.combinations(features, 2))
    x = list(it.combinations(constants.PERIODS_INDICATORS, 3))
    print(">>>>>>>>", x)
    print(len(x))
    
combinate_features()