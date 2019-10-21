# IMPORT LIBRARIES
import plotly.graph_objs as go
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import colorlover as cl

# INITIAL VARIABLES
button_font_size='1.2em'
cardbody_font_size='1em'
cardheader_color='info'
cardbody_color='info'
main_panel_margin={'margin': '10px 0px'}
left_panel_margin={'width': '25%'}
right_panel_margin={'class': 'col-md-8', 'display':'block-inline'}
toggle_switch_color='#91c153'
line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']
marker_symbols = ['Circle', 'Square', 'Diamond', 'Cross', 'X', 'Triangle-Up', 'Pentagon', 'Hexagon', 'Star']
default_alpha = 0.65
default_symbol_alpha = 1
box_color_saved = {}
percentile_color_saved = cl.to_rgb(cl.scales[str('5')]['qual']['Dark2'])
num_of_color=9
default_color = cl.to_rgb(cl.scales[str(num_of_color)]['qual']['Set1'])
dtick_value = None

# Initialising selected marker symbol
selected_marker_symbols = ['diamond', 'cross', 'triangle-up', 'star', 'x']

# generate default colors list
col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
    col_idx += 1

col_idx = 0
for i in percentile_color_saved:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_symbol_alpha)
    percentile_color_saved[col_idx] = i
    col_idx += 1

# FUNCTIONS GOES HERE
# Function: Reading file
# Input: file name
# Output: data frame
def read_file(filename):
    try:
        if 'csv' in filename:
            dff = pd.read_csv(filename)
        elif ('xls' or 'xlsx') in filename:
            dff = pd.read_excel(filename)
    except Exception as e:
        print(e)
        return u'There was an error opening {}'.format(filename)
    return dff

# Function: Render drop down list
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown(id, options):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': i} for i in options],
        className='card h-100' )

# Function: Render drop down list without any options
# Input: id
# Output: dcc.Dropdown
def render_dropdown_blank(id):
    return dcc.Dropdown(id=id)

# Function: Render drop down list with selected value
# Input: id, [options], value
# Output: dcc.Dropdown
def render_dropdown_valued(id, options, value):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': i} for i in options], value=value,
        className='card h-100' )

# Function: Render drop down list with label formatting (remove space between words and turn to lower case)
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown_format(id, options):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': (i.replace(" ", "")).lower()} for i in options],
        className='card h-100' )

# Function: Render radio items
# Input: id, [options]
# Output: dcc.RadioItems
def render_radio(id, options):
    return dcc.RadioItems(id=id, options=[{'label': i, 'value': i} for i in options],
        value=str(options[0]), labelStyle={'display': 'block'} )

# Function: Render radio items for data points and outlies
# Input: id
# Output: dcc.RadioItems
def render_radio_outliers(id):
    return dcc.RadioItems(
        id=id,
        options=[
            {'label': 'Default', 'value': 'outliers'},
            {'label': 'Only Wiskers', 'value': 'False'},
            {'label': 'Suspected Outliers', 'value': 'suspectedoutliers'},
            {'label': 'All Points', 'value': 'all'},
        ],
        value='outliers',
        labelStyle={'display': 'block'} )

# Function: Render radio items contain id only
# Input: id
# Output: dcc.RadioItems
def render_radio_blank(id):
    return dcc.RadioItems(id=id, labelStyle={'display': 'block'} )

# Function: Render radio items with label formatting (remove space between words and turn to lower case)
# Input: id, [options]
# Output: dcc.RadioItems
def render_radio_format(id, options):
    return dcc.RadioItems(
        id=id,
        options=[{'label': i, 'value': (i.replace(" ", "")).lower()} for i in options],
        value=(str(options[0]).replace(" ", "")).lower(),
        labelStyle={'display': 'block'}, )

# Function: Render text input
# Input: id, placeholder
# Output: dcc.Input
def render_input(id, placeholder):
    return dcc.Input(id=id, type='text', placeholder=placeholder, style={'width': '100%'})

# Function: Render number input
# Input: id, placeholder
# Output: dcc.Input
def render_input_number(id, placeholder):
    return dcc.Input(id=id, type='number', min=0, placeholder=placeholder, style={'width': '100%'})

# Function: Render text input with delay feature, will callback after enter key pressed or input area loss its focus
# Input: id, placeholder
# Output: dcc.RadioItems
def render_input_delay(id, placeholder):
    return dcc.Input(id=id, type='text', placeholder=placeholder, debounce=True, style={'width': '100%'})

