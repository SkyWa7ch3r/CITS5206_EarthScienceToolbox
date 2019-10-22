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
datetime = []
for col in names:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        datetime = df[col]

# Other data in ynames
ynames = df.select_dtypes(include='number').columns.values

# Six defferent line styles to choose from
linestyle_list = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']

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
    {'value': 'circle', 'label': 'Circle'},
    {'value': 'square', 'label': 'Square'},
    {'value': 'diamond', 'label': 'Diamond'},
    {'value': 'cross', 'label': 'Cross'},
    {'value': 'x', 'label': 'X'},
    {'value': 'triangle-up', 'label': 'Triangle-up'},
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

marker_dict = {}
linestyle_dict = {}
gap_dict = {}
label_dict = {}
LINECOLOR_DICT = {}
linefill = {}
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

            # option to choose y value, move from right side to choose x value to underneath x value
            html.H6('Select Variables'),
            dcc.Dropdown(
                id = 'select-variables',
                options = [{'label': i, 'value': i} for i in ynames],
                value = [ynames[0]],
                multi = True
                ),

            daq.BooleanSwitch(
                id = 'use-group-by',
                on = False,
                label = 'Use Group By',
                labelPosition = 'top',
                color = toggle_switch_color
                ),

            html.H6('Group By'),
            html.Div([
                dcc.Dropdown(
                    id = 'select-groupby',
                    options = [{'label': i, 'value': i} for i in cat_features],
                    value = str(cat_features[0]),
                    disabled = False
                ),
            ], style = {'display': 'block'}),


            html.H6('Select Group'),
            dcc.RadioItems(
                id = 'select-group',
                #disabled = False
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
                options = [{'label': i, 'value': (i.replace(" ", "")).lower()} for i in linestyle_list],
                value = (str(linestyle_list[0]).replace(" ", "")).lower(),
                ),

            # Option to change lable style
            html.H6("Label Style"),
            dcc.Dropdown(
                id = 'alignment-labelstyle-dropdown',
                options = LABELSTYLE_DICT,
                value = 'lines'
            ),

            # Option to change marker style
            html.H6("Marker Style"),
            dcc.Dropdown(
                id = 'alignment-markers-dropdown',
                className = 'markers-controls-block-dropdown',
                options = MARKERS_DICT,
                value = 'circle'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        # All kinds of function buttons
        html.Div([
            html.H6('Function Buttons'),
            daq.BooleanSwitch(
                id = 'ALF',
                on = False,
                label = 'Line Fill',
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
                label = 'Y Zeroline',
                labelPosition = 'top',
                color = toggle_switch_color
                )
            ],
            style = {'width': '50%', 'display': 'inline-block', 'padding': '10px'}),

        # Slider to change line opacity
        html.H6("Opacity"),
        html.Div([
            dcc.Slider(
                id = 'opacity-slider',
                min = 0,
                max = 100,
                value = 85
            )
        ]),

        # Change distances between y ticks
        html.H6("Y ticks"),
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
    [Input('select-group', 'value'),]
)
def update_line(select_group):
    temp_str = LINECOLOR_DICT.get(select_group, dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb = dict(r = temp_str[0], g = temp_str[1], b = temp_str[2], a = temp_str[3]))
    return temp_str


@app.callback(
    [Output('select-group', 'options'),
    Output('select-groupby', 'disabled')],
    [Input('select-groupby', 'value'),
    Input('use-group-by', 'on'),
    Input('select-variables', 'value')]
)
def update_group(groupby, usegroup, selected):
    idx = 0
    if usegroup:
        groups = []
        for s in selected:
            for i in df[groupby].unique():
                LINECOLOR_DICT[s + ' : '+ i] = default_color[idx % 5]
                marker_dict[s + ' : '+ i] = MARKERS_DICT[idx % 5]['value']
                linestyle_dict[s + ' : '+ i] = linestyle_list[idx % 6].replace(' ', '').lower()
                gap_dict[s + ' : '+ i] = True
                label_dict[s + ' : '+ i] = LABELSTYLE_DICT[0]['value']
                linefill[s + ' : '+ i] = False
                idx += 1
                groups.append(s + ' : '+ i)
            return [{'label': i, 'value': i} for i in groups], False
    else:
        for i in selected:
            LINECOLOR_DICT[i] = default_color[idx % 5]
            marker_dict[i] = MARKERS_DICT[idx % 5]['value']
            linestyle_dict[i] = linestyle_list[idx % 6].replace(' ', '').lower()
            gap_dict[i] = True
            label_dict[i] = LABELSTYLE_DICT[0]['value']
            linefill[i] = False
            idx += 1
        return [{'label': i, 'value': i} for i in selected], True


