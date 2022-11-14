# ai-investor-helper
 Artificial Intelligence Investor Helper

Este projeto tem o objetivo de analisar o histórico de preços de um ativo financeiro (valores OHLCV) e, por meio do uso de algoritmos de aprendizado de máquina recomendar a compra do ativo com vistas a obter o melhor retorno financeiro.


A sequência de execução do projeto é a que se segue:

1. Baixar os arquivos de séries anuais dos períodos de 2012 a 2022 da B3, a partir do link (https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/) e disponibilizar os arquivos, ainda compactados, no diretório /data

2. Executar o script coletor_b3.py o qual irá extrair os ativos que são alvo do estudo e gravar os dados da B3 e os indicadores em arquivos 
	2.1 Arquivo dos dados B3 do ativo em /data/<ATIVO>.csv
	2.2 Arquivo dos dados B3 do ativo enriquecidos com indicadores e classes em /data/<ATIVO>-ind.csv
	2.2 Arquivo dos dados normalizados do ativo enriquecidos com indicadores e classes em /data/<ATIVO>-log-ind.csv

3. Executar o script ai_investor_b3_trainner.py passando os nomes dos ativos para treinamento em paralelo, uma vez que esse é o passo mais lento do processamento, por exemplo:
	ai_investor_b3_trainner.py PETR4
	ai_investor_b3_trainner.py BBDC4
	ai_investor_b3_trainner.py ITUB4
	ai_investor_b3_trainner.py BBAS3
	ai_investor_b3_trainner.py VALE3
	ai_investor_b3_trainner.py USIM5
	ai_investor_b3_trainner.py BRKM5

4. Executar o script result_processor.py para consolidar os arquivos de resultados dos modelos e gerar o arquivo /data/-result.csv

5. Executar o script result_analyse.py para visualizar os gráficos de desempenho dos algoritmos, períodos de resultado, períodos de indicadores e tamanho de conjunto de teste;

6. Executar o script model.py para gravar os arquivos os melhores modelos obtidos após o passo 4, considerando melhores aqueles que obtiveram o maior índice para os atributos definidos em constants.BY_CRITERIA_RANK. Este script irá salvar arquivos /models/<ATIVO>-<PARÂMETTROS>.joblib

7. Executar o script ai_investor_validator.py para visualizar os gráficos de desempenho dos ativos considerando uma aplicação inicial definida em constants.DEFAULT_INIT_BALANCE conforme melhores modelos identificados e gravados no passo 6.
	