# Function: Render toggle switch
# Input: id, [labels], value
# Output: daq.ToggleSwitch
def render_toggleswitch(id, labels, value):
    return daq.ToggleSwitch(id=id, label=labels, value=value, color=toggle_switch_color, )

# Function: Render boolean switch
# Input: id, label, on
# Output: daq.BooleanSwitch
def render_booleanswitch(id, label, on):
    return daq.BooleanSwitch(id=id, label=label, on=on, labelPosition='top', color=toggle_switch_color, )

# Function: Render boolean switch without label
# Input: id, on
# Output: daq.BooleanSwitch
def render_booleanswitch_nolab(id, on):
    return daq.BooleanSwitch(id=id, on=on, color=toggle_switch_color, )

# Function: Render slider
# Input: id, min, max, value, step, label
# Output: daq.Slider
def render_slider(id, min, max, value, step, marks):
    mymark={}
    for i in marks:
        mymark[i]=str(i)
    return daq.Slider(id=id, min=min, max=max, value=value, step=step, marks=mymark )

# Function: Render Range slider
# Input: id, min, max, [value], step, {marks}
# Output: dcc.RangeSlider
def render_range_slider(id, min, max, value, step, marks):
    return dcc.RangeSlider(id=id, min=min, max=max, value=value, step=step, marks=marks )

# Function: Render color picker
# Input: id, min, max, value, step, label
# Output: daq.ColorPicker
def render_colorpicker(id, color, r, g, b, a):
    value=dict(rgb=dict(r=r, g=g, b=b, a=a))
    return daq.ColorPicker(id=id, value=value)

# Function: Render numeric Input
# Input: id, min, max, value
# Output: daq.NumericInput
def render_numinput(id, min, max, value):
    return daq.NumericInput(id=id, min=min, max=max, value=value )

# MAIN APP HERE
# Loading Data
file_name = 'data3.xlsx'
df = read_file(file_name)

# Loading Numeric Data from Dataframe
# Please be aware with categoric data stored in numeric data
# example: gender variable coded by 1 and 2, this feature will
#          fall into numeric data instead of categoric.
#          proposed solution: modify file by recode to alphabetic
#          (ex: recode 1 = m and 2 = f)
features = df.select_dtypes(include='number').columns.values

# Loading non-Numeric Data from Dataframe
cat_features = df.select_dtypes(exclude=['number', 'datetime', 'datetime64']).columns.values

# Loading datetime from Dataframe
datetime_feature = df.select_dtypes(include=['datetime', 'datetime64']).columns.values
if datetime_feature.shape[0]==0:
    df_no_time=True