# Main callback
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('select-variables', 'value'),
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
     Input('select-group', 'value'),
     Input('use-group-by', 'on')
     ])
def update_graph(select_variables, data_transform,
                 show_gridlines, show_zeroline_y,
                 alignment_markers_dropdown, alignment_labelstyle_dropdown,
                 show_gaps, ALF, OS, colorPicker, line_style,
                 groupby, y_dtick, select_group, use_group_by
                 ):
    if use_group_by == True:

        group_list = df[groupby].unique()
        type_y = None
        if data_transform:
            type_y = 'log'

        picker_line_color = 'rgba({}, {}, {}, {})'.format(
            colorPicker['rgb']['r'],
            colorPicker['rgb']['g'],
            colorPicker['rgb']['b'],
            colorPicker['rgb']['a'])

        traces_list = []
        for variable in select_variables:
            for selection in group_list:
                reference = variable + ' : '+ selection
                if reference == select_group:
                    LINECOLOR_DICT[reference] = picker_line_color
                    marker_dict[reference] = alignment_markers_dropdown
                    linestyle_dict[reference] = line_style
                    gap_dict[reference] = show_gaps
                    label_dict[reference] = alignment_labelstyle_dropdown
                    linefill[reference] = ALF
                traces_list.append(
                    go.Scatter(
                        x=datetime,
                        y=df[df[groupby] == selection][variable],
                        text=df[df[groupby] == selection][variable],
                        mode=label_dict[reference],
                        name=reference,
                        connectgaps = gap_dict[reference],
                        fill = "toself" if linefill[reference] else "none",
                        opacity = OS/100,
                        marker = dict(
                            size = 8,
                            opacity = 0.8,
                            symbol = marker_dict[reference]
                        ),
                        line = dict(color=LINECOLOR_DICT[reference], width=3, dash=linestyle_dict[reference])
                    )
                )    
        return {
            'data': traces_list,
            'layout': go.Layout(
                xaxis={
                    'title' : 'Time',
                    'showgrid': show_gridlines,
                    'rangeslider': {'visible': True}, 'type': 'date'
                },
                yaxis={
                    'title' : ', '.join(select_variables),
                    'type' : type_y,
                    'showgrid': show_gridlines,
                    'zeroline': show_zeroline_y,
                    'dtick': y_dtick
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                title= "Time-Series-Edit Me Last",
                hovermode='closest'
            )
        }

    else:
        type_y = None
        if data_transform:
            type_y = 'log'

        yaxis_list = ynames

        picker_line_color = 'rgba({}, {}, {}, {})'.format(
            colorPicker['rgb']['r'],
            colorPicker['rgb']['g'],
            colorPicker['rgb']['b'],
            colorPicker['rgb']['a'])

        Fill = "none"
        if ALF:
            Fill = "toself"

        traces_list = []
        for variable in select_variables:
            if select_group is not None:
                if variable == select_group:
                    LINECOLOR_DICT[variable] = picker_line_color
                    marker_dict[variable] = alignment_markers_dropdown
                    linestyle_dict[variable] = line_style
                    gap_dict[variable] = show_gaps
                    label_dict[variable] = alignment_labelstyle_dropdown
                    linefill[variable] = ALF
            traces_list.append(
                go.Scatter(
                    x=datetime,
                    y=df[variable],
                    text=df[variable],
                    mode=label_dict[variable],
                    name=str(variable).replace('[', '').replace(']', '').replace("\'", ""),
                    connectgaps = gap_dict[variable],
                    fill = "toself" if linefill[variable] else "none",
                    opacity = OS/100,
                    marker = dict(
                        size = 8,
                        opacity = 0.8,
                        symbol = marker_dict[variable]
                    ),
                    line = dict(color=LINECOLOR_DICT[variable], width=3, dash=linestyle_dict[variable])
                    )
                )

        return {
            'data': traces_list,
            'layout': go.Layout(
                xaxis={
                    'title' : 'Time',
                    'showgrid': show_gridlines,
                    'rangeslider': {'visible': True}, 
                    'type': 'date'
                },
                yaxis={
                    'title' : ', '.join(select_variables),
                    'type' : type_y,
                    'showgrid': show_gridlines,
                    'zeroline': show_zeroline_y,
                    'dtick': y_dtick
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                title= "Time-Series-Edit Me Last",
                hovermode='closest'
            )
        }   


if __name__ == '__main__':
    app.run_server(debug=True)
