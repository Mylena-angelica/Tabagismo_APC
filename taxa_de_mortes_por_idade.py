import pandas as pd
import plotly.graph_objects as go

# criação de uma variável que lerá os dados csv em dataframe 
df = pd.read_csv('death-rates-smoking-age.csv', sep = ',')

# a propriedade values lê os dados em dataframe e passa para dentro de uma lista de listas
dados = df.values

# definição da função que fará a filtragem dos dados do Brasil e do mundo
def filtrar_dados(dados):
    # transformando os dados de 2017 que estavam em array para lista
    dados2017 = []
    for elemento in dados:
        dados2017.append(elemento)

    # arrumando a ordem das idades dos dados
    x = dados2017[6]    # exemplo: [idade_2, idade_1]
    dados2017[6] = dados2017[7]
    dados2017[7] = x

    # pegando apenas os dados numéricos e deletando dados zerados
    mortes_por_idade = dados2017[3:]
    del mortes_por_idade[1:3]

    # arredondando os dados
    mortes_por_idade_arredondado = []
    for num in mortes_por_idade:
        mortes_por_idade_arredondado.append(round(num, 2))
    
    # me retorna os dados de 2017 já arredondados
    return mortes_por_idade_arredondado

# introdução dos dados do Brasil e do mundo array
dados_mundo = []
dados_brasil = []
for linha in dados:
    if 'World' == linha[0]:
        dados_mundo.append(linha)
    if 'Brazil' == linha[0]:
        dados_brasil.append(linha)
       
# filtragem para apenas o ano de 2017
dados_brasil2017 = dados_brasil[-1]
dados_mundo2017 = dados_mundo[-1]

# uso da função filtrar_dados para filtrar e organizar os dados do Brasil
mortes_idade_brasil = filtrar_dados(dados_brasil2017)

# uso da função filtrar_dados para filtrar e organizar os dados do mundo
mortes_idade_mundo = filtrar_dados(dados_mundo2017)

# formulação da variável x do gráfico
idades = ['Todas as idades', 'Entre 15 e 49 anos', 'Entre 50 e 69 anos', 'Mais de 70 anos']

# formulação do gráfico
barra1 = go.Bar(
    name = 'Brasil',
    x = idades,
    y = mortes_idade_brasil
)

barra2 = go.Bar(
    name = 'Mundo',
    x = idades,
    y = mortes_idade_mundo
)

grafico = go.Figure([barra1, barra2])

# layout e título
grafico.update_layout(barmode = 'group',  # layout de barras mais finas
title = 'Taxa de mortes prematuras devido ao tabagismo no ano de 2017'
)

grafico.show()