else:
    print('have a time')
    df_no_time=False
    dt_min=df[datetime_feature[0]].min()
    dt_max=df[datetime_feature[0]].max()
    dt_range=((dt_max.year + 1) - dt_min.year)*12

    # Generate date time slider marks
    dt_slider_marks = {}
    for i in range(0, dt_range+1):
        if i % 12 == 0:
            dt_slider_marks[i]=str(dt_min.year + (i//12))

## MAIN APP HERE
app = dash.Dash(__name__)
app.layout=html.Div(className='row', children=[
    html.Div(children=[
        html.Div(className='container', children=[
            html.Div(className='accordion', children=[
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Select Data", id='group-1-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Variable')),
                                dbc.CardBody(children=render_dropdown_valued('select-variable', features, features[0]))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Group by')),
                                dbc.CardBody(children=render_dropdown_valued('select-groupby', cat_features, cat_features[0]))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            )
                        ]),
                        id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Plot Setting", id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Orientation')),
                                dbc.CardBody(children=render_toggleswitch('graph-alignment', ['Vertical', 'Horizontal'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Legend')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-legend', True))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Grid Lines')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-gridlines', True))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Zero Line')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-zeroline-x', True))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Zero Line')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-zeroline-y', True))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Grid Width')),
                                dbc.CardBody(children=render_numinput('grid-width', 1, 5, 1))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Tick Step')),
                                dbc.CardBody(children=render_input_number('delta-tick', 'Tick Step'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-3'
                    ),
                ], color='info', outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Statistic Information", id='group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Data Transformation')),
                                dbc.CardBody(children=render_toggleswitch('data-transform', ['Linear', 'Logarithmic'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Boxplot type')),
                                dbc.CardBody(children=render_radio_outliers('select-outliers'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Frequency')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-ndata', True))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Mean')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-mean', False))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Std. Dev.')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-sd', False))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Summary Stats')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-stats', False))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-4'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Percentiles", id='group-7-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Show Percentiles')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-percentiles', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Percentile')),
                                dbc.CardBody(children=render_dropdown('select-percentile', ['5%', '10%', '90%', '95%']))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Marker Symbol')),
                                dbc.CardBody(children=render_dropdown_format('marker-symbol', marker_symbols))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Symbol Size'), className='card w-100'),
                                dbc.CardBody(children=render_numinput('symbol-size', 1, 15, 8))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Color')),
                                dbc.CardBody(children=render_colorpicker('select-percentile-color', 'white', 100, 200, 255, 0.65))
                            ],
                            ),
                        ]),
                        id='collapse-7'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Threshold Setting", id='group-5-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Threshold')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-treshold', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Value')),
                                dbc.CardBody(children=render_input('treshold-value', 'Threshold Value'))
                            ], className='col-md-6'
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Line Size')),
                                dbc.CardBody(children=render_numinput('treshold-line-size', 1, 10, 2))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Line Style')),
                                dbc.CardBody(children=render_dropdown_format('treshold-style', line_style))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Line Color')),
                                dbc.CardBody(children=render_colorpicker('treshold-line-color', 'white', 0, 0, 255, 1))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Box Color", id='group-6-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Fill')),
                                dbc.CardBody(children=render_toggleswitch('box-color-fill', ['Transparent', 'Colored'], True))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Select Box'), className='card w-100'),
                                dbc.CardBody(children=render_dropdown_blank('select-box'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Color')),
                                dbc.CardBody(children=render_colorpicker('box-color', 'white', 0, 0, 255, 0.65))
                            ],
                            ),
                        ]),
                        id='collapse-6'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Graph Size", id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Height')),
                                dbc.CardBody(children=render_slider('graph-height', 600, 1200, 600, 50, [600, 700, 800, 900, 1000, 1100, 1200]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Width')),
                                dbc.CardBody(children=render_slider('graph-width', 800, 1400, 800, 50, [800, 900, 1000, 1100, 1200, 1300, 1400]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                        ]),
                        id='collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='box-plot',
                    style={'width' : '90%', 'padding-left' : '3%'},
                    config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'titleText': True}},
            ),
        ],
        ),
        dbc.Row(children=[
            html.Div(id='time-msg-card', children=[
                dbc.Card([
                    dbc.CardHeader(html.H5('Select Time Range')),
                    dbc.CardBody(children=render_range_slider('time-range-slider', 0, 0 if df_no_time else dt_range, [0, 0 if df_no_time else dt_range], 1, {} if df_no_time else dt_slider_marks), style={'padding':'2% 2% 4% 2%'}),
                    dbc.CardFooter(id='time-range-msg'),
                ], style={'width': '100%', 'font-size': cardbody_font_size, 'display': 'none' if df_no_time else 'block'}, color=cardbody_color, outline=True,
                ),
            ], style={'width': '90%', 'margin': '2%'}
            ),
        ]),
    ], className='col-md-9'
    ),
], style=main_panel_margin)

# CALLBACK GOES HERE
# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,8)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,8)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,8)]
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, n7, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False, False, False, False, False
    elif button_id ==  'group-2-toggle' and n2:
        return False, not is_open2, False, False, False, False, False
    elif button_id ==  'group-3-toggle' and n3:
        return False, False, not is_open3, False, False, False, False
    elif button_id ==  'group-4-toggle' and n4:
        return False, False, False, not is_open4, False, False, False
    elif button_id ==  'group-5-toggle' and n5:
        return False, False, False, False, not is_open5, False, False
    elif button_id ==  'group-6-toggle' and n6:
        return False, False, False, False, False, not is_open6, False
    elif button_id ==  'group-7-toggle' and n7:
        return False, False, False, False, False, False, not is_open7
    return False, False, False, False, False, False, False

