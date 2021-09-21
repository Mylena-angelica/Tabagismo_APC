#IMPORTANDO BIBLIOTECAS
import plotly.graph_objects as go
import pandas as pd
import math

#ORGANIZANDO OS DADOS 
dados=pd.read_csv('tobacco-production.csv', sep=',') #Lendo os dados que estão em csv

dados_array=dados.values #Criando variável para os dados

pais=[] # Lista dos paises, será utlizado os codígos ISO_alpha para indicar a localidade no mapa.
ano=[]  # Lista dos anos (min. 1961 e máx. 2018)
producao=[] # Lista da quantidade de tabaco produzida

for linha in dados_array:  #Selecionando os dados da tabela
    if linha[2]== 2018: # A priori, a seleção do ano será assim. No futuro será por meio de um dropdown.
        pais.append(linha[1]) 
        ano.append(linha[2]) 
        producao.append(linha[3])

for codes in pais:
    if not type(codes)== str:
        if math.isnan(float(codes)):
            index=pais.index(codes)
            del pais[index]
            del ano[index]
            del producao[index]
            
    elif codes=='OWID_WRL'
        index=pais.index(codes)
            del pais[index]
            del ano[index]
            del producao[index]

#Configurando o gráfico

fig = go.Figure(data=go.Choropleth( #Recuperando dados do gráfico na base de dados e o tipo de dados
    locations = pais,
    z = producao,
    text = ano,
    colorscale = 'plasma',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_tickprefix = 'Toneladas',
    colorbar_title = 'Produção em <br>toneladas',
))

fig.update_layout(
    title_text='Produção mundial de tabaco',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.1,
        xref='paper',
        yref='paper',
        text='Fonte: <a href="https://ourworldindata.org/grapher/tobacco-production">\
            Our world in Data</a>',
        showarrow = False
    )]
)

fig.show()


