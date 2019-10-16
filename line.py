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
import colorlover as cl


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

# Data without date and time
names = df.select_dtypes(exclude='number').columns.values

# Date and time in list xnames
xnames = []
for col in names:
    if 'date' in col.lower() or 'time' in col.lower():
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        xnames.append(col)

# Other data in ynames
ynames = df.select_dtypes(include='number').columns.values

# Users can choose lines only, lines and markers and lines, markers and text
LABELSTYLE_DICT = [
    {'label': 'lines', 'value': 'lines'},
    {'label': 'lines+markers', 'value': 'lines+markers'},
    {'label': 'lines+markers+text', 'value': 'lines+markers+text'}
]

# Line colors users can choose from 
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

# Marker styles users can choose from
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

# Six different line styles users can choose from
LINESTYLES_DICT = [
    {'value': 'solid', 'label': 'solid'}, 
    {'value': 'dash', 'label': 'dash'},
    {'value': 'dot', 'label': 'dot'},
    {'value': 'dashDot', 'label': 'dashDot'},
    {'value': 'longDash', 'label': 'longDash'},
    {'value': 'longDashDot', 'label': 'longDashDot'}
]

#
LINECOLOR_DICT = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
default_alpha = 0.65


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

        # This is the title for Y axes
        html.Div([
            html.H6('Y-Axis Title:'),
            dcc.Input(id='yaxis_title',
                value=ynames[0],
                type='text')
            ],
            style={'width': '33%', 'float': 'rifght', 'display' : 'inline-block'}),

        # Option to choose marker style
        html.H6("Change Marker Style:"),
        dcc.Dropdown(
            id = 'alignment-markers-dropdown',
            className = 'markers-controls-block-dropdown',
            options = MARKERS_DICT,
            value = 'circle'
            ),

        # Option to change line style
        html.H6("Change Line Style:"),
        dcc.Dropdown(
            id = 'alignment-linestyle-dropdown',
            className = 'linestyle-controls-block-dropdown',
            options = LINESTYLES_DICT,
            value = 'solid'
            ),

        # Option to change lable style
        html.H6("Change Label Style:"),
        dcc.Dropdown(
            id = 'alignment-labelstyle-dropdown',
            options = LABELSTYLE_DICT,
            value = 'lines'
            ),

        # All kinds of function buttons
        html.Div([
            daq.BooleanSwitch(label = 'Show Gaps', id = 'SG', on = False),
            daq.BooleanSwitch(label = 'Add Line Fill', id = 'ALF', on = False)],
            style = {'width': '50%', 'display': 'inline-block', 'padding': '10px'}),


        html.H6("Function Buttons:"),
        html.Div([
            html.Button('Hide or Show grid line', id = 'GL'),
            html.Button('Hide or Show zero line', id = 'OL')
            ],
            style = {'width': '100%', 'display': 'inline-block'}),

        # Slider to change line opacity
        html.H6("Change Opacity:"),
        html.Div([
            dcc.Slider(
                id = 'opacity-slider',
                min = 0,
                max = 100,
                value = 85
            )
        ]),

        # Change distance of X ticks and Y ticks
        html.H6("Change X ticks:"),
        html.Div([
            dcc.Input(
                id = 'X-dtick',
                type = 'number')
            ]),

        # Change distances between y ticks
        html.H6("Change Y ticks:"),
        html.Div([
            dcc.Input(
                id = 'Y-dtick',
                type = 'number')
            ]),    

        # Change different colors
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
    
    
    # Select a particular line
    html.Div([
        html.H6('Select Line'),

        
        html.Div([
        dcc.RadioItems(
            id = 'select-line',
            )
        ]),

        # Pick a color for different lines
        html.Div([
            daq.ColorPicker(
                id = 'line-color',
                label = 'Line Color',
                value = dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
            ]),
        ], style = {'width': '48%', 'display': 'inline-block'}),


    # main graph
    html.Div([
        dcc.Graph(
            id = 'indicator-graphic'),
            # set width and height of the main graph and move it to the right side of the page
            ],style = {'width': '48%', 'height': '100%', 'display': 'inline-block', 'float': 'right'})
])



@app.callback(
    Output('line-color', 'value'),
    [Input('select-line', 'value')]
)
def update_line_color(yaxis):
    temp_str = LINECOLOR_DICT.get(yaxis, dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb = dict(r = temp_str[0], g = temp_str[1], b = temp_str[2], a = temp_str[3]))
    return temp_str

# Change the selected y axis
@app.callback(
    Output('select-line', 'options'),
    [Input('yaxis-column', 'value')]
)
def update_yaxis(yaxis_column):
    idx = 0
    for i in df[yaxis_column]:
        LINECOLOR_DICT[i] = default_color[idx % 5]
        idx += 1
    return [{'label': i, 'value': i} for i in df[yaxis_column]]

# Main callback
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
     Input('alignment-labelstyle-dropdown', 'value'),
     Input('SG', 'on'),
     Input('ALF', 'on'),
     Input('opacity-slider', 'value'),
     Input('line-color', 'value'),
     Input('select-line', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 yaxis_type,
                 title_1, alignment_colorscale_dropdown,
                 xaxis_title, yaxis_title, GL, OL,
                 alignment_markers_dropdown,
                 alignment_labelstyle_dropdown, SG, ALF, OS, line_color,
                 select_line):
    
    yaxis_list = ynames
    
    picker_line_color = 'rgba({}, {}, {}, {})'.format(
        line_color['rgb']['r'],
        line_color['rgb']['g'],
        line_color['rgb']['b'],
        line_color['rgb']['a'])
    
    color_idx = 0
    for i in yaxis_list:
        if select_line is not None:
            print('select_line: {}'.format(select_line))
            print('line color 1: {}'.format(LINECOLOR_DICT))
            if i == select_line:
                LINECOLOR_DICT[i] = picker_line_color

        color_idx += 1


    G_click = False
    if GL != None and int(GL) % 2 == 1:
        G_click = True

    O_click = False
    if OL != None and int(OL) % 2 == 1:
        O_click = True

    ConnectGaps = True
    if SG:
         ConnectGaps = False

    # Variable to change line fill
    # 可能有其他参数 减小fill的范围
    Fill = "none"
    if ALF:
        Fill = "toself"

    # Variables for label styles
    lineStyle = dict()
    MarkerOnly = dict()
    if alignment_labelstyle_dropdown == 'lines':
        MarkerOnly = None
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                line_color['rgb']['r'],
                line_color['rgb']['g'],
                line_color['rgb']['b'],
                line_color['rgb']['a'],), width = 3)
    elif alignment_labelstyle_dropdown == 'lines+markers':
        MarkerOnly = dict(
            size = 8,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white'},
            symbol = alignment_markers_dropdown
        )
        lineStyle = None
    #else:

        


    traces_list = []
    for col in yaxis_column_name:
        traces_list.append(
            go.Scatter(
                x=df[xaxis_column_name],
                y=df[col],
                text=df[col],
                mode=alignment_labelstyle_dropdown,
                name=col,
                connectgaps = ConnectGaps,
                fill = Fill,
                opacity = OS/100,
                marker = MarkerOnly,
                line = lineStyle
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
                #'range': [range1[0], range1[1]]
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            title= title_1,
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)