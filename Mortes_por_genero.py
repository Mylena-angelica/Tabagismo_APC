import pandas as pd
import plotly.graph_objects as go

dados = pd.read_csv("plotly/comparing-the-share-of-men-and-women-who-are-smoking.csv", sep=",")
#print(dados)

dados_array = dados.values
#print(dados_array)

pais = []
sigla = []
pais3 = []

for linha in dados_array:      #verificar se o nome do país por linha para tirar as repetições e 
    if not linha[0] in pais3:  #armazenar apenas uma vez o nome de cada pais em pais3
        pais3.append(linha[0])
        sigla.append(linha[1])


#print(ano)
#print(sf)
#print(sm)
#print(pais3)


import dash 
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

pag = dash.Dash()


pag.layout = html.Div([
    html.H1("Numeros de morte por genero"),
    html.Br(),
   #dcc.Graph(figure = grafico),#
    dcc.Dropdown(
        id = "paises",
        options = [{'label' : name, 'value' : name} for name in pais3],
        value = "Abkhazia",
        clearable = False
    ),
    dcc.Graph(id = "grafico-por-pais")
])

def filtar_nomes(name):
    for i in pais3:
        if name == i:
            return name


@pag.callback(
    Output("grafico-por-pais", "figure"),
    Input("paises", 'value')
)



def grafico_morte_por_pais(argumento):
    ano = []
    sf = []
    sm = []
    pop = []

    for linha in dados_array:      #verificar o nome as datas e só considerar as informações entre oa anos:
                               # 2007, 2010, 2012, 2014, 2016 e 2018

        if (linha[2] == 2007 or linha[2] >= 2010 and linha[2] <= 2018 and (linha[2] % 2 == 0)) and linha[0] == argumento:

            ano.append(linha[2])
            sf.append(linha[3])
            sm.append(linha[4])
            pais.append(linha[0])
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
    
    

    return grafico

pag.run_server(use_reloader = False, debug = True)

