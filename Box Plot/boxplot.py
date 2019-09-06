import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

file_name='data.xlsx'

def read_file(file_name):
    try:
        if 'csv' in file_name:
            df = pd.read_csv(file_name)
        elif ('xls' or 'xlsx') in file_name:
            df = pd.read_excel(file_name)
    except Exception as e:
        print (e)
        return u'There was an error opening {}'.format(file_name)
    return df

df = read_file(file_name)
features=df.columns.values
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H5('Data Features:'),
        dcc.Dropdown(
            id='dd_features',
            options=[{'label':i, 'value':i} for i in features],
            value=str(features[0])
        )
    ]),
    dcc.Graph(id='box-plot')
])

@app.callback(
    Output(component_id='box-plot', component_property='figure'),
    [Input(component_id='dd_features', component_property='value')]
)
def update_figure(value):
    return {
        'data': [go.Box(
            y=df[value],
            name=value
            )], 
    }


if __name__ == '__main__':
    app.run_server(debug=True)