import pandas as pd
from sklearn import svm

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
df_test = df[['br', 'dia_semana', 'fase_dia', 'condicao_metereologica']]
teste = df_test.groupby(df_test.columns.tolist(),as_index=False).size()
# teste['size'] =teste['size'].div(100)
for i in teste[['dia_semana', 'fase_dia', 'condicao_metereologica']]:
    count =0
    for j in teste[i].unique():
        teste = teste.replace(j, count)
        count += 1
# print(teste)
data = teste.iloc[:, 0:4]
target = teste['size']
# print(data)
# print(target)
clf = svm.SVC(gamma=0.001, C=100)
clf.fit(data, target)
print(clf.predict([[10, 0, 2, 0]])[0]/100)