import pandas as pd
from apyori import apriori

def openDataSet():
    return pd.read_csv('./datatran2021.csv', encoding='ISO-8859-1', on_bad_lines='skip', sep=';')

def preProcessing(df):
    df['horario'] = pd.to_datetime(df['horario'], format='%H:%M:%S')
    df['horario'] = df['horario'].dt.hour
    df.loc[(df['horario'] >= 5) & (df['horario'] < 12), 'fase_dia'] = 'Manhã'
    df.loc[(df['horario'] >= 12) & (df['horario'] < 19), 'fase_dia'] = 'Tarde'
    df.loc[(df['horario'] >= 19) | (df['horario'] < 5), 'fase_dia'] = 'Noite'

    df.dropna()
    df = df.dropna(subset=['br'])

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

    df.loc[df['causa_acidente'] == 'Iluminação deficiente', 'causa_acidente'] = 'Deficiência do Sistema de Iluminação/Sinalização'

    df.loc[df['causa_acidente'] == 'Sinalização mal posicionada', 'causa_acidente'] = 'Problema de sinalização'
    df.loc[df['causa_acidente'] == 'Sinalização encoberta', 'causa_acidente'] = 'Problema de sinalização'
    df.loc[df['causa_acidente'] == 'Ausência de sinalização', 'causa_acidente'] = 'Problema de sinalização'

    df = df[~df['tipo_acidente'].str.contains('Eventos atípicos')]
    df.loc[df['tracado_via'] == 'Não Informado']

    df = df[['dia_semana','causa_acidente', 'br', 'tipo_acidente', 'condicao_metereologica', 'fase_dia', 'classificacao_acidente', 'tracado_via', 'tipo_pista']]
    df['br'] = df['br'].astype(str)

    return df

def generateRecords(df):
    records = []
    for i in range(0, len(df)):
        records.append([str(df.values[i, j]) for j in range(0, len(df.columns))])
    return records

def last(n):
    return n[-1]

def getAccidentsByValue(lista, value, df):
    for i in df[value].unique():
        lista.append((i, len(df[df[value] == i])))
    return sorted(lista, key=last, reverse=True)

def main():
    data = openDataSet()
    df = preProcessing(data)

    records = generateRecords(df)

    br = list(df['br'].unique())
    tipo_pista = list(df['tipo_pista'].unique())
    tracado_via = list(df['tracado_via'].unique())

    association_rules = apriori(records, min_support=0.001, min_confidence=0.50, min_lift=2, min_length=2, max_length=2)
    association_results = list(association_rules)

    # sort the results by confidence
    association_results = sorted(association_results, key=lambda x: x[2][0][2], reverse=True)

    teste = list(association_results)
    results = pd.DataFrame(teste)
    results.to_csv('results.csv')

    print(len(association_results))

    for i in association_results:
        check = list(i.items)

        if (check[0] in br):
            if (check[1] in tipo_pista) or (check[1] in tracado_via):
                continue
        if (check[1] in br):
            if (check[0] in tipo_pista) or (check[0] in tracado_via):
                continue

        # print(i.items)
        # print(i.support)
        print(i.ordered_statistics, sep='\n')
        print('')


if __name__ == '__main__':
    main()