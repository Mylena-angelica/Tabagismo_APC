import pandas as pd
import plotly.graph_objects as go
from math import isnan


dados = pd.read_csv("plotly/comparing-the-share-of-men-and-women-who-are-smoking.csv", sep=",")
#print(dados)

dados_array = dados.values
#print(dados_array)

#Declaração de listas vazias
pais = []
sigla = []
pais = []

for linha in dados_array:      #verificar se o nome do país por linha para tirar as repetições e 
    if (not linha[0] in pais) and (not isnan(float(linha[3]))):  #armazenar apenas uma vez o nome de cada pais em pais3
        pais.append(linha[0])
        sigla.append(linha[1])


######################################## Introdução ao Dash #################################################

import dash 
import dash_core_components as dcc          
import dash_html_components as html
from dash.dependencies import Input, Output

pag = dash.Dash()


pag.layout = html.Div([                 #O layout é composto por uma árvore de "componentes" como html.Div e dcc.Graph, onde saõ escolhidas opções de titulos, subtitutos,..., enfi formatação do visual da pagina.
    html.H1("Dados sobre Tabagismo", style = {'color': 'grey', 'fontsize' : 30}),
    html.Br(),                             #Br() é usado pra quebra de linha
    
    #O dcc dropdown determina uma caixa de opções de entrada, no caso os nomes dos paises. Aqui nos endereçamos as identificações
    
    #Caixa de opções:

    dcc.Dropdown(                                           
        id = "paises",
        options = [{'label' : name, 'value' : name} for name in pais],      #delimita as opções dos nomes dos paises a serem escolhidos, que estão na variável pais3
        value = "Africa Eastern and Southern",                           # esse é o primeiro nome que vai aparecer na caixa de opções
        clearable = False
    ),
    dcc.Graph(id = "grafico-por-pais")                   #dcc.Graph irá receber o grafico da função "grafico_morte_por_pais" endereçada no componente "output" do callback
])

#A função "filtar_nomes" recebe como argumento o nome selecionado na caixa de opções e verifica se o nome do pais selecionado na caixa de opções está na lista de paises disponíveis 

def filtar_nomes(name):
    for i in pais:
        if name == i:
            return name


#As "entradas" e "saídas" da interface de nossa pagina são descritas declarativamente como os argumentos do callback. A função de saída deve estar declarada logo abaixo do callback correspondente, nesse caso a função do gráfico
#O callback diz ao Dash para chamar a função "grafico_morte_por_pais", sempre que o valor do componente "input"(a caixa de texto) mudar para atualizar os novos atributos do componente "output" na página (o div HTML )

@pag.callback(
    Output("grafico-por-pais", "figure"),
    Input("paises", 'value')
)

#A função "grafico_morte_por_pais" recebe como argumento o nome do país escolhido na caixa de opções(Dropdown) e retorna um grafico de barras horizontais

def grafico_consumo_por_genero(argumento):

    ano = [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018]

    #Declaração das listas vazias. é importante declarar essas listas no incio da função, porque quando for selecionado outro pais pela caixa de opções(Dropdown) essas listas vão ser atualizadas e as informações anteriores não vão aparecer no grafico 
   
    sf = []
    sm = []
   
    for linha in dados_array:      #verificar o nome do pais e só considerar as informações entre oa anos:
                                   #2010, 2012, 2014, 2016 e 2018

        #Para cada uma das datas especificadas na variavel "ano" na condição seram considerados os dados a respeito do pais escolhido, identificado pelo "argumento", que traz o nome do pais escolhido pelo dropdown
        #O bloco condicional abaixo irá atribuir os dados relativos apenas aos paises, escolhidos pelo parâmetro "argumento", e que apresentem todas as informações necessárias. Ex: linhas que tiverem Nan(not a number) seram desconsideradas  

        if not isnan(float(linha[3])) and linha[2] != 2007 and linha[0] == argumento:

            sf.append(linha[3])    #Atribui o valor da porcentagem de mortos do sexo feminino, para o pais que foi escolhido no ano especifico
            sm.append(linha[4])    #Atribui o valor da porcentagem de mortos do sexo masculino, para o pais que foi escolhido no ano especifico
    

    #As variaveis "genero_feminino" e "genero_masculino", passam os dados correspondentes já lidos, para a função "dados_filtrados", que retornará esses dados filtrados, já que alguns anos não apresentavam dados

    genero_feminino = dados_filtrados (sf)
    genero_masculino = dados_filtrados (sm)


    # Gera o gráfio de barras horizontais para a porcentagem de mortos do genero feminino para o país escolhido:

    barra1 = go.Bar(
        x = ano,
        y = genero_masculino,
        marker=dict(color='#0099ff'),   #atribui a cor azul a barra do gráfico
        name = "Sexo Masculino",        #Nome que aparece na legenda associado a cor escolhida
    )
    

    # Gera o gráfio de barras horizontais para a porcentagem de mortos do genero feminino para o país escolhido:

    barra2 = go.Bar(
        x = ano,
        y = genero_feminino,
        marker=dict(color='deeppink'),     #atribui a cor rosa a barra do gráfico
        name = "Sexo Feminino",
    )

    grafico = go.Figure([barra1, barra2])    #Associa as barras dos graficos "barra1" e "barra2", para comparação do consumo de tabaco por genero



    grafico.update_layout(            #Atualiza o layout incerindo um título para o grafico e subtítulos nos eixos
        plot_bgcolor = 'white',
        xaxis_title = 'ano',
        yaxis_title = 'Consumidores de tabaco (em %)',
        title = dict(
            text = "Porcentagem de uso do tabaco por genero, de 2010 a 2018",
            font = dict(
                family = "Arial",
                size = 20,
                color = "grey"
            ), 
        ),
    )
        

    return grafico


#A função "dados_filtrados" irá receber os valores das porcentagens de consumo, dos anos que apresentam dados e depois faz uma média entre uma ano antecessor e um ano sucessor, para os anos que que não apresentavam dados:
#Onde "a" á o parametro que a função recebe, no caso as porcentagens de consumo de cada genero

def dados_filtrados (a):
    sexo = []

    for i in range(0,4):
        media1 = 0

        sexo.append(a[i])
        media1 = (a[i] + a[i+1])/2
        sexo.append(media1)

    sexo.append(a[4])

    
    return sexo


pag.run_server(use_reloader = False, debug = True)  #O Dash atualizará automaticamente seu navegador quando você fizer uma alteração em seu código.

