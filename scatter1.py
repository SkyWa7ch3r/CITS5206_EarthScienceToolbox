import plotly.graph_objs as go
import dash
import dash_daq as daq
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np
import colorlover as cl
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from scipy import stats
from numpy import arange,array,ones
import colorlover as cl
import random

# Function: Render drop down list with label formatting (remove space between words and turn to lower case)
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown_format(id, options):
    return dcc.Dropdown(id=id, options=options,
        className='card h-100' )

def render_dropdown(id, options):
    return dcc.Dropdown(id=id, options=options,
        className='card h-100' )

# Function: Render drop down list without any options
# Input: id
# Output: dcc.Dropdown
def render_dropdown_blank(id):
    return dcc.Dropdown(id=id)


# Function: Render drop down list with label formatting (remove space between words and turn to lower case)
# Input: id, [options]


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

file_name= r'..\UWA_acid_base_table.xlsx'

df = pd.read_excel(file_name)

cnames = df.select_dtypes(include='number').columns.values
num_of_color=9
default_alpha = 0.65
default_color = cl.to_rgb(cl.scales[str(num_of_color)]['qual']['Set1'])
button_font_size='1.2em'
cardbody_font_size='1em'
cardheader_color='info'
cardbody_color='info'
main_panel_margin={'margin': '10px 0px'}
left_panel_margin={'width': '25%'}
right_panel_margin={'class': 'col-md-8', 'display':'block-inline'}
toggle_switch_color='#91c153'

col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
    col_idx += 1

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
    {'value': 'circle', 'label': 'Circle'},
    {'value': 'square', 'label': 'Square'},
    {'value': 'diamond', 'label': 'Diamond'},
    {'value': 'cross', 'label': 'Cross'},
    {'value': 'x', 'label': 'x'},
    {'value': 'triangle-up', 'label': 'Triangle-up'},
    {'value': 'pentagon', 'label': 'Pentagon'},
    {'value': 'hexagon', 'label': 'Hexagon'},
    {'value': 'hexagon2', 'label': 'Hexagon2'},
    {'value': 'octagon', 'label': 'Octagon'},
    {'value': 'star', 'label': 'Star'},
    {'value': 'hexagram', 'label': 'Hexagram'},
    {'value': 'star-triangle-up', 'label': 'Star-triangle-up'},
    {'value': 'hourglass', 'label': 'Hourglass'},
    {'value': 'bowtie', 'label': 'Bowtie'},
]

DASH_DICT = [
    {'value': 'solid', 'label': 'Solid'}, 
    {'value': 'dash', 'label': 'Dash'},
    {'value': 'dot', 'label': 'Dot'},
    {'value': 'dashdot', 'label': 'Dash Dot'},
    {'value': 'longdash', 'label': 'Long Dash'},
    {'value': 'longdashdot', 'label': 'Long Dash Dot'}
]

MARKERS_LIST = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'pentagon', 'hexagon', 'hexagon2',
'octagon', 'star', 'hexagram', 'star-triangle-up', 'hourglass', 'bowtie'
]

markers_choice = dict()
markers_shape = dict()


