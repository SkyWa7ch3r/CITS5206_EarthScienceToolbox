import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from scipy import stats
from numpy import arange,array,ones
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


file_name='UWA_acid_base_table.xlsx'


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

cnames = df.select_dtypes(include='number').columns.values

COLORSCALES_DICT = [
    {'value': 'Blackbody', 'label': 'Blackbody'},
    {'value': 'Bluered', 'label': 'Bluered'},
    {'value': 'Blues', 'label': 'Blues'},
    {'value': 'Earth', 'label': 'Earth'},
    {'value': 'Electric', 'label': 'Electric'},
    {'value': 'Greens', 'label': 'Greens'},
    {'value': 'Greys', 'label': 'Greys'},
    {'value': 'Hot', 'label': 'Hot'},
    {'value': 'Jet', 'label': 'Jet'},
    {'value': 'Picnic', 'label': 'Picnic'},
    {'value': 'Portland', 'label': 'Portland'},
    {'value': 'Rainbow', 'label': 'Rainbow'},
    {'value': 'RdBu', 'label': 'RdBu'},
    {'value': 'Reds', 'label': 'Reds'},
    {'value': 'Viridis', 'label': 'Viridis'},
    {'value': 'YlGnBu', 'label': 'YlGnBu'},
    {'value': 'YlOrRd', 'label': 'YlOrRd'},
]

MARKERS_DICT = [
    {'value': 'circle', 'label': 'circle'},
    {'value': 'square', 'label': 'square'},
    {'value': 'diamond', 'label': 'diamond'},
    {'value': 'cross', 'label': 'cross'},
    {'value': 'x', 'label': 'x'},
    {'value': 'triangle-up', 'label': 'triangle-up'},
    {'value': 'pentagon', 'label': 'pentagon'},
    {'value': 'hexagon', 'label': 'hexagon'},
    {'value': 'hexagon2', 'label': 'hexagon2'},
    {'value': 'octagon', 'label': 'octagon'},
    {'value': 'star', 'label': 'star'},
    {'value': 'hexagram', 'label': 'hexagram'},
    {'value': 'star-triangle-up', 'label': 'star-triangle-up'},
    {'value': 'hourglass', 'label': 'hourglass'},
    {'value': 'bowtie', 'label': 'bowtie'},
]



app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in cnames],
                value=cnames[0],
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in cnames],
                value=cnames[-1],
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
                
        html.Div([
            html.Button('Swap Axes', id='swap'),
            ]),

        html.Div([
            html.Button('Show the Linear Fit', id='linear'),
            ]),


        html.Div([
            dcc.Input(
                id="title",
                type="text",
                placeholder="title")
            ]
            + [html.Div(id="out-all-types")]
            ),

        html.Div([
            dcc.Input(
                id="x_label",
                type="text",
                value=cnames[0],
                placeholder=cnames[0]),

            dcc.Input(
                id="y_label",
                type="text",
                value=cnames[-1],
                placeholder=cnames[-1])
            ]),

        html.Div([
            html.Button('Hide or Show grid line', id='GL'),
            html.Button('Hide or Show zero line', id='OL')
            ])
    
    ]),

    html.Div(id='alignment-body', className='app-body', children=[
        html.Div([
            html.Div(id='alignment-control-tabs', className='control-tabs', children=[
                        dcc.Tab(
                            label='Graph',
                            value='control-tab-customize',
                            children=html.Div(className='control-tab', children=[
                                html.Div([
                                    html.H3('General', className='alignment-settings-section'),
                                    html.Div(
                                        className='app-controls-block',
                                        children=[
                                            html.Div(className='app-controls-name',
                                                     children="Colorscale"),
                                            dcc.Dropdown(
                                                id='alignment-colorscale-dropdown',
                                                className='app-controls-block-dropdown',
                                                options=COLORSCALES_DICT,
                                                value='Blackbody',
                                            ),
                                            html.Div(
                                                className='app-controls-desc',
                                                children='Choose the color theme of the viewer.'
                                            )
                                        ],
                                    ),
                                ]),
                                
                            ]),
                        ),
            ]),
        ]),
        dcc.Store(id='alignment-data-store'),
    ]),

    dcc.Dropdown(
            id='alignment-markers-dropdown',
            className='markers-controls-block-dropdown',
            options=MARKERS_DICT,
            value='circle',
    ),

    dcc.Graph(id='indicator-graphic'),
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('title', 'value'),
     Input('alignment-colorscale-dropdown', 'value'),
     Input('swap', 'n_clicks'),
     Input('linear', 'n_clicks'),
     Input('x_label', 'value'),
     Input('y_label', 'value'),
     Input('GL', 'n_clicks'),
     Input('OL', 'n_clicks'),
     Input('alignment-markers-dropdown', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 title_1, alignment_colorscale_dropdown, swap, linear, x_label, y_label, GL, OL, alignment_markers_dropdown):
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    line = slope*df[xaxis_column_name]+intercept


    if swap != None and int(swap) % 2 == 1:
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp

    l_click = False
    if linear != None and int(linear) % 2 == 1:
        l_click = True
    
    G_click = False
    if GL != None and int(GL) % 2 == 1:
        G_click = True

    O_click = False
    if OL != None and int(OL) % 2 == 1:
        O_click = True

    return {
        'data': [go.Scatter(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            text=xaxis_column_name,
            mode='markers',
            marker=dict(
                size = 15,
                opacity = 0.5,
                line = {'width': 0.5, 'color': 'white'},
                color = df[xaxis_column_name],
                colorscale = alignment_colorscale_dropdown,
                showscale = True,
                symbol = alignment_markers_dropdown
            ),

        ),
        
        go.Scatter(
                x=df[xaxis_column_name],
                y=line,
                mode='lines',
                marker=dict(
                    size = 15,
                    opacity = 0.5,
                    line = {'width': 0.5, 'color': 'white'},
                    color = 'black',
                    colorscale = alignment_colorscale_dropdown,
                    showscale = True,
            ),
                name='Fit',
                visible=l_click
                    )
        ],

        'layout': go.Layout(
            xaxis={
                'title': x_label,
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
                'showgrid': G_click,
                'zeroline': O_click
            },
            yaxis={
                'title': y_label,
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'showgrid': G_click,
                'zeroline': O_click
            },

            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            title= title_1,
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
