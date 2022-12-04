import pandas as pd
from apyori import apriori
import numpy as np
import matplotlib.pyplot as plt
import functools as ft

def last(n):
    return n[-1]

def getAccidentsByValue(lista, value, df):
    for i in df[value].unique():
        # if len(df[df[value] == i])>=100:
        lista.append((i, len(df[df[value] == i])))
    # print(i, len(df[df['dia_semana'] == i]))
    return sorted(lista, key=last, reverse=True)

def generateRecords(df):
    records = []
    for i in range(0, len(df)):
        records.append([str(df.values[i, j]) for j in range(0, 5)])
    return records

arr = []
df = pd.read_csv('./datatran2021.csv', encoding='ISO-8859-1', on_bad_lines='skip', sep=';')
df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S')
df['horario'] = df['horario'].dt.hour
df.loc[(df['horario'] >= 5) & (df['horario'] < 12), 'fase_dia'] = 'Manhã'
df.loc[(df['horario'] >= 12) & (df['horario'] < 19), 'fase_dia'] = 'Tarde'
df.loc[(df['horario'] >= 19) | (df['horario'] < 5), 'fase_dia'] = 'Noite'

df.dropna()

# Remove the columns that are not relevant
# df = df.drop(['id', 'latitude', 'longitude', 'regional', 'delegacia', 'uop', 'km', 'horario', 'sentido_via', 'uso_solo',
#                   'municipio', 'ignorados', 'ilesos', 'pessoas', 'feridos_leves', 'feridos_graves', 'classificacao_acidente',
#                   'veiculos', 'data_inversa', 'tracado_via'], axis=1)

# change causa_acidente to teste if estacionar
df.loc[df['causa_acidente'] == 'Ingestão de álcool ou de substâncias psicoativas pelo pedestre', 'causa_acidente'] = 'Ingestão de álcool e/ou substâncias psicoativas pelo pedestre'
df.loc[df['causa_acidente'] == 'Ingestão de álcool pelo condutor', 'causa_acidente'] = 'Ingestão de álcool e/ou substâncias psicoativas pelo condutor'
df.loc[df['causa_acidente'] == 'Ingestão de substâncias psicoativas pelo condutor', 'causa_acidente'] = 'Ingestão de álcool e/ou substâncias psicoativas pelo condutor'
df.loc[df['causa_acidente'] == 'Ausência de reação do condutor', 'causa_acidente'] = 'Reação tardia ou ineficiente do condutor'

df.loc[df['causa_acidente'] == 'Afundamento ou ondulação no pavimento', 'causa_acidente'] = 'Má condição da via'
df.loc[df['causa_acidente'] == 'Pista em desnível', 'causa_acidente'] = 'Má condição da via'
df.loc[df['causa_acidente'] == 'Pista esburacada', 'causa_acidente'] = 'Má condição da via'
df.loc[df['causa_acidente'] == 'Demais falhas na via', 'causa_acidente'] = 'Má condição da via'

df.loc[df['causa_acidente'] == 'Acumulo de água sobre o pavimento', 'causa_acidente'] = 'Pista Escorregadia'
df.loc[df['causa_acidente'] == 'Acumulo de óleo sobre o pavimento', 'causa_acidente'] = 'Obstrução e/ou acumulo de substâncias na via'
df.loc[df['causa_acidente'] == 'Obstrução na via', 'causa_acidente'] = 'Obstrução e/ou acumulo de substâncias na via'
df.loc[df['causa_acidente'] == 'Acumulo de areia ou detritos sobre o pavimento', 'causa_acidente'] = 'Obstrução e/ou acumulo de substâncias na via'

df.loc[df['causa_acidente'] == 'Iluminação deficiente', 'causa_acidente'] = 'Deficiência do sistema de iluminação/sinalização'

df.loc[df['causa_acidente'] == 'Sinalização mal posicionada', 'causa_acidente'] = 'Problema de sinalização'
df.loc[df['causa_acidente'] == 'Sinalização encoberta', 'causa_acidente'] = 'Problema de sinalização'
df.loc[df['causa_acidente'] == 'Ausência de sinalização', 'causa_acidente'] = 'Problema de sinalização'

df = df[['dia_semana','causa_acidente', 'tipo_acidente', 'condicao_metereologica', 'fase_dia', 'classificacao_acidente']]
# print(df['fase_dia'])
# df['fase_dia'] = df[df['fase_dia'] != 'ceu claro']
# print(df.head())

# @ft.lru_cache(maxsize=128)
# print(df.head(10))
def generateRecords(df):
    records = []
    for i in range(0, len(df)):
        records.append([str(df.values[i, j]) for j in range(0, len(df.columns))])
    return records
records = generateRecords(df)
# print(records)
    
association_rules = apriori(records, min_support=0.0001, min_confidence=0.2, min_lift=2, min_length=2, max_length=2)
association_results = list(association_rules)
print(len(association_results))
for i in association_results:
    print(i.items)
    print(i.support)
    print(i.ordered_statistics)
    print('')