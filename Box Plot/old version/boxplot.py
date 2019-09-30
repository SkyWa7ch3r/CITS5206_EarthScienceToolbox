import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

file_name='data1.xlsx'

def read_file(filename):
    try:
        if 'csv' in filename:
            dff = pd.read_csv(filename)
        elif ('xls' or 'xlsx') in filename:
            dff = pd.read_excel(filename)
    except Exception as e:
        print (e)
        return u'There was an error opening {}'.format(filename)
    return dff

df = read_file(file_name)
features=df.select_dtypes(include='number').columns.values
feat_types=['int', 'float', 'object']
cat_features=df.select_dtypes(exclude='number').columns.values

colors = ['chocolate', 'darkorchid', 'aqua', 'goldenrod', 'hotpink']
colors_label={'chocolate':'Chocolate',
              'darkorchid':'Dark Orchid',
              'aqua':'Aqua',
              'goldenrod':'Golden Rod',
              'hotpink':'Hot Pink'}

app = dash.Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.H5('Feature:'),
            dcc.Dropdown(
                id='dd_features',
                options=[{'label':i, 'value':i} for i in features],
                value=str(features[0])
                )
            ]),
        html.Div([
            html.H5('Group by:'),
            dcc.Dropdown(
                id='dd_group',
                options=[{'label':j, 'value':j} for j in cat_features],
                value=cat_features[0]
                )
            ]),
        html.Div([
            html.H5('Color:'),
            dcc.Dropdown(
                id='dd_colors',
                options=[{'label':colors_label[i], 'value':i} for i in colors],
                value=colors[0]
        )
            ]),
        html.Div([
            html.H5('Main Title:'),
            dcc.Input(id='main_title', value='Main Title', type='text')
            ]),
        html.Div([
            html.H5('X-Axis Title:'),
            dcc.Input(id='xaxis_title', value='X Axis Title', type='text')
            ]),
        html.Div([
            html.H5('Y-Axis Title:'),
            dcc.Input(id='yaxis_title', value='Y Axis Title', type='text')
            ]),
        html.Div([
            html.H5('Show Legend:'),
            dcc.RadioItems(
                id='show_legend',
                options=[{'label': i, 'value': i} for i in ['True', 'False']],
                value='True'
                )
            ]),
        html.Div([
            html.H5('Y Axis Tick Steps:'),
            dcc.Slider(
                id='yaxis-slider',
                min=5,
                max=20,
                step=5,
                value=10,
                marks={5: '5', 10: '10', 15: '15', 20: '20'},
                included=False,
                dots=True
                )
            ]),
        ], style={'width': '30%', 'display': 'inline-block'},
    ),
    html.Div([
        dcc.Graph(id='box-plot')
        ], style={'width': '70%', 'float': 'right', 'display': 'inline-block'},
    )
])


@app.callback(
    Output(component_id='box-plot', component_property='figure'),
    [Input(component_id='dd_group', component_property='value'),
     Input(component_id='dd_features', component_property='value'),
     Input(component_id='dd_colors', component_property='value'),
     Input('main_title', 'value'),
     Input('xaxis_title', 'value'),
     Input('yaxis_title', 'value'),
     Input('show_legend', 'value'),
     Input('yaxis-slider', 'value')
     ]
)
def update_figure(groupby, value, clr, main_title, xaxs_title, yaxs_title, show_lgnd, dtick):
    if show_lgnd == 'True':
        show_lgnd = True
    else:
        show_lgnd = False

    return {
        'data': [go.Box(
            x=df[groupby],
            y=df[value],
            name=value,
            marker_color=clr
            )],
        'layout': go.Layout(
            xaxis=go.layout.XAxis(
                title=xaxs_title
            ),
            yaxis=go.layout.YAxis(
                title=yaxs_title,
                dtick=dtick,
                showgrid=True
            ),
            title=main_title,
            showlegend=show_lgnd
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
