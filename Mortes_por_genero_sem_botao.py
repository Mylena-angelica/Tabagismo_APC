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
     Abaixo são declaradas listas vazias, que iram receber os anos (ano), porcentagem do sexo feminino (sf), porcentagem do sexo masculino (sm) e dois textos que iram aparecer 
nas colunas (Texto1 e Texto2), respectivamente.
'''
ano = []
sf = []
sm = []
Texto1 = []
Texto2 = []

'''
     Esse loop abaixo tem a função de verificar o nome as datas e só considerar as informações entre oa anos:
2007, 2010, 2012, 2014, 2016 e 2018.
'''             
        
for linha in dados_array:  
        
        '''
              O bloco condicional abaixo, restringe os anaos especificos e o país especifico, cujos dados são desejados.
        A função append vai adicioando os dados no final das linhas e prolongando as listas.
        '''
        
    if (linha[2] == 2007 or linha[2] >= 2010 and linha[2] <= 2018 and (linha[2] % 2 == 0)) and linha[0] == 'Brazil':
          
        ano.append(linha[2])
        sf.append(linha[3])
        sm.append(linha[4])
        
        '''
             Essas listas Texto1 e Texto2 abaixo, iram receber uma string, com o nome do país e a porcentagem que ele tem 
        para mortes dos sexo feminino em Texto1 e mortes dos sexo masculino em Texto 2, ficando da seguinte forma:
        Por exemplo: (''Brazil - 11,5 %''). 
        '''
        
        Texto1.append(f'{linha[0]} - {(linha[3]):.1f} %')
        Texto2.append(f'{linha[0]} - {(linha[4]):.1f} %')

'''
    Abaixo são criadas duas figuras relativas aos graficos, Barra1 para mostrar a porcentagem de mortes do genero feminino 
e Barra2 para mostrar a porcentagem de mortes do genero masculino, de 2007 a 2018.
'''

barra1 = go.Bar(
    x = sm,
    y = ano,
        
        '''
        text recebe o texto com a string presente nas variaveis Texto1, isso tambem é feito na estrutura de codigo do gráfico Barra2
        '''
        
    text = Texto2,
        
        '''
        marker recebe a cor que a barra do grafico apareça, por exemplo: '#0099ff' equivale a cor azul
        '''
        
    marker=dict(color='#0099ff'),      
        
        '''
        name recebe a legenda do gráfico. Recebe o nome, no caso sexo masculino ou feminnino e asssocia a cor correspondente
        '''
        
    name = "Sexo Masculino",
        
        '''
        orientation recebe a orientação do grafico de barras. Nesse caso é no sentido horizontal
        '''
        
    orientation='h'
)

'''
Os mesmos comentarios feitos quanto a Barra1 valem para Barra2
'''

barra2 = go.Bar(
    x = sf,
    y = ano,
    text = Texto1,
    marker=dict(color='#404040'),
    name = "Sexo Feminino",
    orientation='h'
)

'''
grafico irá receber uma figura, que associa as duas barras, para comparar o a taxa de mortes entre os generos
'''

grafico = go.Figure([barra1, barra2])


'''
Esse layout abaixo é apenas para atribuir o titulo ao gráfico
'''

grafico.update_layout(
        title_text = 'Numero de mortes por gênero em função do uso de tabaco, no Brasil, de 2007 a 2018',
)

grafico.show()
