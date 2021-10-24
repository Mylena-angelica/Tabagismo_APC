# importando as bibliotecas 
from logging import debug
import pandas as pd
import plotly.graph_objects as go

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# importando a base de dados e criação de uma variável que lerá os dados csv em dataframe 
df = pd.read_csv('death-rates-smoking-age.csv', sep = ',')

# criando uma página com o dash
app = dash.Dash(__name__)

# layout da página do dash
app.layout = html.Div([     # o layout da página é formado por vários componentes como o html.Div e o dcc.Graph

    html.Div([
        dcc.Graph(id = 'the_graph')    # o dcc.Graph irá receber o gráfico da função 'the_graph' que foi endereçada no componente do output
    ]),

    html.Div([
        dcc.Input(id ='input_state', type = 'number', inputMode = 'numeric', value = 2017,   
                max = 2017, min = 1990, required = True), 

        html.Button(id = 'submit_button', n_clicks = 0, children = 'Gerar gráfico'),
        html.Div(id = 'output_state'), 
    ], style = {'text-align': 'center'})

])

# configurações do callback: identificação do output, input e state
@app.callback( 
    Output(component_id = 'output_state', component_property = 'children'), 
    Output(component_id = 'the_graph', component_property = 'figure'),
    [Input(component_id = 'submit_button', component_property = 'n_clicks')], 
    [State(component_id = 'input_state', component_property = 'value')]  
)

# criando uma função para o botão que vai gerar o gráfico
def update_output(num_clicks, val_selected):
    if val_selected is None: 
        raise PreventUpdate 
    else:
        dados = df.values   # a propriedade values lê os dados em dataframe e passa para dentro de uma lista de listas
         
        # introdução dos dados do Brasil e do mundo array 
        dados_mundo = []
        dados_brasil = []

        for linha in dados:
            if 'World' == linha[0]:
                dados_mundo.append(linha)
            if 'Brazil' == linha[0]:
                dados_brasil.append(linha)
        
        # filtragem para apenas o ano escolhido
        for dado in dados_mundo:
            if dado[2] == val_selected:
                dados_mundo_ano = dado

        for dado in dados_brasil:
            if dado[2] == val_selected:
                dados_brasil_ano = dado  
        
        # definição da função que fará a filtragem dos dados do Brasil e do mundo
        def filtrar_dados(dados_ano_array):
            # transformando os dados de 2017 que estavam em array para lista
            dados_ano_lista = []
            for elemento in dados_ano_array:
                dados_ano_lista.append(elemento)
                
            # arrumando a ordem das idades dos dados
            x = dados_ano_lista[6]    # exemplo: [idade_2, idade_1]
            dados_ano_lista[6] = dados_ano_lista[7]
            dados_ano_lista[7] = x
            
            # pegando apenas os dados numéricos e deletando dados zerados
            mortes_por_idade = dados_ano_lista[3:]
            del mortes_por_idade[1:3]

            # arredondando os dados
            mortes_por_idade_arredondado = []
            for num in mortes_por_idade:
                mortes_por_idade_arredondado.append(round(num, 2))
    
            return mortes_por_idade_arredondado
        
        # uso da função filtrar_dados para filtrar e organizar os dados do Brasil
        mortes_idade_brasil = filtrar_dados(dados_brasil_ano)   
        
        # uso da função filtrar_dados para filtrar e organizar os dados do mundo
        mortes_idade_mundo = filtrar_dados(dados_mundo_ano) 

        # formulação da variável x do gráfico
        idades = ['Todas as idades', 'Entre 15 e 49 anos', 'Entre 50 e 69 anos', 'Mais de 70 anos']

        # formulação do gráfico
        barra1 = go.Bar(
            name = 'Brasil',
            x = idades,
            y = mortes_idade_brasil,
            text = mortes_idade_brasil,
            textposition = 'auto'
        )

        barra2 = go.Bar(
            name = 'Mundo',
            x = idades,
            y = mortes_idade_mundo,
            text = mortes_idade_mundo,
            textposition = 'auto'
        )

        grafico = go.Figure([barra1, barra2])

        # layout e título
        grafico.update_layout(barmode = 'group',  # layout de barras uma do lado da outra
        title = 'Taxa de mortes prematuras devido ao tabagismo no ano de {}'.format(val_selected)
        )
        
        return ('O ano selecionado foi {} e você já fez  \
                 {} pesquisas'.format(val_selected, num_clicks), grafico)

if __name__ == '__main__':
    app.run_server(debug = True)

    


            




