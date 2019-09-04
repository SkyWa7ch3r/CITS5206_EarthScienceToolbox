import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_excel('UWA_acid_base_table_edit.xlsx')
ph = df['pH1:2']
ec = df['EC1:2']

app = dash.Dash(__name__)

features = df.columns.values

file_name = 'test'

if file_name == '':
    app.layout = html.Div([
        html.Div([
            dcc.Upload(
                id='file-upload',
                children=html.Div([
                    'Drag and Drop or ', html.A('klik to pick a files')
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
    ])
else:
    app.layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='features',
                options=[{'label':i, 'value':i} for i in features],
                value=str(features[0])
            )
        ])
    ])

if __name__ == '__main__':
    app.run_server(debug=True)