## MAIN APP HERE
app = dash.Dash(__name__, suppress_callback_exceptions=True)
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
                                dbc.CardHeader(html.H5('X-Value')),
                                dbc.CardBody(children=render_radio('xaxis-column', cnames))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y-Value')),
                                dbc.CardBody(children=render_radio('yaxis-column', cnames))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            )
                        ]),
                        id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Plot Setting", id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Swap Axis')),
                                dbc.CardBody(children=render_booleanswitch_nolab('swap', False))
                            ], className='col-md-3', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Legend')),
                                dbc.CardBody(children=render_booleanswitch_nolab('LD', True))
                            ], className='col-md-3', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Show Label')),
                                dbc.CardBody(children=render_booleanswitch_nolab('LB', True))
                            ], className='col-md-3', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Grid Lines')),
                                dbc.CardBody(children=render_booleanswitch_nolab('GL', False))
                            ], className='col-md-3', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Zero Marker')),
                                dbc.CardBody(children=render_booleanswitch_nolab('OL', True))
                            ], className='col-md-3', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Legend of ColorScale')),
                                dbc.CardBody(children=render_booleanswitch_nolab('LS', True))
                            ],className='col-md-6',style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X-Tick Step')),
                                dbc.CardBody(children=render_input_number('X-dtick', 'Tick Step'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y-Tick Step')),
                                dbc.CardBody(children=render_input_number('Y-dtick', 'Tick Step'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-2'
                    ),
                ], color='info', outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Plot Orientation", id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('X-Data Transformation')),
                                dbc.CardBody(children=render_toggleswitch('xaxis-type', ['Linear', 'Logarithmic'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y-Data Transformation')),
                                dbc.CardBody(children=render_toggleswitch('yaxis-type', ['Linear', 'Logarithmic'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Threshold Settings", id='group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('X-Threshold')),
                                dbc.CardBody(children=render_input_number('X-thredshold', 'X Threshold'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y-Threshold')),
                                dbc.CardBody(children=render_input_number('Y-thredshold', 'Y Threshold'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-4'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Line of Best Fit", id='group-5-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Linear best fit')),
                                dbc.CardBody(children=render_booleanswitch_nolab('linear', False))
                            ],style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Line Style')),
                                dbc.CardBody(children=render_dropdown_format('change-dash',DASH_DICT))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                #############################################################################################################
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Color and Markers", id='group-6-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            '''
                            In this section there needs to be
                            color-drop is a dropdown which uses all the columns in the dataframe 
                            selected-groupby which uses a blank drop down
                            alignment-colorscale-dropdown needs to be the COLORSCALE DICT as options
                            alignment-markers-dropdown needs to be a dropdown with MARKERS_DICT
                            my-color-picker is a color picker
                            '''
                            dbc.Card([
                                dbc.CardHeader(html.H5('X-Value')),
                                dbc.CardBody(children=render_radio('select-variable', cnames))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y-Value')),
                                dbc.CardBody(children=render_radio('select-groupby', cnames))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
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
                        dbc.Button("Graph Size", id='group-7-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
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
                        id='collapse-7'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='indicator-graphic',
                    style={'width' : '90%', 'padding-left' : '3%'},
                    config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'titleText': True}},
            ),
        ]),
    ], className='col-md-9'
    ),
], style=main_panel_margin)

# CALLBACK GOES HERE
# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,9)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,9)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,9)]
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, n7, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False, False, False, False, False,False
    elif button_id ==  'group-2-toggle' and n2:
        return False, not is_open2, False, False, False, False, False, False
    elif button_id ==  'group-3-toggle' and n3:
        return False, False, not is_open3, False, False, False, False, False
    elif button_id ==  'group-4-toggle' and n4:
        return False, False, False, not is_open4, False, False, False, False
    elif button_id ==  'group-5-toggle' and n5:
        return False, False, False, False, not is_open5, False, False, False
    elif button_id ==  'group-6-toggle' and n6:
        return False, False, False, False, False, not is_open6, False, False
    elif button_id ==  'group-7-toggle' and n7:
        return False, False, False, False, False, False, not is_open7, False
    return False, False, False, False, False, False, False

@app.callback(
    Output('my-color-picker', 'value'),
    [Input('alignment-markers-dropdown', 'value')]
)
def update_scatter_color_selector(box):
    temp_str = markers_choice.get(box, dict(rgb=dict(r=222, g=110, b=75, a=default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb=dict(r=temp_str[0], g=temp_str[1], b=temp_str[2], a=temp_str[3]))
    return temp_str

@app.callback(
	[Output('linear', 'on'),
	Output('linear', 'disabled')
	],
	[Input('xaxis-type', 'value'),
	Input('yaxis-type', 'value'),
	]
	)
def show_fitline(xv, yv):
	if xv=='Log' or yv=='Log':
		return False,True
	else:
		return False,False

@app.callback(
	[Output('selected-groupby', 'options'),
	Output('alignment-colorscale-dropdown', 'disabled'),
	Output('my-color-picker','disabled'),
	Output('LS', 'disabled'),
	Output('selected-groupby', 'disabled')
	],
	[Input('color-drop', 'value'),]
	)
def traces_groupby(color_drop):
	if df[color_drop].dtypes =='object':
		idx =0
		for i in df[color_drop].unique():
			markers_choice[i] = default_color[idx % num_of_color]
			markers_shape[i] = random.choice(MARKERS_LIST)
			idx += 1
		return [{'label': i, 'value': i} for i in df[color_drop].unique()], True, False, True, False
	else:
		return [{'label': color_drop, 'value': color_drop}], False, True, False, True

@app.callback(
	Output('change-dash', 'disabled'),
	[Input('linear', 'on'),]
	)
def show_linear(on):
	if on:
		return False
	else:
		return True


@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('alignment-colorscale-dropdown', 'value'),
     Input('swap', 'on'),
     Input('linear', 'on'),
     Input('GL', 'on'),
     Input('OL', 'on'),
     Input('alignment-markers-dropdown', 'value'),
     Input('color-drop', 'value'),
     Input('LD', 'on'),
     Input('opacity-slider', 'value'),
     Input('X-dtick', 'value'),
     Input('Y-dtick', 'value'),
     Input('X-thredshold', 'value'),
     Input('Y-thredshold', 'value'),
     Input('selected-groupby', 'value'),
     Input('my-color-picker', 'value'),
     Input('LB', 'on'),
     Input('LS', 'on'),
     Input('change-dash', 'value'),
     Input('graph-height', 'value'),
     Input('graph-width', 'value'),])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type, alignment_colorscale_dropdown, 
                 swap, linear, GL, OL, 
                 alignment_markers_dropdown, color_var, LD, OS, X_D, Y_D, X_T, Y_T, G_t, C_P, LB, LS, CD,graph_height,
                 graph_width,):

    if swap:
    	# Swapping the x and y axes names and values
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp

    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    line = slope*df[xaxis_column_name]+intercept


    threshold_shape = []


    #if users set a threshold for X, then show this line
    if X_T !=None:
    	threshold_shape.append(dict(
    	type='line',
    	x0=X_T,
    	x1=X_T,
    	y0=df[yaxis_column_name].min(),
    	y1=df[yaxis_column_name].max()
    	))

    #if users set a threshold for Y, then show this line
    if Y_T !=None:{
    	threshold_shape.append(dict(
    	type='line',
    	x0=df[xaxis_column_name].min(),
    	x1=df[xaxis_column_name].max(),
    	y0=Y_T,
    	y1=Y_T
    	))}

    mode_t='markers'
    if LB:
    	mode_t='markers+text'

    picker_markers_color = 'rgba({}, {}, {}, {})'.format(
        C_P['rgb']['r'],
        C_P['rgb']['g'],
        C_P['rgb']['b'],
        C_P['rgb']['a'],)

    if df[color_var].dtypes=='object':
    	for i in df[color_var].unique():
    		if color_var is not None:
    			if i == G_t:
    				markers_choice[i] = picker_markers_color
    				markers_shape[i] = alignment_markers_dropdown

    traces = []
    #if the data type of the group by column is object, it will show each different values with different colors
    if df[color_var].dtypes=='object':
    	for i in df[color_var].unique():
    		df_by = df[df[color_var] == i]
    		if i == G_t:
    			traces.append(go.Scatter(
	    		x=df_by[xaxis_column_name],
	       		y=df_by[yaxis_column_name],
	       		mode=mode_t,	       		
	       		text=i,
	       		textposition='top center',
	       		opacity=OS/100,
	       		marker={
	       			'size': 15,
	       			'line': {'width' :0.5, 'color': 'white'},
	       			'symbol': alignment_markers_dropdown,
	       			'color': markers_choice[i],
	       		},
	       		name=i
	       		))
    		else:
		    	traces.append(go.Scatter(
		    		x=df_by[xaxis_column_name],
		       		y=df_by[yaxis_column_name],
		       		mode=mode_t,
		       		text=i,
		       		textposition='top center',
		       		opacity=OS/100,
		       		marker={
		       			'size': 15,
		       			'line': {'width' :0.5, 'color': 'white'},
		       			'color': markers_choice[i],
		       			'symbol':markers_shape[i]
		       		},
		       		name=i
		    	))

    #if the data type of the group by column is int or float, it will show the VS, and the color based on the X values
    if df[color_var].dtypes=='int64' or df[color_var].dtypes=='float64':
	    traces.append(go.Scatter(
	    	x=df[xaxis_column_name],
	    	y=df[yaxis_column_name],
	    	mode=mode_t,
	    	text = color_var,
	    	opacity=OS/100,
	    	marker=dict(
	    		size = 15,
	        	line = {'width': 0.5, 'color': 'white'},
	        	color = df[color_var],
	        	colorscale = alignment_colorscale_dropdown,
	        	colorbar=dict(
	        		title=color_var
	        		),
	        	showscale = LS,
	        	symbol = alignment_markers_dropdown
	    	),
	    	name='{} VS {}'.format(xaxis_column_name, yaxis_column_name)
	    ))

    traces.append(go.Scatter(
    	x=df[xaxis_column_name],
        y=line,
        mode='lines',
        name='Y = {:.3f}*X + {:.3f}'.format(slope, intercept),
        marker=dict(
            size = 15,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white'},
            color = 'black',
            showscale = LD
        ),
        line = dict(
        	dash=CD
        	),
        visible=linear
    ))

    layou_t=dict(
    	xaxis={
            'title': xaxis_column_name,
            'type': 'linear' if xaxis_type == 'Linear' else 'log',
           	'showgrid': GL,
           	'zeroline': OL,
            'dtick': X_D
        },
        yaxis={
            'title': yaxis_column_name,
            'type': 'linear' if yaxis_type == 'Linear' else 'log',
            'showgrid': GL,
            'zeroline': OL,
            'dtick': Y_D
        },
        title= xaxis_column_name + 'vs.' + yaxis_column_name,
        showlegend = LD,
        shapes=threshold_shape,
        hovermode='closest',
        height=graph_height,
        width=graph_width,
    	)

    return {
       	'data': 
       		traces,

       	'layout': go.Layout(
           	layou_t
       	)
    }


if __name__ == '__main__':
    app.run_server(debug=True)
