import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import flask
#import numpy as np
import plotly.graph_objs as go
import pandas as pd

df = pd.read_excel ('UWA_acid_base_table.xlsx')


server = flask.Flask('app')

app = dash.Dash('app', server=server)
app.scripts.config.serve_locally = False

app.layout = html.Div([
    html.H1('Test'),
    dcc.Input(
        id='my-input',
        placeholder='Enter a value...',
        type='text',
        value='Box Plot'
    ),
    dcc.Graph(id='my-graph')
], className="container")

@app.callback(Output('my-graph', 'figure'),
              [Input('my-input', 'value')])
def update_graph(input_text):
    y0 = df[:]['pH1:2']
    y1 = df[:]['NAGpH']
    ph12 = go.Box(y=y0)
    nagph = go.Box(y=y1)
    data = [ph12, nagph]
    return {
        'data': data,
        'layout': go.Layout(
            title=input_text
        )
    }

if __name__ == '__main__':
    app.run_server()