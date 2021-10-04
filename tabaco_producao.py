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
        pais.append(linha[1]) # append serve para criar as listas.
        ano.append(linha[2]) 
        producao.append(linha[3])

for codes in pais:    # Laço para excluir os dados que não se aplica a ISO_alpha (Dados por continente)
    if not type(codes)== str: 
        if math.isnan(float(codes)): #Condição para usar a função a baixo, quando aparece nan (ou seja, não existe o código ISO_alpha na tabela)
            index=pais.index(codes) #Função index serve para procurar um elemento
            del pais[index] #Deletando os dados relacionados ao nan
            del ano[index] #Deletando os dados relacionados anos dos codes que apresentam nan
            del producao[index] #Deletando os dados relacionados à produção que apresenta nan
            
    elif codes=='OWID_WRL' #Excluindo os dados relacionados ao mundo como um todo, os dados ligados a str OWID_WRL
        index=pais.index(codes) 
            del pais[index] #Deletando os dados relacionados ao nan
            del ano[index] #Deletando os dados relacionados ao nan
            del producao[index] #Deletando os dados relacionados ao nan

#Configurando o gráfico

fig = go.Figure(data=go.Choropleth( #Recuperando dados do gráfico na base de dados e o tipo de dados
    locations = pais, #Utiliza os ISO_Alpha (Codes) para localizar os países no gráfico
    z = producao, #Utiliza os dados de produção, é o que relaciona as cores do gráfico
    text = ano, #O ano escolhido
    colorscale = 'plasma', # Paleta de cores do mapa
    autocolorscale=False, # O false determina que você escolhe a paleta de cores
    reversescale=True, # Quando verdadeira, associa as cores aos valores do z
    marker_line_color='darkgray', # Cor das fronteiras
    marker_line_width=0.5, # Espessura das fronteiras
    colorbar_tickprefix = 'Toneladas', #Prefixo da coluna da legenda
    colorbar_title = 'Produção em <br>toneladas', #Título da legenda de cores
))

fig.update_layout(
    title_text='Produção mundial de tabaco', #Título do gráfico
    geo=dict(
        showframe=False, # Borda do mapa, quando False não irá aparecer
        showcoastlines=False, # Fronteiras costeiras, quando False não são marcadas
        projection_type='equirectangular' #Tipo de projeção do mapa
    ),
    annotations = [dict(
        x=0.55, #Posição do text no eixo x
        y=0.1, #Posição do text no eixo y
        xref='paper', #Referência do eixo X
        yref='paper', #Referência do eixo X
        text='Fonte: <a href="https://ourworldindata.org/grapher/tobacco-production">\
            Our world in Data</a>',  #Fonte
        showarrow = False #Questão estética
    )]
)

fig.show()


