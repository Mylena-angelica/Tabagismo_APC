from logging import debug
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

dados=pd.read_csv('tobacco-production.csv', sep=',')

app = dash.Dash(__name__)

#---------------------------------------------------------------
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2017,
                  max=2018, min=1961, required=True),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center'}),

])

#---------------------------------------------------------------
@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State(component_id='input_state', component_property='value')]
)

def update_output(num_clicks, val_selected):
    if val_selected is None:
        raise PreventUpdate
    else:
        dados_array=dados.values

        pais=[]
        ano=[]
        producao=[]

        for linha in dados_array:
            if linha[2]== val_selected:
                pais.append(linha[1])
                ano.append(linha[2])
                producao.append(linha[3])

        for codes in pais:
            if not type(codes)== str:
                if math.isnan(float(codes)):
                    index=pais.index(codes)
                    del pais[index]
                    del ano[index]
                    del producao[index]
            elif codes=='OWID_WRL':
                index=pais.index(codes)
                del pais[index]
                del ano[index]
                del producao[index]

        dados_array = px.data.gapminder().query("year=={}".format(val_selected))
        # print(df[:3])

        fig = go.Figure(data=go.Choropleth(
            locations = pais,
            z = producao,
            text = val_selected,
            colorscale = 'sunsetdark',
            autocolorscale=False,
            reversescale=True,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            colorbar_tickprefix = ' Toneladas ',
            colorbar_title = 'Produção em <br>toneladas',
        ))

        fig.update_layout(
            title_text='Produção mundial de tabaco',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='equirectangular'
            ),
            annotations = [dict(
                x=0.55,
                y=0.1,
                xref='paper',
                yref='paper',
                text='Fonte: <a href="https://www.cia.gov/library/publications/the-world-factbook/fields/2195.html">\
                    Our world in Data</a>',
                showarrow = False
            )]
        )

        return ('O ano selecionado foi "{}" e você já fez  \
                 {} pesquisas'.format(val_selected, num_clicks), fig)

if __name__ == '__main__':
    app.run_server(debug=True)


