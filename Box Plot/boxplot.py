import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_excel('UWA_acid_base_table_edit.xlsx')
ph = df['pH1:2']
ec = df['EC1:2']

app = dash.Dash(__name__)

app.layout = html.Div(
    dcc.Graph(
        id='pH',
        figure={
            'data':[
                go.Box(y=ph, name='pH1:2')
                ],
            'layout': go.Layout()
            }
        )
    )

if __name__ == '__main__':
    app.run_server(debug=True)