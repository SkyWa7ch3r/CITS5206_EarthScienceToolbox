import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from numpy import arange, array, ones
import pandas as pd
import plotly.graph_objs as go
import dash_daq as daq

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



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
    {'value': 'dashDot', 'label': 'dashDot'},
    {'value': 'longDash', 'label': 'longDash'},
    {'value': 'longDashDot', 'label': 'longDashDot'}
]


app.layout = html.Div([
     html.Div([
        html.Div([
            # option to choose x value
            html.H6("Choose X value:"),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in xnames],
                value=xnames[0],
            ),

            # option to choose y value, move from right side to choose x value to underneath x value 
            html.H6("Choose Y value:"),
            dcc.Dropdown(
                id = 'yaxis-column',
                options = [{'label': i, 'value': i} for i in ynames],
                value = [ynames[0]],
                multi = True
            )
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        #option to choose linear or log for y value
        html.Div([
            html.H6("Linear or Logarithmic:"),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        # Set the title of the plot
        html.Div([
            html.H6('Plot Title'),
            dcc.Input(
                id="title",
                type="text",
                placeholder="title")
            ],
            style={'width': '33%', 'float': 'left', 'display' : 'inline-block'}),

        #This is the title for X axes
        html.Div([
            html.H6('X-Axis Title:'),
            dcc.Input(
                id='xaxis_title',
                value=xnames[0],
                type='text')
            ],
            style={'width': '33%', 'float': 'center', 'display' : 'inline-block'}),

        #This is the title for Y axes
        html.Div([
            html.H6('Y-Axis Title:'),
            dcc.Input(id='yaxis_title',
                value=ynames[0],
                type='text')
            ],
            style={'width': '33%', 'float': 'rifght', 'display' : 'inline-block'}),

        # option to choose marker style
        html.H6("Change Marker Style:"),
        dcc.Dropdown(
            id = 'alignment-markers-dropdown',
            className = 'markers-controls-block-dropdown',
            options = MARKERS_DICT,
            value = 'circle'
            ),

        # All kinds of function buttons
        html.H6("Function Buttons:"),
        html.Div([
            html.Button('Hide or Show grid line', id = 'GL'),
            html.Button('Hide or Show zero line', id = 'OL')
            ],
            style = {'width': '100%', 'display': 'inline-block'}),

        html.H6("Change Opacity:"),
        html.Div([
            dcc.Slider(
                id = 'opacity-slider',
                min = 0,
                max = 100,
                value = 50
            )
        ]),

        # Change distance of X ticks and Y ticks
        html.H6("Change X ticks:"),
        html.Div([
            dcc.Input(
                id = 'X-dtick',
                type = 'number')
            ]),

        html.H6("Change Y ticks:"),
        html.Div([
            dcc.Input(
                id = 'Y-dtick',
                type = 'number')
            ]),    

        html.Div([
            html.H6("Change Colorscale:"),
            dcc.Dropdown(
                # option to choose colorscale
                id = 'alignment-colorscale-dropdown',
                className = 'app-controls-block-dropdown',
                options = COLORSCALES_DICT,
                value = 'Blackbody'
            ),

            html.Div("Color and Hover Text Grouping"),
            dcc.Dropdown(
                id = 'color-drop',
                options = [{'label': i, 'value': i} for i in df.columns],
                value = df.columns[0]
                )
            ]),
    ], style = {'width': '45%', 'height': '100%', 'display': 'inline-block', 'float': 'left'}),

    html.Div([html.Span(ynames[0], className="column",
        style={"text-align": "center", "border": "1px solid #ccc"}),
        html.Div([dcc.RangeSlider(id='range1',min=0,max=100000000,step=500,updatemode="drag",value=[0, 20000000],
                marks={10000000: "10M",20000000: "20M",30000000: "30M",40000000: "40M",
                50000000: "50M",60000000: "60M",70000000: "70M",80000000: "80M",
                90000000: "90M",100000000: "100M"})], className="column",
        style={"margin": 0, "padding": 10})], className="row", style={'width': '48%', 'padding': 15}),

    # main graph
    html.Div([
        dcc.Graph(
            id = 'indicator-graphic'),
            # set width and height of the main graph and move it to the right side of the page
            ],style = {'width': '48%', 'height': '100%', 'display': 'inline-block', 'float': 'right'})
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
     Input('alignment-markers-dropdown', 'value'),
     Input('range1', 'value'),
     Input('line-style', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 yaxis_type,
                 title_1, alignment_colorscale_dropdown,
                 xaxis_title, yaxis_title, GL, OL,
                 alignment_markers_dropdown, range1, line_style):
    
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
                'zeroline': O_click,
                # new
                'range': [range1[0], range1[1]]
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            title= title_1,
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)