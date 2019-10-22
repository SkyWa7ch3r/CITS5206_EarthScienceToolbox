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

# Six defferent line styles to choose from
line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']

# Features that are Categorical
cat_features = df.select_dtypes(include = 'object').columns.values

# Users can choose lines only, lines and markers and lines, markers and text
LABELSTYLE_DICT = [
    {'label': 'Lines', 'value': 'lines'},
    {'label': 'Lines & Markers', 'value': 'lines+markers'},
    {'label': 'Lines, Markers & Text', 'value': 'lines+markers+text'}
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

#
LINECOLOR_DICT = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
default_alpha = 0.65

toggle_switch_color = '#91c153'

col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
    col_idx += 1


app.layout = html.Div([
     html.Div([
        html.Div([
            # option to choose x value
            html.H6('Choose X value:'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in xnames],
                value=xnames[0],
                ),

            # option to choose y value, move from right side to choose x value to underneath x value
            html.H6('Select Variables'),
            dcc.Dropdown(
                id = 'select-variables',
                options = [{'label': i, 'value': i} for i in ynames],
                value = [ynames[0]],
                multi = True
                ),

            html.H6('Group By'),
            dcc.Dropdown(
                id = 'select-groupby',
                options = [{'label': i, 'value': i} for i in cat_features],
                value = str(cat_features[0])
                ),

            html.H6('Select Group'),
            dcc.RadioItems(
                id = 'select-group'
                ),

            # Pick a color for different lines
            daq.ColorPicker(
                id = 'colorpicker',
                label = 'Pick Color',
                style = {'background-color': 'white'},
                value = dict(rgb = dict(r = 0, g = 0, b = 255, a = 1))
                )
        ], style={'width': '48%', 'display': 'inline-block'}),

        #option to choose linear or log for y value
        html.Div([
            html.Div([
                html.H6('Data Transformation'),
                daq.ToggleSwitch(
                    id = 'data-transform',
                    label = ['Linear', 'Logarithmic'],
                    value = False,
                    size = '35',
                    color = toggle_switch_color
                )], style = {'padding': '0px 0px 360px 0px'}),

            daq.BooleanSwitch(
                id = 'show-gaps',
                on = False,
                label = 'Show Gaps',
                labelPosition = 'top',
                color = toggle_switch_color
                ),

            html.H6('Line Style'),
            dcc.Dropdown(
                id = 'line-style',
                options = [{'label': i, 'value': (i.replace(" ", "")).lower()} for i in line_style],
                value = (str(line_style[0]).replace(" ", "")).lower(),
                ),

            # Option to change marker style
            html.H6("Change Marker Style:"),
            dcc.Dropdown(
                id = 'alignment-markers-dropdown',
                className = 'markers-controls-block-dropdown',
                options = MARKERS_DICT,
                value = 'circle'
            ),

            # Option to change lable style
            html.H6("Change Label Style:"),
            dcc.Dropdown(
                id = 'alignment-labelstyle-dropdown',
                options = LABELSTYLE_DICT,
                value = 'lines'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        # All kinds of function buttons
        html.Div([
            html.H6('Function Buttons'),
            daq.BooleanSwitch(
                id = 'ALF',
                on = False,
                label = 'Add Line Fill',
                labelPosition = 'top',
                color = toggle_switch_color),
            daq.BooleanSwitch(
                id = 'show-gridlines',
                on = False,
                label = 'Gridlines',
                labelPosition = 'top',
                color = toggle_switch_color),
            daq.BooleanSwitch(
                id = 'show-zeroline-y',
                on = False,
                label = 'Show Y Zeroline',
                labelPosition = 'top',
                color = toggle_switch_color
                )
            ],
            style = {'width': '50%', 'display': 'inline-block', 'padding': '10px'}),

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

        # Change distances between y ticks
        html.H6("Change Y ticks:"),
        html.Div([
            dcc.Input(
                id = 'Y-dtick',
                type = 'number',
                min = 0,
                step = 0.1)
            ]),
    ], style = {'width': '45%', 'height': '100%', 'display': 'inline-block', 'float': 'left'}),

    # main graph
    html.Div([
        dcc.Graph(
            id = 'indicator-graphic',
            config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'legendPosition' : True, 'legendText' : True, 'colorbarPosition' : True, 'colorbarTitleText' : True}}),
            # set width and height of the main graph and move it to the right side of the page
            ],style = {'width': '48%', 'height': '100%', 'display': 'inline-block', 'float': 'right'},
            )
])


@app.callback(
    Output('colorpicker', 'value'),
    [Input('select-group', 'value')]
)
def update_line_color(yaxis):
    temp_str = LINECOLOR_DICT.get(yaxis, dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb = dict(r = temp_str[0], g = temp_str[1], b = temp_str[2], a = temp_str[3]))
    return temp_str


@app.callback(
    Output('select-group', 'options'),
    [Input('select-groupby', 'value')]
)
def update_group(groupby):
    idx = 0
    for i in df[groupby].unique():
        LINECOLOR_DICT[i] = default_color[idx % 5]
        idx += 1
    return [{'label': i, 'value': i} for i in df[groupby].unique()]




# Main callback
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('select-variables', 'value'),
     Input('data-transform', 'value'),
     Input('show-gridlines', 'on'),
     Input('show-zeroline-y', 'on'),
     Input('alignment-markers-dropdown', 'value'),
     Input('alignment-labelstyle-dropdown', 'value'),
     Input('show-gaps', 'on'),
     Input('ALF', 'on'),
     Input('opacity-slider', 'value'),
     Input('colorpicker', 'value'),
     Input('line-style', 'value'),
     Input('select-groupby', 'value'),
     Input('Y-dtick', 'value'),
     Input('select-group', 'value')
     ])
