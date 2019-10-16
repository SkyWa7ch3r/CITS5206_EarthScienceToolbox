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
button_font_size='1.5em'
cardbody_font_size='1.5em'
cardheader_color='info'
cardbody_color='info'
main_panel_margin={'margin': '10px 0px'}
left_panel_margin={'width': '25%'}
right_panel_margin={'class': 'col-md-8', 'display':'block-inline'}
toggle_switch_color='#91c153'
line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']
default_alpha = 0.65
box_color_saved = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
dtick_value = None

# generate default colors list
col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
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

# Function: Render color picker
# Input: id, min, max, value, step, label
# Output: daq.ColorPicker
def render_colorpicker(id, color, r, g, b, a):
    value=dict(rgb=dict(r=r, g=g, b=b, a=a))
    return daq.ColorPicker(id=id, style={'background-color': color}, value=value, size=160 )

# Function: Render numeric Input
# Input: id, min, max, value
# Output: daq.NumericInput
def render_numinput(id, min, max, value):
    return daq.NumericInput(id=id, min=min, max=max, value=value )

# Function: Get Quantile
# Input: df
# Output: Q1
def get_quantile(df):
    df=df.sort_values()
    n = len(df)
    n_q1=n//2
    q1_idx=(n_q1//2)
    q3_idx=n-q1_idx
    df_keys=df.keys()
    if n_q1%2==0:
        q1=(df[df_keys[q1_idx]]+df[df_keys[q1_idx-1]])/2
        q3=(df[df_keys[q3_idx]]+df[df_keys[q3_idx-1]])/2
    else:
        q1=df[df_keys[(q1_idx)]]
        q3=df[df_keys[(q3_idx-1)]]
    #if n%2==0:
    #print ('Data: \n{}'.format(df))
    #print ('Data: \n{}'.format(df_keys))
    #print ('Num of data: {}'.format(n))
    #print ('Q1: {}'.format(q1))
    #print ('Q3: {}'.format(q3))
    return q1, q3



# MAIN APP HERE
# Loading Data
file_name = 'data2.xlsx'
df = read_file(file_name)

# Loading Numeric Data from Dataframe
# Please be aware with categoric data stored in numeric data
# example: gender variable coded by 1 and 2, this feature will
#          fall into numeric data instead of categoric.
#          proposed solution: modify file by recode to alphabetic
#          (ex: recode 1 = m and 2 = f)
features = df.select_dtypes(include='number').columns.values

# Loading non-Numeric Data from Dataframe
cat_features = df.select_dtypes(exclude='number').columns.values


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
                                dbc.CardHeader(html.H2('Variable')),
                                dbc.CardBody(children=render_radio('select-variable', features))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Group by')),
                                dbc.CardBody(children=render_radio('select-groupby', cat_features))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            )
                        ]),
                        id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Change Title and Axis Labels", id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Main Title')),
                                dbc.CardBody(children=render_input('main-title', 'Main Title'))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H2('X Axis Label')),
                                dbc.CardBody(children=render_input('xaxis-title', 'X Axis Label'))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Y Axis Label')),
                                dbc.CardBody(children=render_input('yaxis-title', 'Y Axis Label'))
                            ]),
                        ]),
                        id='collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Graph Setting", id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Graph Orientation')),
                                dbc.CardBody(children=render_toggleswitch('graph-alignment', ['Vertical', 'Horizontal'], False))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Legend')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-legend', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Grid Lines')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-gridlines', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('X Zero Line')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-zeroline-x', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Y Zero Line')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-zeroline-y', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Graph Height')),
                                dbc.CardBody(children=render_slider('graph-height', 600, 1200, 600, 50, [600, 700, 800, 900, 1000, 1100, 1200]))
                            ], style={'width': '100%', 'padding': '20px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Graph Width')),
                                dbc.CardBody(children=render_slider('graph-width', 800, 1400, 800, 50, [800, 900, 1000, 1100, 1200, 1300, 1400]))
                            ], style={'width': '100%', 'padding': '20px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Grid Width')),
                                dbc.CardBody(children=render_numinput('grid-width', 1, 5, 1))
                            ], className='col-md-6'
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Tick Step')),
                                dbc.CardBody(children=render_input_number('delta-tick', 'Tick Step'))
                            ], className='col-md-6'
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
                                dbc.CardHeader(html.H2('Data Transformation')),
                                dbc.CardBody(children=render_toggleswitch('data-transform', ['Linear', 'Logarithmic'], False))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Group by')),
                                dbc.CardBody(children=render_radio_outliers('select-outliers'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Frequency')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-ndata', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Percentiles')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-percentiles', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Mean')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-mean', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Std. Dev.')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-sd', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Summary Stats')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-stats', False))
                            ], className='col-md-6',
                            ),
                        ]),
                        id='collapse-4'
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
                                dbc.CardHeader(html.H2('Threshold')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-treshold', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Value')),
                                dbc.CardBody(children=render_input('treshold-value', 'Threshold Value'))
                            ], className='col-md-6'
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Line Style')),
                                dbc.CardBody(children=render_radio_format('treshold-style', line_style))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Line Size')),
                                dbc.CardBody(children=render_numinput('treshold-line-size', 1, 10, 2))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Line Color')),
                                dbc.CardBody(children=render_colorpicker('treshold-line-color', 'white', 0, 0, 255, 1))
                            ],
                            ),
                        ]),
                        id='collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Color Setting", id='group-6-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Select Box')),
                                dbc.CardBody(children=render_radio_blank('select-box'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Box Color')),
                                dbc.CardBody(children=render_colorpicker('box-color', 'white', 0, 0, 255, 0.65))
                            ],
                            ),
                        ]),
                        id='collapse-6'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} )
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='box-plot'),
        ])
    ], className='col-md-9'
    ),
], style=main_panel_margin)

