import pandas as pd
import plotly.graph_objects as go

dados = pd.read_csv("plotly/comparing-the-share-of-men-and-women-who-are-smoking.csv", sep=",") #leitura dos dados 
#print(dados)

dados_array = dados.values 
#print(dados_array)

pais = []                     #Declaração de listas vazias
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


pag.layout = html.Div([                               #O layout é composto por uma árvore de "componentes" como html.Div e dcc.Graph, onde saõ escolhidas opções de titulos, subtitutos,..., enfi formatação do visual da pagina.
    html.H1("Numeros de morte por genero"),
    html.Br(),                                        #Br() é usado pra quebra de linha
                                                      #O dcc dropdown determina uma caixa de opções de entrada, no caso os nomes dos paises. Aqui nos endereçamos as identificações                        
    dcc.Dropdown(                                      
        id = "paises",
        options = [{'label' : name, 'value' : name} for name in pais3],    #delimita as opções dos nomes dos paises a serem escolhidos, que estão na variável pais3
        value = "Abkhazia",                                                # esse é o primeiro nome que vai aparecer na caixa de opções
        clearable = False
    ),
    dcc.Graph(id = "grafico-por-pais")                                     #dcc.Graph irá receber o grafico da função "grafico_morte_por_pais" endereçada no componente "output" do callback
])


#A função "filtar_nomes" recebe como argumento o nome selecionado na caixa de opções e verifica se o nome do pais selecionado na caixa de opções está na lista de paises disponíveis 

def filtar_nomes(name):
    for i in pais3:
        if name == i:
            return name

#As "entradas" e "saídas" da interface de nosso aplicativo são descritas declarativamente como os argumentos do callback. A função de saída deve estar declarada logo abaixo do callback correspondente
#O callback diz ao Dash para chamar a função "grafico_morte_por_pais", sempre que o valor do componente "input"(a caixa de texto) mudar para atualizar os novos atributos do componente "output" na página (o div HTML )

@pag.callback(
    Output("grafico-por-pais", "figure"), #Na saída que recebe o grafico que é retornado pela função, que está logo abaixo desse callback e retorna esse gráfico para o componente dcc.Graph do layout
    Input("paises", 'value')              #Na entrada eu identifico o id = "paises" e value = "primeiro nome que vai aparecer na caixa de opções"
)


#A função "grafico_morte_por_pais" recebe como argumento o nome do país escolhido na caixa de opções(Dropdown) e retorna um grafico de barras horizontais

def grafico_morte_por_pais(argumento):
    
    #Declaração das listas vazias. é importante declarar essas listas no incio da função, porque quando for sellecionado outro pais pela caixa de opções(Dropdown) essas lista vão ser atualizadas e as informações anteriores não vão aparecer no grafico 
   
    ano = []
    sf = []
    sm = []
    pop = []

    for linha in dados_array:      #loop coma a função de verificar as datas e só considerar as informações entre os anos:
                                   # 2007, 2010, 2012, 2014, 2016 e 2018.

        if (linha[2] == 2007 or linha[2] >= 2010 and linha[2] <= 2018 and (linha[2] % 2 == 0)) and linha[0] == argumento:    #Para cada uma das datas especificadas na condição seram considerados os dados a respeito do pais, identificado pelo variável "argumento", que traz o nome do pais escolhido

            ano.append(linha[2])   #Recebe o valor dos anos especificados na condição
            sf.append(linha[3])    #Atribui o valor da porcentagem de mortos do sexo feminino, para o pais que foi escolhido no ano especifico
            sm.append(linha[4])    #Atribui o valor da porcentagem de mortos do sexo masculino, para o pais que foi escolhido no ano especifico
            pop.append(linha[3])   #Atribui o valor total de mortos para o pais que foi escolhido no ano especifico

            
   # Gera o gráfio de barras horizontais para a porcentagem de mortos do genero feminino para o país escolhido:
    barra1 = go.Bar(
        x = sm,
        y = ano,
        marker=dict(color='#0099ff'),
        name = "Sexo Masculino",
        orientation='h'
    )
    
     # Gera o gráfio de barras horizontais para a porcentagem de mortos do genero feminino para o país escolhido:
    barra2 = go.Bar(
        x = sf,
        y = ano,
        marker=dict(color='#404040'),
        name = "Sexo Feminino",
        orientation='h'
    )

    grafico = go.Figure([barra1, barra2])
    
    

    return grafico

pag.run_server(use_reloader = False, debug = True) #O Dash atualizará automaticamente seu navegador quando você fizer uma alteração em seu código.

