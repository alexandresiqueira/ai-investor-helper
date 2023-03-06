# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 21:53:53 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import constants
"""
def apple_finder(file):
    for line in file:
        if 'apple' in line:
             yield line


source = open('forest','rb')

apples = apple_finder(source)

"""
ativo = 'PETR'
isn = 'BRPETRACNPR6'
file_name = constants.DATA_PATH_SERIES + "COTAHIST_A2022.TXT"
file_ativo = constants.DATA_PATH_SERIES + ativo+"4.TXT"
file_ativo2 = constants.DATA_PATH_SERIES + ativo+"4-2.TXT"
open(file_ativo,'w').writelines([ line for line in open(file_name) if isn in line])
open(file_ativo2,'w').writelines([ line for line in open(file_ativo) if ('78'+ativo not in line) 
                                  and ('82'+ativo not in line)
                                  and ('42'+ativo not in line)
                                  and ('38'+ativo not in line)
                                  and ('96'+ativo not in line)])
