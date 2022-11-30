import pandas as pd

def last(n):
    return n[-1]

def getAccidentsByValue(lista, value, df):
    for i in df[value].unique():
        # if len(df[df[value] == i])>=100:
        lista.append((i, len(df[df[value] == i])))
    # print(i, len(df[df['dia_semana'] == i]))
    return sorted(lista, key=last, reverse=True)

arr = []
df = pd.read_csv('./datatran2021.csv', encoding='ISO-8859-1', on_bad_lines='skip', sep=';')
# print(df[['causa_acidente', 'uf', 'br']])



# arr = getAccidentsByValue(arr, 'municipio')
# for i in arr:
#     print(i[0], i[1], 'acidentes')
# dfbr = df[df['br']==101]
arr = getAccidentsByValue(arr, 'tipo_acidente', df)
for i in arr:
    print(i[0], i[1], 'acidentes')
