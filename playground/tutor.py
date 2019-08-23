import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_excel ('UWA_acid_base_table.xlsx')
#print(df.columns.values.tolist())
asppm = df[:]['AS_PPM']
mpa = df[:]['MPA']
anc = df[:]['ANC']
cls = df[:]['Class'].unique()
x = mpa
y = anc
hole_id = df[:]['Hole ID']

app.layout = html.Div([
    dcc.Graph(
        id='asppm-vs-mpa',
        figure={
            'data': [
                go.Scatter(
                    x=mpa,
                    y=anc,
                    text=hole_id,
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'
                                 }
                        }#,
                    #name=i
                    ) #for i in df[:]['LITH_G']
                ],
            'layout': go.Layout(
                xaxis={'type':'log', 'title': 'log MPA'},
                yaxis={'title': 'ANC'},
                margin={'l': 50, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
                )
            }
        )
    ])

if __name__ == '__main__':
    app.run_server(debug=True)