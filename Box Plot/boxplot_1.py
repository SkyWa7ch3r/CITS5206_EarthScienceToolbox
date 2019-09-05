import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.graph_objs as go

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

upload_dcc = html.Div([
    dcc.Upload(
    id='upload-file',
    children=html.Div([
        'Drag and Drop or ', html.A('Select a File')
    ]),
    style={
        'width': '50%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': '10px'
    },
    multiple=False
    )
])

html_content = html.Div(id='file-content')

def read_file(file_name):
    try:
        if 'csv' in file_name:
            df = pd.read_csv(file_name)
        elif ('xls' or 'xlsx') in file_name:
            df = pd.read_excel(file_name)
    except Exception as e:
        print (e)
        return u'There was an error opening {}'.format(file_name)
    
    features = df.columns.values
    
    children = html.Div([
        html.H5("Data Features:"),
        dcc.Dropdown(
            id='dd_features',
            options=[{'label':i, 'value':i} for i in features],
            value=str(features[0])
            ),
        dcc.Graph(
            id='box-plot',
            figure={
            'data': [go.Box(
                y=df[features[0]],
                name=features[0]
                )],
            })
    ])
    
    return children

app.layout = html.Div([
    upload_dcc,
    html_content,
    html.Div(id='plot-content')
])

@app.callback(Output('file-content', 'children'),
              [Input('upload-file', 'filename')],
              )
def update_output(file_name):
    df = ''
    if (file_name != None):
        df = read_file(file_name)
    return df

if __name__ == '__main__':
    app.run_server(debug=True)