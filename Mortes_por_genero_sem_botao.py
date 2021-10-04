import pandas as pd
import plotly.graph_objects as go

dados = pd.read_csv("plotly/comparing-the-share-of-men-and-women-who-are-smoking.csv", sep=",")

'''
print(dados)
'''

dados_array = dados.values

'''
print(dados_array)
'''

'''
     Abaixo são declaradas listas vazias, que iram receber os anos (ano), porcentagem do sexo feminino (sexo_feminino), porcentagem do sexo masculino (sexo_masculino) e dois textos que iram aparecer 
nas colunas (Texto1 e Texto2), respectivamente.
'''
ano = []
sexo_feminino = []
sexo_masculino = []
texto1 = []
texto2 = []

'''
     Esse loop abaixo tem a função de verificar o nome as datas e só considerar as informações entre oa anos:
2007, 2010, 2012, 2014, 2016 e 2018.
'''   

'''
    O bloco condicional abaixo, que está dentro do loop, restringe os anaos especificos e o país especifico, cujos dados são desejados.
A função append vai adicioando os dados no final das linhas e prolongando as listas. O primeiro ano é 2007 e como os outros são pares de
2010 a 2018, entam foi usado o operador de resto ''linha[2] % 2 == 0''.
'''
                
for linha in dados_array:  
        
    
    if (linha[2] == 2007 or linha[2] >= 2010 and linha[2] <= 2018 and (linha[2] % 2 == 0)) and linha[0] == 'Brazil':
          
        
        
        ano.append(linha[2])
        sexo_feminino.append(linha[3])
        sexo_masculino.append(linha[4])
        texto1.append(f'{linha[0]} - {(linha[3]):.1f} %')
        texto2.append(f'{linha[0]} - {(linha[4]):.1f} %')

'''
    Essas listas texto1 e texto2 abaixo, iram receber uma string, com o nome do país e a porcentagem que ele tem 
para consumidores de tabaco do sexo feminino em texto1 e do sexo masculino em texto 2, ficando da seguinte forma:
Por exemplo: (''Brazil - 11,5 %''). 
'''        

'''
    Abaixo são criadas duas figuras relativas aos graficos, Barra1 para mostrar a porcentagem de uso do tabaco pelo genero feminino 
e Barra2 para mostrar a porcentagem de uso do tabaco pelo genero masculino, de 2007 a 2018.
'''

barra1 = go.Bar(
    x = sexo_masculino,
    y = ano, 
    text = texto2,                # text recebe o texto com a string presente nas variaveis Texto1, isso tambem é feito na estrutura de codigo do gráfico Barra2
    marker=dict(color='#0099ff'), # marker recebe a cor que a barra do grafico apareça, por exemplo: '#0099ff' equivale a cor azul
    name = "Sexo Masculino",      # name recebe a legenda do gráfico. Recebe o nome, no caso sexo masculino ou feminnino e asssocia a cor correspondente
    orientation='h'               # orientation recebe a orientação do grafico de barras. Nesse caso é no sentido horizontal
)

'''
Os mesmos comentarios feitos quanto a Barra1 valem para Barra2
'''

barra2 = go.Bar(
    x = sexo_feminino,
    y = ano,
    text = texto1,
    marker=dict(color='#404040'),
    name = "Sexo Feminino",
    orientation='h'
)

'''
grafico irá receber uma figura, que associa as duas barras, para comparar o a taxa de uso do tabaco entre os generos
'''

grafico = go.Figure([barra1, barra2])


'''
Esse layout abaixo é apenas para atribuir o titulo ao gráfico
'''

grafico.update_layout(
        title_text = 'Uso de tabaco por gênero, no Brasil, de 2007 a 2018',
)

grafico.show()
