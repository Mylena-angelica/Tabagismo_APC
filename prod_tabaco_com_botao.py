#IMPORTANDO BIBLIOTÉCAS

from logging import debug
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#IMPORTANDO AS BASES DE DADO
dados=pd.read_csv('https://github.com/Mylena-angelica/Tabagismo_APC/blob/main/tobacco-production.csv', sep=',')

#UTILIZANDO O DASH PARA CRIAR UMA PÁGINA
app = dash.Dash(__name__)

#---------------------------------------------------------------
#MODIFICANDO O LAYOUT DO APP
app.layout = html.Div([  

    html.Div([
        dcc.Graph(id='the_graph') #IDENTIFICANDO O QUE SERÁ USANDO, NO CASO UM GRÁFICO (id É UMA STRING QUE IDENTIFICA O QUE SERÁ USADO NO DASH)
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2017,       #id(IDENTIFICANDO O QUE SERÁ O INPUT), type(QUER DIZER QUE SERÁ ESCRITO UM NÚMERO)
                  #inputmode(DIZ O TIPO DE "LINGUAGEM, NO CASO SERÁ NUMERAL, MAS EM OUTRO CASOS PODE SER LATIN, POR EXEMPLO), value(É O VALOR DO INPUT, OU SEJA, SEMPRE QUE GERAR O GRÁFICO SERÁ NESSE ANO)
                  max=2018, min=1961, required=True), #max(O ANO MÁXIMO QUE PODE SER RECEBIDO), min(O MENOR ANO A SER COLOCADO), required( QUANDO VERDADEIRO DIZ QUE É OBRIGATÓRIO O PREENCHIMENTO)
        html.Button(id='submit_button', n_clicks=0, children='Gerar gráfico'), #id(IDENTIFICANDO O QUE SERÁ), n_clicks(REPRESENTA O NÚMERO DE VEZES QUE UM ELEMENTO FOI CLICADO, NO CASO O INICIAL SERÁ 0), children(A "CRIANÇA DESSE COMPONENTE, OU SEJA, COMO SERÁ CHAMADO O BOTÃO)
        html.Div(id='output_state'), #id(IDENTIFICANDO)
    ],style={'text-align': 'center'}), #ALIANDO A POSIÇÃO DOS TEXTOS, QUESTÃO DE ESTILO

])

#---------------------------------------------------------------
@app.callback( #CONFIGURAÇÃO DO CALLBACK
    [Output('output_state', 'children'), #DECLARANDO O QUE SERÁ OUTPUT
    Output(component_id='the_graph', component_property='figure')], #DECLARANDO A id DO COMPONENTE E QUAL A SUA PROPRIEDADE, OU SEJA, O GRÁFICO UTILIZADO SERÁ A FIGURA MONTADA NO PLOTLY
    [Input(component_id='submit_button', component_property='n_clicks')], #DECLARANDO QUE O submit_button, ESTÁ RELACIONADO AO n_clicks
    [State(component_id='input_state', component_property='value')]  #DECLARANDO QUE O input_state ESTÁ RELACIONADO AO value
    #State é diferente de Input, POIS AQUELE PERMITE QUE VOCÊ DECLARE VALORES EXTRAS SEM DISPARAR O RETORNO DOS CALLBACKS
)