# CALLBACK GOES HERE
# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,7)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,7)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,7)]
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False, False, False, False
    elif button_id ==  'group-2-toggle' and n2:
        return False, not is_open2, False, False, False, False
    elif button_id ==  'group-3-toggle' and n3:
        return False, False, not is_open3, False, False, False
    elif button_id ==  'group-4-toggle' and n4:
        return False, False, False, not is_open4, False, False
    elif button_id ==  'group-5-toggle' and n5:
        return False, False, False, False, not is_open5, False
    elif button_id ==  'group-6-toggle' and n6:
        return False, False, False, False, False, not is_open6
    return False, False, False, False, False, False

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
        box_color_saved[i] = default_color[idx % 5]
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
        Input('main-title', 'value'), Input('xaxis-title', 'value'),
        Input('yaxis-title', 'value'), Input('show-gridlines', 'on'),
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
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,
    gridshow, xzeroline, yzeroline, legendshow,
    datapointsshow, is_vertical, is_log, outliersshow, is_ndatashow,
    is_percentileshow, is_meanshow, is_sdshow, is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, is_statshow, graph_height,
    graph_width, selected_box, box_color, grid_width, dtick
):
    # Update dtick_value
    if dtick != None:
        dtick_value = dtick

    # Title and axises label modificator
    if xaxis_title is None:
        xaxis_title = groupby

    if yaxis_title is None:
        yaxis_title = variable

    if main_title is None:
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
    # max_n = 1.1*max_n

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
                    fillcolor=box_color_saved[i],
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
                    fillcolor=box_color_saved[i],
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

    symbol_size = 8

    # Change Orientation
    type_x = None
    type_y = None
    if (is_vertical):
        xaxis_title, yaxis_title = yaxis_title, xaxis_title
        type_x = 'log' if is_log else None
        if(is_meanshow):
            data_list.append(go.Scatter(x=data_mean, y=group_list, mode='markers', name='Mean', marker=dict(symbol='x', size=symbol_size)))
        # Generating Percentiles to Figure
        if (is_percentileshow):
            data_list.append(go.Scatter(y=group_list, x=percentile_5, mode='markers', name='5%', marker=dict(symbol='diamond', size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_10, mode='markers', name='10%', marker=dict(symbol='cross', size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_90, mode='markers', name='90%', marker=dict(symbol='triangle-up', size=symbol_size)))
            data_list.append(go.Scatter(y=group_list, x=percentile_95, mode='markers', name='95%', marker=dict(symbol='star', size=symbol_size)))
    else:
        type_y = 'log' if is_log else None
        if(is_meanshow):
            data_list.append(go.Scatter(x=group_list, y=data_mean, mode='markers', name='Mean', marker=dict(symbol='x', size=symbol_size)))
        # Generating Percentiles to Figure
        if (is_percentileshow):
            data_list.append(go.Scatter(x=group_list, y=percentile_5, mode='markers', name='5%', marker=dict(symbol='diamond', size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_10, mode='markers', name='10%', marker=dict(symbol='cross', size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_90, mode='markers', name='90%', marker=dict(symbol='triangle-up', size=symbol_size)))
            data_list.append(go.Scatter(x=group_list, y=percentile_95, mode='markers', name='95%', marker=dict(symbol='star', size=symbol_size)))

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
