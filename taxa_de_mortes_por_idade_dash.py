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

    html.Div([     # id : identifica o input; type : parâmetro do que será escrito, um número (ano)
        dcc.Input(id ='input_state', type = 'number', inputMode = 'numeric', value = 2017,    # inputmode : identifica a linguagem utilizada, o numeral; value : valor em que o gráfico será gerado inicialmente 
                max = 2017, min = 1990, required = True),    # required : aparecerá um retanângulo vermelho no botão caso não tenha selecionado um ano ou o ano escolhido não tenha dados 

        html.Button('Gerar gráfico', id = 'submit_button', n_clicks = 0),  # n_clicks : quantidade de pesquisas feitas (iniciamnente nenhuma)
        html.Div(id = 'output_state'), 
    ], style = {'text-align': 'center'})   # posição do texto

])

# configurações do callback: identificação do output, input e state
@app.callback( 
    Output(component_id = 'output_state', component_property = 'children'),     # declarando qual será o output
    Output(component_id = 'the_graph', component_property = 'figure'),          # declarando o id do componente e sua propriedade
    [Input(component_id = 'submit_button', component_property = 'n_clicks')],   # declarando que o submit_button, relaciona-se com o n_clicks
    [State(component_id = 'input_state', component_property = 'value')]         # declarando O input_state relaciona-se com value
    #State é diferente de Input, permitindo que você declare valores extras sem disparar o callback
)

# criando uma função para o botão que vai gerar o gráfico
def update_output(num_clicks, val_selected):
    if val_selected is None: 
        raise PreventUpdate    # se não for selecionado nenhum valor no botão o gráfico não atualizará
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
        
        # filtragem para apenas o ano escolhido usando a função filtrar_ano_selecionado 
        def filtrar_ano_selecionado(dados_todos_anos):
            for dado in dados_todos_anos:
                if dado[2] == val_selected:
                    dados_ano_selecionado = dado
            
            return dados_ano_selecionado       

        dados_brasil_ano = filtrar_ano_selecionado(dados_brasil)   
        dados_mundo_ano = filtrar_ano_selecionado(dados_mundo)        
        
        # definição da função que fará a filtragem dos dados do Brasil e do mundo
        def filtrar_dados(dados_ano_array):
            # transformando os dados do ano selecionado que estavam em array para lista
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
            text = mortes_idade_brasil,   # textro mostrando as taxas em cada barra
            textposition = 'auto'   # localização do texto dentro da barra
        )

        barra2 = go.Bar(
            name = 'Mundo',
            x = idades,
            y = mortes_idade_mundo,
            text = mortes_idade_mundo,   # texto mostrando as taxas em cada barra
            textposition = 'auto'   # localização do texto dentro da barra
        )

        grafico = go.Figure([barra1, barra2])

        # layout e título
        grafico.update_layout(barmode = 'group',  # layout de barras uma do lado da outra
        title = 'Taxa de mortes por idade, devido ao tabagismo <br><sup> Medida pelo número de mortes prematuras, devido ao tabagismo, por 100.000 indivíduos em um determinado grupo demográfico.</sup>' 
        )     # colocando um título e subtítulo usando html
        
        # a função retornará o gráfico e a frase abaixo mencionando o ano selecionado(val_selected) e o número de pesquisas(num_clicks)
        return ('O ano selecionado foi {} e você já fez  \
                 {} pesquisas'.format(val_selected, num_clicks), grafico)

if __name__ == '__main__':
    app.run_server(debug = True)

    


            




