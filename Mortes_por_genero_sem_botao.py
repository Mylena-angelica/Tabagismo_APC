from numpy import nan
import pandas as pd
import plotly.graph_objects as go

dados = pd.read_csv("plotly/comparing-the-share-of-men-and-women-who-are-smoking.csv", sep=",")
#print(dados)

dados_array = dados.values
#print(dados_array)

sigla = []
ano = []
sf = []
sm = []
pop = []
pais3 = []

for linha in dados_array:  #verificar se o nome do país por linha para tirar as repetições e 
    if not linha[0] in pais3:  #armazenar apenas uma vez o nome de cada pais em pais3
        pais3.append(linha[0])
        sigla.append(linha[1])


for linha in dados_array:      #verificar o nome as datas e só considerar as informações entre oa anos:
                               # 2007, 2010, 2012, 2014, 2016 e 2018
    if (linha[2] == 2007 or linha[2] >= 2010 and linha[2] <= 2018 and (linha[2] % 2 == 0)) and linha[0] == 'Brazil':
          
        ano.append(linha[2])
        sf.append(linha[3])
        sm.append(linha[4])
        pop.append(linha[3])


barra1 = go.Bar(
    x = sm,
    y = ano,
    marker=dict(color='#0099ff'),
    name = "Sexo Masculino",
    orientation='h'
)
barra2 = go.Bar(
    x = sf,
    y = ano,
    marker=dict(color='#404040'),
    name = "Sexo Feminino",
    orientation='h'
)

grafico = go.Figure([barra1, barra2])

grafico.show()
