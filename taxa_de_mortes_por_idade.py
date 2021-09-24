import pandas as pd
import plotly.graph_objects as go
df = pd.read_csv('death-rates-smoking-age.csv', sep = ',')

dados = df.values

#introdução dos dados do brasil e do mundo array
dados_mundo = []
dados_brasil = []
for linha in dados:
    if 'World' == linha[0]:
        dados_mundo.append(linha)
    if 'Brazil' == linha[0]:
        dados_brasil.append(linha)
       
#filtragem para apenas o ano de 2017
dados_brasil2017 = dados_brasil[-1]
dados_mundo2017 = dados_mundo[-1]

print(dados_brasil2017)
"""
#transformando dados_brasil2017 em lista
dados_b = []
for elemento_b in dados_brasil2017:
    dados_b.append(elemento_b)

#arrumando a ordem das idades do dados do brasil
x = dados_b[6]
dados_b[6] = dados_b[7]
dados_b[7] = x

#pegando apenas os dados numéricos e deletando dados zerados (brasil)
mortes_por_idade_brasil = dados_b[3:]
del mortes_por_idade_brasil[2]
del mortes_por_idade_brasil[1]
print(mortes_por_idade_brasil)

#transformando dados_mundo2017 em lista
dados = []
for elemento in dados_mundo2017:
    dados.append(elemento)

#arrumando a ordem das idades dos dados do mundo
x = dados[6]
dados[6] = dados[7]
dados[7] = x

#pegando apenas os dados numéricos e deletando dados zerados (mundo)
mortes_por_idade = dados[3:]
del mortes_por_idade[2]
del mortes_por_idade[1]
print(mortes_por_idade)

#formulação da variável x do gráfico
idades = ['Todas as idades', 'Entre 15 e 49 anos', 'Entre 50 e 69 anos', 'Mais de 70 anos']

barra1 = go.Bar(
    name = 'Brasil',
    x = idades,
    y = mortes_por_idade_brasil
)

barra2 = go.Bar(
    name = 'Mundo',
    x = idades,
    y = mortes_por_idade
)

grafico = go.Figure([barra1, barra2])

#layout de barras menores e do título
grafico.update_layout(barmode = 'group',
title = 'Taxa de mortes prematuras devido ao tabagismo no ano de 2017'
)

grafico.show()



"""