def update_graph(xaxis_column_name, select_variables,
                 data_transform,
                 show_gridlines, show_zeroline_y,
                 alignment_markers_dropdown,
                 alignment_labelstyle_dropdown, show_gaps, ALF,
                 OS,
                 colorPicker,
                 line_style,
                 groupby,
                 y_dtick,
                 select_group
                 ):
    group_list = df[groupby].unique()

    type_y = None
    if data_transform:
        type_y = 'log'

    yaxis_list = ynames

    picker_line_color = 'rgba({}, {}, {}, {})'.format(
        colorPicker['rgb']['r'],
        colorPicker['rgb']['g'],
        colorPicker['rgb']['b'],
        colorPicker['rgb']['a'])

    color_idx = 0
    for i in group_list:
        if select_group is not None:
            if i == select_group:
                LINECOLOR_DICT[i] = picker_line_color
            # else:
            #    box_color_saved[i] = default_color[color_idx % 5]
        color_idx += 1

    marker_idx = 0
    for i in group_list:
        if select_group is not None:
            if i == select_group:
                a = 0
        marker_idx += 1



    # Variable to change gaps
    ConnectGaps = True
    if show_gaps:
         ConnectGaps = False

    # Variable to change line fill
    Fill = "none"
    if ALF:
        Fill = "toself"

    # Variables for label styles
    lineStyle = dict()
    markerOnly = dict()
    if alignment_labelstyle_dropdown == 'lines':
        markerOnly = None
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)
    elif alignment_labelstyle_dropdown == 'lines+markers':
        markerOnly = dict(
            size = 8,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white', 'dash': line_style},
            symbol = alignment_markers_dropdown
        )
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)
    else:
        markerOnly = dict(
            size = 8,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white', 'dash': line_style},
            symbol = alignment_markers_dropdown
        )
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)

    traces_list = []
    for variable in select_variables:
        print("Var: {}".format(variable))
        for selection in group_list:
            traces_list.append(
                go.Scatter(
                    x=df[xaxis_column_name],
                    y=df[df[groupby] == selection][variable],
                    text=df[df[groupby] == selection][variable],
                    mode=alignment_labelstyle_dropdown,
                    name=str(variable).replace('[', '').replace(']', '').replace("\'", "")+': '+str(selection),
                    connectgaps = ConnectGaps,
                    fill = Fill,
                    opacity = OS/100,
                    marker = markerOnly,
                    line = dict(color=LINECOLOR_DICT[selection], width=3, dash=line_style)
                    )
                )

    return {
        'data': traces_list,
        'layout': go.Layout(
            xaxis={
                #'title' : xaxis_title,
                'showgrid': show_gridlines,
                #'zeroline': show_zeroline_x,
                'rangeslider': {'visible': True}, 'type': 'date'
            },
            yaxis={
                #'title' : yaxis_title,
                'type' : type_y,
                'showgrid': show_gridlines,
                'zeroline': show_zeroline_y,
                'dtick': y_dtick
                # new
                #'range': [range1[0], range1[1]]
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            #title= title_1,
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
