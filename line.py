import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from numpy import arange, array, ones
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('https://raw.githubusercontent.com/cszdzr/DataFile_RainierWeather/master/Rainier_Weather.csv?token=AM4CACREQ55DGSX372CISTK5PHQ6O')


#data = df.select_dtypes(include = 'datetime').columns.values

file_name='Rainier_Weather.csv'


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

names = df.select_dtypes(exclude='number').columns.values
xnames = []
for col in names:
    if 'date' in col.lower() or 'time' in col.lower():
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        xnames.append(col)

ynames = df.select_dtypes(include='number').columns.values

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

LINESTYLE_DICT = [

    {'value': 'solid', 'label': 'solid'}, 
    {'value': 'dash', 'label': 'dash'},
    {'value': 'dot', 'label': 'dot'},
    {'value': 'dashdot', 'label': 'dashdot'}
]


app.layout = html.Div([
     html.Div([

        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in xnames],
                value=xnames[0],
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in ynames],
                value=[ynames[0]],
                multi=True,
            ),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        #This is the form for the title of the plot
        html.Div([
            html.H5('Plot Title'),
            dcc.Input(
                id="title",
                type="text",
                placeholder="title")
            ]
        , style={'display' : 'inline-block', 'padding-right' : '5px'}),
        #This is the title for the X axes
        html.Div([
            html.H5('X-Axis Title:'),
            dcc.Input(id='xaxis_title', value=xnames[0], type='text')
            ], style={'display' : 'inline-block', 'padding-right' : '5px'}),
        #This is the title for Y axes
        html.Div([
            html.H5('Y-Axis Title:'),
            dcc.Input(id='yaxis_title', value=ynames[0], type='text')
            ], style={'display' : 'inline-block'}),
        html.Div([
            html.Button('Hide or Show grid line', id = 'GL'),
            html.Button('Hide or Show zero line', id = 'OL')
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
        id = 'alignment-markers-dropdown',
        className = 'markers-controls-block-dropdown',
        options = MARKERS_DICT,
        value = 'square'),

    dcc.Graph(id='indicator-graphic'),
])

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('yaxis-type', 'value'),
     Input('title', 'value'),
     Input('alignment-colorscale-dropdown', 'value'),
     Input('xaxis_title', 'value'),
     Input('yaxis_title', 'value'),
     Input('GL', 'n_clicks'),
     Input('OL', 'n_clicks'),
     Input('alignment-markers-dropdown', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 yaxis_type,
                 title_1, alignment_colorscale_dropdown,
                 xaxis_title, yaxis_title, GL, OL,
                 alignment_markers_dropdown):
    
    G_click = False
    if GL != None and int(GL) % 2 == 1:
        G_click = True

    O_click = False
    if OL != None and int(OL) % 2 == 1:
        O_click = True


    traces_list = []
    for col in yaxis_column_name:
        traces_list.append(
            go.Scatter(
                x=df[xaxis_column_name],
                y=df[col],
                text=xaxis_column_name,
                mode='lines',
                name=col,
                marker=dict(
                    size = 15,
                    opacity = 0.5,
                    line = {'width': 0.5, 'color': 'white'},
                    color = df[col],
                    colorscale = alignment_colorscale_dropdown,
                    showscale = True,
                    symbol = alignment_markers_dropdown
                )
            )
        )
        
    return {
        'data': traces_list,

        'layout': go.Layout(
            xaxis={
                'title' : xaxis_title,
                'showgrid': G_click,
                'zeroline': O_click,
                'rangeslider': {'visible': True}, 'type': 'date'
            },
            yaxis={
                'title' : yaxis_title,
                'type' : yaxis_type.lower(),
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