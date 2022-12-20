# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 16:53:47 2022

@author: Alexandre Siqueira de Medeiros
@contact: alexandre.siqueira@gmailcom
"""
import coletor_b3
import ai_investor_b3_trainner
import result_processor
import result_analyse
import constants
from datetime import datetime
def main():
    today       = datetime.now()
    dir_        = today.strftime("%Y%m%d-%H%M%S")
    constants.DATA_PATH_RESULTS = constants.DATA_PATH_RESULTS + dir_ +"/"
    #coletor_b3.main()
    ai_investor_b3_trainner.main()
    result_processor.main()
    result_analyse.main()
    print("Resultados em:", constants.DATA_PATH_RESULTS)
    
print("The value of __name__ is:", repr(__name__))
if __name__ == "__main__":
    main()    