#CRIANDO UMA FUNÇÃO PARA O BOTÃO
def update_output(num_clicks, val_selected):
    if val_selected is None: 
        raise PreventUpdate # QUER DIZER QUE SE NÃO FOR ESCOLHIDO NENHUM VALOR, O GRÁFICO NÃO SERÁ ATUALIZADO
    else:
        dados_array=dados.values #Criando variável para os dados

        pais=[] # Lista dos paises, será utlizado os codígos ISO_alpha para indicar a localidade no mapa.
        ano=[] # Lista dos anos (min. 1961 e máx. 2018)
        producao=[] # Lista da quantidade de tabaco produzida

        for linha in dados_array: #Selecionando os dados da tabela
            if linha[2]== val_selected: #OS DADOS DO ANO UTILIZADO SERÃO OS DECLARADOS NO BOTÃO, QUE ESTÁ DEFINIDO PELA FUNÇÃO CRIADA ACIMA
                pais.append(linha[1]) # append serve para criar as listas.
                ano.append(linha[2])
                producao.append(linha[3])

        for codes in pais:  # Laço para excluir os dados que não se aplica a ISO_alpha (Dados por continente)
            if not type(codes)== str: 
                if math.isnan(float(codes)): #Condição para usar aS informações abaixo, quando aparece nan (ou seja, não existe o código ISO_alpha na tabela)
                    index=pais.index(codes) #Função index serve para procurar um elemento
                    del pais[index] #Deletando os dados relacionados ao nan
                    del ano[index] #Deletando os dados relacionados ao nan
                    del producao[index] #Deletando os dados relacionados ao nan
            elif codes=='OWID_WRL': #Excluindo os dados relacionados ao mundo como um todo, os dados ligados a str OWID_WRL
                index=pais.index(codes)
                del pais[index] #Deletando os dados relacionados ao nan
                del ano[index] #Deletando os dados relacionados ao nan
                del producao[index] #Deletando os dados relacionados ao nan

        dados_array = px.data.gapminder().query("year=={}".format(val_selected)) #FILTRANDO OS DADOS QUE SERÃO UTILIZADOS, dados_array FOI DECLARADO NA FUNÇÃO LÁ EM CIMA
        #px(PLOTLY EXPRESS), gapminder(FUNÇÃO DENTRO DO PX QUE CONSTRUI DADOS), query(CRIA UMA LISTA DE DADOS), DENTRO DO query TEM O ANO QUE SERÁ UTILIZADO O format(ESPECIFICA QUAL O DADO DENTRO  {}) QUE NO CASO SERÁ O ANO ESCOLHIDO NO BOTÃO(submit_button) 
        

        fig = go.Figure(data=go.Choropleth( #Recuperando dados do gráfico na base de dados e o tipo de dados
            locations = pais, #Utiliza os ISO_Alpha (Codes) para localizar os países no gráfico
            z = producao, #Utiliza os dados de produção, é o que relaciona as cores do gráfico
            text = val_selected, #DIZ QUE O QUE APARECERÁ NAS CAIXINHAS DE TEXTO, SERÁ O QUE FOI DIGITADO NO BOTÃO, OU SEJA, O ANO
            colorscale = 'sunsetdark',  # Paleta de cores do mapa
            autocolorscale=False, # O false determina que você escolhe a paleta de cores
            reversescale=True, # Quando verdadeira, associa as cores aos valores do z
            marker_line_color='darkgray', # Cor das fronteiras
            marker_line_width=0.5, # Espessura das fronteiras
            colorbar_tickprefix = ' Toneladas ', #Prefixo da coluna da legenda
            colorbar_title = 'Produção em <br>toneladas', #Título da legenda de cores
        ))

        fig.update_layout(
            title_text='Produção mundial de tabaco por país no ano de {}'.format(val_selected), #Título do gráfico UTILIZANDO O ANO ESCRITO NO BOTÃO
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations = [dict(
                 x=0.55, #Posição do text no eixo x
                y=0.1, #Posição do text no eixo y
                xref='paper', #Referência do eixo X
                yref='paper', #Referência do eixo X
                text='Fonte: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                    Our world in Data</a>', #LINK COM A FONTE DA BASE DE DADOS
                showarrow = False #Questão estética
            )]
        )
                

        return ('O ano selecionado foi {} e você já fez  \
                 {} pesquisas'.format(val_selected, num_clicks),fig)  #IRÁ RETORNAR OS INPUTS DECLARADOS LÁ EM CIMA, APARECERÁ DEBAIXO DO CAMPO PARA DIGITAR O ANO

if __name__ == '__main__':
    app.run_server(debug=True)
