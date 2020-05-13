
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from data import get_similar_sentences
import flask
import dash_table
import pandas as pd

queries = ['Range of incubation periods for the disease in humans', 'antiviral covid-19 success treatment','virus detected from animals?', 'risk of fatality among symptomatic hospitalized patients']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([

html.H1('HAP880 Project - COVID-19 Research Semantic Search ',style={'textAlign': 'center',"background": "lightblue"}),


dcc.Input(id='my-id', value='Range of incubation periods for the disease in humans',
                  type='search',
                  placeholder="Ask your Query here like Range of incubation periods for the disease in humans or What are the rapid molecular diagnostics for COVID-19",
                  style={'display': 'flex', 'verticalAlign': "middle", 'justifyContent': 'center', 'width': '60%',
                         'textAlign': 'center'}),


html.Div([
                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                    dcc.Tab(label='Research Article Search', value='tab-1',style={'textAlign': 'center','font-size': '32px',"background": "lightblue"}),
                    dcc.Tab(label='Topic Modelling of Articles', value='tab-2',style={'textAlign': 'center','font-size': '32px',"background": "lightblue"}),
dcc.Tab(label='Clustering of Articles', value='tab-3',style={'textAlign': 'center','font-size': '32px',"background": "lightblue"})
                ]),
                html.Div(id='tabs-example-content')
                ]),


])


@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(children=[html.Table(id='my-div')])

        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Iframe(src=app.get_asset_url('scispacylda.html'),
                        style=dict(position="absolute",width="100%", height="100%"))
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Iframe(src=app.get_asset_url('tsne.html'),
                        style=dict(position="absolute",width="100%", height="100%"))
        ])











@app.callback(
    Output(component_id='my-div', component_property='children'),
    [Input(component_id='my-id', component_property='value')]
)

def update_output_div(input_value):
    queries = input_value
    dataframe = get_similar_sentences([queries])
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            # update this depending on which
            # columns you want to show links for
            # and what you want those links to be
            if col == 'url':
                cell = html.Td(html.A(href=value, children=value))
            else:
                cell = html.Td(children=value)
            row.append(cell)
        rows.append(html.Tr(row))
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns],style={'color':'#FFFFFF',
                                                'background-color':'#76e8a8'})] +

        rows,
    style = {'color': '#FFFFFF',
             'background-color': '#76e8a8'}
    )



if __name__ == '__main__':
    app.run_server(host='10.193.124.234')