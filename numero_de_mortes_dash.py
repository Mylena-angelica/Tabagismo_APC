#Importando as bibliotecas
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate


app = dash.Dash(__name__)

#---------------------------------------------------------------

app.layout = html.Div([

    html.H1("Mortes por fumo a cada 100 mil habitantes", style = {'fontSize' : 20}), #titulo
    html.Br(), #pular uma linha

    dcc.Slider( # gerando o slider (barra deslizante)
        id='my-slider', 
        min= 1990, #valor minimo do slider
        max= 2017, #valor maximo do slider
        step= 1, #de quanto em quanto vai andar na barra
        value=2017, # o valor inicial na barra
        marks={ #valores que vao aparecer em destaque na barra
                2017: '2017', 
                2014: '2014',
                2011: '2011', 
                2008: '2008', 
                2005: '2005', 
                2002: '2002', 
                1999: '1999', 
                1996: '1996', 
                1993: '1993',
                1990: '1990',
            },
        tooltip={"placement": "bottom", "always_visible": True}

    ),
    html.Div(id='slider-output-container'), #Idenficando que um slider sera usado
    html.Div([dcc.Graph(id='our_graph') #Idenficando que um gráfico sera usado
    ]),
])

# configurações do callback identificação do output e input
@app.callback(
    Output('slider-output-container', 'children'),
    Output('our_graph','figure'),
    [Input('my-slider', 'value')],

)


def update_output(value):
    if value is None:
        raise PreventUpdate
    else:
        df = pd.read_csv('https://raw.githubusercontent.com/Beatrizvn/Codigo/main/numerodemortes.csv')

        dados_array = df.values 

        pais = []
        codigo_ISO = []
        ano = []
        mortes = []
        texto = [] 

        for linha in dados_array:
            if linha[2] == value: #selecionando o ano que sera utilizado
                pais.append(linha[0])
                codigo_ISO.append(linha[1])
                ano.append(linha[2])
                mortes.append(linha[3])
                texto.append(f'{linha[0]} - Mortes : {int(linha[3])}') #texto que vai aparecer ao passar o mouse por cima das bolhas

        #Gerando o gráfico

        figura = go.Figure((go.Scattergeo(
                    locationmode = 'ISO-3', #para achar o local de cada pais no mapa
                    locations = codigo_ISO, #achar o local de cada pais no mapa
                    text = texto, #o texto a ser mostrado ao passar o mouse
                    marker = dict( 
                        size = mortes,#tamanho das bolinhas
                        sizemode = 'area', #A  regra para a qual os dados sãoconvertidos em pixels. Evita que as bolhas fiquem enormes
                        color = mortes, #O que vai levar em conta para definir a escala de cor
                        colorscale = 'Rainbow', #A cor da barra
                        cmax = max(mortes), #O valor maximo da barra de cor
                        cmin = 0, #O valor minimo da barra de cor
                        colorbar_title = "Mortes"))

                        ))
        return ('Ano selecionado "{}" '.format(value), figura)

if __name__ == '__main__':
    app.run_server(debug=True)