# Update time range message
@app.callback(
    Output('time-range-msg', 'children'),
    [Input('time-range-slider', 'value'), ]
)
def update_time_range_msg(dt_range_slider):
    if not df_no_time:
        from_year=dt_min.year+(dt_range_slider[0]//12)
        from_month=dt_min.month+(dt_range_slider[0]%12)
        to_year=dt_min.year+(dt_range_slider[1]//12)
        to_month=dt_range_slider[1]%12+1
        return html.H5('Time range from {}/{} to {}/{}'.format(from_month, from_year, to_month, to_year))
    else:
        return None

# Update marker symbol when percentile selected
@app.callback(
    Output('marker-symbol', 'value'),
    [Input('select-percentile', 'value')]
)
def update_marker_symbol(percentile):
    i = 0
    if percentile == '5%':
        i = 0
    elif percentile == '10%':
        i = 1
    elif percentile == '90%':
        i = 2
    else:
        i = 3
    return selected_marker_symbols[i]

# Update Percentile Symbol Color Picker
@app.callback(
    Output('select-percentile-color', 'value'),
    [Input('select-percentile', 'value')]
)
def update_box_color_selector(percentile):
    i = 0
    if percentile == '5%':
        i = 0
    elif percentile == '10%':
        i = 1
    elif percentile == '90%':
        i = 2
    else:
        i = 3

    temp_str = percentile_color_saved[i]
    start_idx = temp_str.find('(')
    temp_str = temp_str[start_idx+1:len(temp_str)-1]
    temp_str = temp_str.split(",")
    temp_str = dict(rgb=dict(r=temp_str[0], g=temp_str[1], b=temp_str[2], a=temp_str[3]))
    return temp_str


# Turn Y Tick Disabled when in Logarithmic and Enabled when in Linear
# Turn Y Tick Value to None when in Logarithmic end recall previous value when turn back to Linear
@app.callback(
    [Output('delta-tick', 'disabled'),
     Output('delta-tick', 'value')],
    [Input('data-transform', 'value')]
)
def update_delta_tick_disabled(is_log):
    return is_log, None if is_log else dtick_value

# Box Color Selector Callback
@app.callback(
    Output('box-color', 'value'),
    [Input('select-box', 'value')]
)
def update_box_color_selector(box):
    temp_str = box_color_saved.get(box, dict(rgb=dict(r=222, g=110, b=75, a=default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb=dict(r=temp_str[0], g=temp_str[1], b=temp_str[2], a=temp_str[3]))
    return temp_str

# Box Selector Callback
@app.callback(
    Output('select-box', 'options'),
    [Input('select-groupby', 'value'), ]
)
def update_select_box(groupby):
    idx = 0
    for i in df[groupby].unique():
        box_color_saved[i] = default_color[idx % num_of_color]
        idx += 1
    return [{'label': i, 'value': i} for i in df[groupby].unique()]

# Threshold Line Callback
@app.callback(
    Output('treshold-value', 'value'),
    [Input('show-treshold', 'on'),
     Input('select-variable', 'value'),
     ]
)
def update_treshold_value(
    is_tresholdshow, variable
):
    return np.around(np.mean(df[variable]), 0) if is_tresholdshow else ' '

# Statistics Show Hide Callback
@app.callback(
    Output('show-stats', 'on'),
    [Input('select-outliers', 'value'), ]
)
def update_showstat(outliersshow):
    return False if outliersshow == 'all' else None

# Figure Callback
@app.callback(
    Output('box-plot', 'figure'),
    [
        Input('select-variable', 'value'), Input('select-groupby', 'value'),
        Input('show-gridlines', 'on'),
        Input('show-zeroline-x', 'on'), Input('show-zeroline-y', 'on'),
        Input('show-legend', 'on'), Input('show-percentiles', 'on'),
        Input('graph-alignment', 'value'), Input('data-transform', 'value'),
        Input('select-outliers', 'value'), Input('show-ndata', 'on'),
        Input('show-percentiles', 'on'), Input('show-mean', 'on'),
        Input('show-sd', 'on'), Input('show-treshold', 'on'),
        Input('treshold-value', 'value'), Input('treshold-style', 'value'),
        Input('treshold-line-color', 'value'),
        Input('treshold-line-size', 'value'),
        Input('show-stats', 'on'), Input('graph-height', 'value'),
        Input('graph-width', 'value'),
        Input('select-box', 'value'), Input('box-color', 'value'),
        Input('grid-width', 'value'), Input('delta-tick', 'value'),
        Input('box-color-fill', 'value'),
        Input('select-percentile', 'value'), Input('marker-symbol', 'value'),
        Input('select-percentile-color', 'value'), Input('symbol-size', 'value'),
        Input('time-range-slider', 'value'),
    ]
)
def update_figure(
    variable, groupby,
    gridshow, xzeroline, yzeroline, legendshow,
    datapointsshow, is_vertical, is_log, outliersshow, is_ndatashow,
    is_percentileshow, is_meanshow, is_sdshow, is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, is_statshow, graph_height,
    graph_width, selected_box, box_color, grid_width, dtick, is_color_filled,
    select_percentile, marker_symbol, select_percentile_color, symbol_size, dt_range_slider
):
    # Set timestamps from time Range
    if not df_no_time:
        from_year=dt_min.year+(dt_range_slider[0]//12)
        from_month=dt_min.month+(dt_range_slider[0]%12)
        to_year=dt_min.year+(dt_range_slider[1]//12)
        to_month=dt_range_slider[1]%12+1
        bottom_time=pd.Timestamp(year=from_year, month=from_month, day=1, hour=0, second=0)
        upper_time=pd.Timestamp(year=to_year, month=to_month, day=30, hour=23, second=59)
        print('from: {}'.format(bottom_time))
        print('until: {}'.format(upper_time))
        mydf = df[(df[datetime_feature[0]]>=bottom_time) & (df[datetime_feature[0]]<=upper_time)]
        if mydf.shape[0] == 0:
            mydf_is_empty=True
        else:
            mydf_is_empty=False
    # Update dtick_value
    if dtick != None:
        dtick_value = dtick

    # Title and axises label modificator
    xaxis_title = groupby
    yaxis_title = variable
    main_title = str(variable + " VS " + groupby)

    # Outliers Selector
    showpoints = ""
    if (outliersshow == 'False'):
        showpoints = False
    elif (outliersshow == 'suspectedoutliers'):
        showpoints = outliersshow
    else:
        showpoints = outliersshow

    # Initialising data list
    group_list = df[groupby].unique()
    data_list = []
    n_data = []
    data_mean = []
    data_median = []
    data_max = []
    data_min = []
    percentile_5 = []
    percentile_10 = []
    percentile_90 = []
    percentile_95 = []
    percentile_25 = []
    percentile_75 = []
    annots_ndata = []
    annots_mean = []
    annots_median = []
    annots_max = []
    annots_min = []
    annots_p5 = []
    annots_p10 = []
    annots_p25 = []
    annots_p75 = []
    annots_p90 = []
    annots_p95 = []
    annots_idx = 0

    # Computing N Data
    max_n = df[variable].max()
    max_n = 1.05*np.log10(max_n) if is_log else 1.05*max_n

    picker_percentile_color = 'rgba({}, {}, {}, {})'.format(
        select_percentile_color['rgb']['r'],
        select_percentile_color['rgb']['g'],
        select_percentile_color['rgb']['b'],
        select_percentile_color['rgb']['a'],)

    picker_box_color = 'rgba({}, {}, {}, {})'.format(
        box_color['rgb']['r'],
        box_color['rgb']['g'],
        box_color['rgb']['b'],
        box_color['rgb']['a'],)

    color_idx = 0
    # Generate boxplot
    for i in group_list:
        if selected_box is not None:
            if i == selected_box:
                box_color_saved[i] = picker_box_color
        color_idx += 1

        if (not is_vertical):
            data_list.append(
                go.Box(
                    y=df[df[groupby] == i][variable],
                    name=i,
                    boxpoints=showpoints,
                    boxmean='sd' if is_sdshow else None,
                    marker_color=box_color_saved[i],
                    fillcolor=box_color_saved[i] if is_color_filled else 'rgba(255,255,255,0)',
                )
            )
        else:
            data_list.append(
                go.Box(
                    x=df[df[groupby] == i][variable],
                    name=i,
                    orientation='h',
                    boxpoints=showpoints,
                    boxmean='sd' if is_sdshow else None,
                    marker_color=box_color_saved[i],
                    fillcolor=box_color_saved[i] if is_color_filled else 'rgba(255,255,255,0)',
                )
            )

        # Counting percentiles
        percentile_5.append(np.around(np.percentile((df[df[groupby] == i][variable]), 5), 2))
        percentile_10.append(np.around(np.percentile((df[df[groupby] == i][variable]), 10), 2))
        percentile_90.append(np.around(np.percentile((df[df[groupby] == i][variable]), 90), 2))
        percentile_95.append(np.around(np.percentile((df[df[groupby] == i][variable]), 95), 2))
        percentile_25.append(np.around(np.percentile((df[df[groupby] == i][variable]), 25), 2))
        percentile_75.append(np.around(np.percentile((df[df[groupby] == i][variable]), 75), 2))
        data_max.append(np.around(np.max((df[df[groupby] == i][variable])), 2))
        data_min.append(np.around(np.min((df[df[groupby] == i][variable])), 2))

        # Calculating mean and median
        data_mean.append(np.around(np.mean((df[df[groupby] == i][variable])), 2))
        data_median.append(np.around(np.median((df[df[groupby] == i][variable])), 2))

        # Counting number of data for each category
        df_shape = df[df[groupby] == i][variable].shape
        n_data.append(df_shape[0])

        # Generating annotations of n of data
        annots_ndata.append(go.layout.Annotation(
            x=max_n if is_vertical else annots_idx,
            y=annots_idx if is_vertical else max_n,
            xref='x',
            yref='y',
            text='N = {}'.format(n_data[annots_idx]),
            showarrow=False,
            ax=0 if is_vertical else annots_idx,
            ay=annots_idx if is_vertical else 0,
            )
        )

        # Generating annotations of mean
        annots_mean.append(go.layout.Annotation(
            x=(np.log10(data_mean[annots_idx]) if is_log else data_mean[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(data_mean[annots_idx]) if is_log else data_mean[annots_idx]),
            xref='x',
            yref='y',
            text='Mean: {}'.format(data_mean[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of mean
        annots_median.append(go.layout.Annotation(
            x=(np.log10(data_median[annots_idx]) if is_log else data_median[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(data_median[annots_idx]) if is_log else data_median[annots_idx]),
            xref='x',
            yref='y',
            text='Med: {}'.format(data_median[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 5
        annots_p5.append(go.layout.Annotation(
            x=(np.log10(percentile_5[annots_idx]) if is_log else percentile_5[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_5[annots_idx]) if is_log else percentile_5[annots_idx]),
            xref='x',
            yref='y',
            text='P5: {}'.format(percentile_5[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 10
        annots_p10.append(go.layout.Annotation(
            x=(np.log10(percentile_10[annots_idx]) if is_log else percentile_10[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_10[annots_idx]) if is_log else percentile_10[annots_idx]),
            xref='x',
            yref='y',
            text='P10: {}'.format(percentile_10[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 25
        annots_p25.append(go.layout.Annotation(
            x=(np.log10(percentile_25[annots_idx]) if is_log else percentile_25[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_25[annots_idx]) if is_log else percentile_25[annots_idx]),
            xref='x',
            yref='y',
            text='Q1: {}'.format(np.around(percentile_25[annots_idx], 2)),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 75
        annots_p75.append(go.layout.Annotation(
            x=(np.log10(percentile_75[annots_idx]) if is_log else percentile_75[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_75[annots_idx]) if is_log else percentile_75[annots_idx]),
            xref='x',
            yref='y',
            text='Q3: {}'.format(np.around(percentile_75[annots_idx], 2)),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 90
        annots_p90.append(go.layout.Annotation(
            x=(np.log10(percentile_90[annots_idx]) if is_log else percentile_90[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_90[annots_idx]) if is_log else percentile_90[annots_idx]),
            xref='x',
            yref='y',
            text='P90: {}'.format(percentile_90[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of percentile 95
        annots_p95.append(go.layout.Annotation(
            x=(np.log10(percentile_95[annots_idx]) if is_log else percentile_95[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(percentile_95[annots_idx]) if is_log else percentile_95[annots_idx]),
            xref='x',
            yref='y',
            text='P95: {}'.format(percentile_95[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        # Generating annotations of max
        annots_max.append(go.layout.Annotation(
            x=(np.log10(data_max[annots_idx]) if is_log else data_max[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(data_max[annots_idx]) if is_log else data_max[annots_idx]),
            xref='x',
            yref='y',
            text='Max: {}'.format(data_max[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        annots_min.append(go.layout.Annotation(
            x=(np.log10(data_min[annots_idx]) if is_log else data_min[annots_idx]) if is_vertical else annots_idx,
            y=annots_idx if is_vertical else (np.log10(data_min[annots_idx]) if is_log else data_min[annots_idx]),
            xref='x',
            yref='y',
            text='Min: {}'.format(data_min[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        annots_idx = annots_idx + 1

    if (not is_ndatashow):
        annots_ndata = []

    if (not is_statshow):
        annots_mean = []
        annots_median = []
        annots_p5 = []
        annots_p10 = []
        annots_p25 = []
        annots_p90 = []
        annots_p75 = []
        annots_p95 = []
        annots_max = []
        annots_min = []

    annots_ndata = annots_ndata + annots_mean + annots_median + annots_p5 + annots_p10 + annots_p25 + annots_p75 + annots_p90 + annots_p95 + annots_max + annots_min

    # Convert selected percentile values
    ip = 0
    if select_percentile == '5%':
        ip = 0
    elif select_percentile == '10%':
        ip = 1
    elif select_percentile == '90%':
        ip = 2
    else:
        ip = 3

    selected_marker_symbols[ip] = marker_symbol
    percentile_color_saved[ip] = picker_percentile_color

    # Change Orientation
    type_x = None
    type_y = None
    if (is_vertical):
        xaxis_title, yaxis_title = yaxis_title, xaxis_title
        type_x = 'log' if is_log else None
        if(is_meanshow):
            data_list.append(go.Scatter(x=data_mean, y=group_list, mode='markers', name='Mean', marker=dict(symbol=selected_marker_symbols[4], size=symbol_size)))
        # Generating Percentiles to Figure
        if (is_percentileshow):
            data_list.append(go.Scatter(y=group_list, x=percentile_5, mode='markers', name='5%', marker_color=percentile_color_saved[0], marker=dict(symbol=selected_marker_symbols[0], size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_10, mode='markers', name='10%', marker_color=percentile_color_saved[1], marker=dict(symbol=selected_marker_symbols[1], size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_90, mode='markers', name='90%', marker_color=percentile_color_saved[2], marker=dict(symbol=selected_marker_symbols[2], size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_95, mode='markers', name='95%', marker_color=percentile_color_saved[3], marker=dict(symbol=selected_marker_symbols[3], size=symbol_size)))
    else:
        type_y = 'log' if is_log else None
        if(is_meanshow):
            data_list.append(go.Scatter(x=group_list, y=data_mean, mode='markers', name='Mean', marker=dict(symbol=selected_marker_symbols[4], size=symbol_size)))
        # Generating Percentiles to Figure
        if (is_percentileshow):
            data_list.append(go.Scatter(x=group_list, y=percentile_5, mode='markers', name='5%', marker_color=percentile_color_saved[0], marker=dict(symbol=selected_marker_symbols[0], size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_10, mode='markers', name='10%', marker_color=percentile_color_saved[1], marker=dict(symbol=selected_marker_symbols[1], size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_90, mode='markers', name='90%', marker_color=percentile_color_saved[2], marker=dict(symbol=selected_marker_symbols[2], size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_95, mode='markers', name='95%', marker_color=percentile_color_saved[3], marker=dict(symbol=selected_marker_symbols[3], size=symbol_size)))

    treshold_shape = []

    if is_tresholdshow:
        treshold_shape.append(dict(line=dict(
                                # color="rgba(68, 68, 68, 0.5)",
                                color='rgba({}, {}, {}, {})'.format(
                                    treshold_color['rgb']['r'],
                                    treshold_color['rgb']['g'],
                                    treshold_color['rgb']['b'],
                                    treshold_color['rgb']['a'], ),
                                width=treshold_size, dash=treshold_style,
                                ),
            type='line',
            x0=-0.5 if not is_vertical else treshold_value,
            x1=len(group_list)-0.5 if not is_vertical else treshold_value,
            y0=treshold_value if not is_vertical else -0.5,
            y1=treshold_value if not is_vertical else len(group_list)-0.5,
        ))

    # Returning figure
    return{
        'data': data_list,
        'layout': go.Layout(
            xaxis=go.layout.XAxis(
                title=xaxis_title,
                showgrid=gridshow,
                zeroline=xzeroline,
                type=type_x,
                gridwidth=grid_width,
                gridcolor='lightgrey',
                dtick=dtick if is_vertical else None,
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=gridshow,
                zeroline=yzeroline,
                type=type_y,
                gridwidth=grid_width,
                gridcolor='lightgrey',
                dtick=None if is_vertical else dtick,
            ),
            title=main_title,
            showlegend=legendshow,
            height=graph_height,
            width=graph_width,
            annotations=annots_ndata,
            shapes=treshold_shape,
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
