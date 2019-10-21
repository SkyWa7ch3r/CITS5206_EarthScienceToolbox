# IMPORT LIBRARIES
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
from scipy import stats
import pandas as pd
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import colorlover as cl
import functions as func
import random

# Initial Styles
button_font_size='1.2em'
cardbody_font_size='1em'
cardheader_color='info'
cardbody_color='info'
main_panel_margin={'margin': '10px 0px'}
left_panel_margin={'width': '25%'}
right_panel_margin={'class': 'col-md-8', 'display':'block-inline'}
toggle_switch_color='#91c153'

# generate default colors list
num_of_color = 9
default_color = cl.to_rgb(cl.scales[str(num_of_color)]['qual']['Set1'])
col_idx = 0
default_alpha = 0.65
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], 1)
    default_color[col_idx] = i
    col_idx += 1

MARKERS_LIST = ['circle', 'square', 'diamond', 'cross', 'x', 'triangle-up', 'pentagon', 'hexagon', 'hexagon2',
'octagon', 'star', 'hexagram', 'star-triangle-up', 'hourglass', 'bowtie']
markers_choice = dict()
markers_shape = dict()

app = dash.Dash(__name__)

file_name=r'..\UWA_acid_base_table.xlsx'

df = pd.read_excel(file_name)

cnames = df.select_dtypes(include='number').columns.values
cat_names = df.select_dtypes(exclude=['number', 'datetime', 'datetime64']).columns.values

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
    {'value': 'x', 'label': 'X'},
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

app.layout=html.Div(className='row', children=[
    html.Div(children=[
        html.Div(className='container', children=[
            html.Div(className='accordion', children=[
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Select Data', id='group-1-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Axis Value')),
                                dbc.CardBody(children=func.render_dropdown_valued('xaxis-column', options=cnames, value=cnames[0] ))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Axis Value')),
                                dbc.CardBody(children=func.render_dropdown_valued('yaxis-column', options=cnames, value=cnames[-1] ))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                        ],
                        ), id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size, }
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Plot Settings', id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Swap Axis')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('swap', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Grid Lines')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('GL', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Zero Lines')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('OL', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Label')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LB', False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Legend')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LD', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Colorbar')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LS', True))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Set X Axis Type')),
                                dbc.CardBody(children=func.render_toggleswitch('xaxis-type', ['Linear', 'Logarithmic'], False))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Set Y Axis Type')),
                                dbc.CardBody(children=func.render_toggleswitch('yaxis-type', ['Linear', 'Logarithmic'], False))
                            ], className='col-md-6',
                            ),
                        ],
                        ), id='collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Thresholds', id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Axis Threshold')),
                                dbc.CardBody(children=func.render_input_number('X-thredshold', 'X Axis Threshold'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Axis Threshold')),
                                dbc.CardBody(children=func.render_input_number('Y-thredshold', 'Y Axis Threshold'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Threshold Line Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('x-threshold-style', DASH_DICT, 'solid'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Threshold Line Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('y-threshold-style', DASH_DICT, 'solid'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Threshold Line Color')),
                                dbc.CardBody(children=func.render_colorpicker_small('x-threshold-color', '#ffffff', 0, 0, 0, 1))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Threshold Line Color')),
                                dbc.CardBody(children=func.render_colorpicker_small('y-threshold-color', '#ffffff', 0, 0, 0, 1))
                            ], className='col-md-6',
                            ),
                        ],
                        ), id='collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Statistics', id='group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Linear Best Fit Line')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('linear', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Best Fit Line Style')),
                                dbc.CardBody(children=func.render_dropdown_dict('change-dash', DASH_DICT))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Best Fit Line Color')),
                                dbc.CardBody(children=func.render_colorpicker_small('fit-color-picker', '#ffffff', 0, 0, 0, 1))
                            ], className='col-md-6',
                            ),
                        ],
                        ), id='collapse-4'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Marker Style', id='group-5-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Category Marker Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-markers-dropdown', MARKERS_DICT, 'circle'))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('marker-style-tog', 'Set Marker by a Group', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Group By')),
                                dbc.CardBody(children=func.render_dropdown_valued('marker-drop', cat_names, cat_names[0]))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Select Category')),
                                dbc.CardBody(children=func.render_dropdown_blank('marker-selected-groupby'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                        ],
                        ), id='collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Marker Size', id='group-6-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('marker-size-tog', 'Set Marker Size by a Group', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('The Maximum Size for the Markers')),
                                dbc.CardBody(children=func.render_input_number_min_value('marker-max', 1, 15))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Marker Size Group')),
                                dbc.CardBody(children=func.render_dropdown_valued('marker-size', cnames, cnames[0]))
                            ], style={'margin': '0px 0px 10px 0px', 'height': '30em'}
                            ),
                        ],
                        ), id='collapse-6'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Plot Color', id='group-7-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Group By')),
                                dbc.CardBody(children=func.render_dropdown_valued('color-drop', df.columns, df.columns[0]))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Select Category')),
                                dbc.CardBody(children=func.render_dropdown_blank('color-selected-groupby'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Change Colorscale')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-colorscale-dropdown', COLORSCALES_DICT, 'Greys'))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Category Color')),
                                dbc.CardBody(children=func.render_colorpicker_small('my-color-picker', '#ffffff', 22, 222, 160, 1))
                            ]
                            ),
                        ],
                        ), id='collapse-7'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Graph Settings', id='group-8-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Height')),
                                dbc.CardBody(children=func.render_slider('graph-height', 600, 1200, 600, 50, [600, 700, 800, 900, 1000, 1100, 1200]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Width')),
                                dbc.CardBody(children=func.render_slider('graph-width', 800, 1400, 800, 50, [800, 900, 1000, 1100, 1200, 1300, 1400]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Opacity')),
                                dbc.CardBody(children=func.render_slider('opacity-slider', 0, 100, 70, 1, []))
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Tick Distance')),
                                dbc.CardBody(children=func.render_input_number_min('X-dtick', 'X Axis Delta Tick', 0))
                            ], className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Tick Distance')),
                                dbc.CardBody(children=func.render_input_number_min('Y-dtick', 'Y Axis Delta Tick', 0))
                            ], className='col-md-6',
                            ),
                        ],
                        ), id='collapse-8'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
            ],
            ),
        ],
        ),
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='indicator-graphic',
                    style={'width' : '90%', 'padding-left' : '3%'},
                    config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'legendPosition' : True, 'legendText' : True, 'colorbarPosition' : True, 'colorbarTitleText' : True}}
            ),
        ],
        ),
    ], className='col-md-9'),
], )

# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,9)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,9)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,9)]
)
def toggle_accordion(n1, n2, n3, n4, n5, n6, n7, n8, is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False, False, False, False, False, False
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
    elif button_id ==  'group-8-toggle' and n8:
        return False, False, False, False, False, False, False, not is_open8
    return False, False, False, False, False, False, False, False

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
    [Output('x-threshold-style', 'disabled'),
    Output('y-threshold-style', 'disabled'),
    Output('x-threshold-color', 'disabled'),
    Output('y-threshold-color', 'disabled')],
    [Input('X-thredshold', 'value'),
     Input('Y-thredshold', 'value'),]
)
def enable_threshold_styles(x_t, y_t):
    if x_t is not None:
        x_style = False
        x_color= False
    else:
        x_style = True
        x_color = True
    if y_t is not None:
        y_style = False
        y_color = False
    else:
        y_style = True
        y_color = True
    return x_style, y_style, x_color, y_color

@app.callback(
	[Output('color-selected-groupby', 'options'),
	Output('alignment-colorscale-dropdown', 'disabled'),
	Output('my-color-picker','disabled'),
	Output('LS', 'disabled'),
	Output('color-selected-groupby', 'disabled')
	],
	[Input('color-drop', 'value'),]
	)
def traces_groupby(color_drop):
	if df[color_drop].dtypes =='object':
		idx =0
		for i in df[color_drop].unique():
			markers_choice[i] = default_color[idx % num_of_color]
			idx += 1
		return [{'label': i, 'value': i} for i in df[color_drop].unique()], True, False, True, False
	else:
		return [{'label': color_drop, 'value': color_drop}], False, True, False, True

@app.callback(
    [Output('marker-selected-groupby', 'options'),
    Output('marker-selected-groupby', 'disabled'),
    Output('marker-drop', 'disabled')],
    [Input('marker-style-tog', 'on'),
    Input('marker-drop', 'value')]
)
def markers_groupby(marker_on, marker_drop):
    idx = 0
    if marker_on:
        for i in df[marker_drop].unique():
            markers_shape[i] = random.choice(MARKERS_LIST)
            idx += 1
        return [{'label': i, 'value': i} for i in df[marker_drop].unique()], False, False
    else:
        return [{'label': marker_drop, 'value': marker_drop}], True, True


@app.callback(
	[Output('change-dash', 'disabled'),
    Output('fit-color-picker', 'disabled')],
	[Input('linear', 'on'),]
	)
def show_linear(on):
	if on:
		return False, False
	else:
		return True, True

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
     Input('color-selected-groupby', 'value'),
     Input('my-color-picker', 'value'),
     Input('LB', 'on'),
     Input('LS', 'on'),
     Input('change-dash', 'value'),
     Input('graph-height', 'value'),
     Input('graph-width', 'value'),
     Input('fit-color-picker', 'value'),
     Input('x-threshold-style', 'value'),
     Input('y-threshold-style', 'value'),
     Input('x-threshold-color', 'value'),
     Input('y-threshold-color', 'value'),
     Input('marker-size-tog', 'on'),
     Input('marker-size', 'value'),
     Input('marker-max', 'value'),
     Input('marker-drop', 'value'),
     Input('marker-selected-groupby', 'value'),
     Input('marker-style-tog', 'on'),
     ])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 alignment_colorscale_dropdown, 
                 swap, linear, GL, OL, 
                 alignment_markers_dropdown, color_var, 
                 LD, OS, X_D, Y_D, X_T, Y_T, G_t, C_P, LB,
                 LS, CD, graph_height, graph_width, 
                 fit_color_picker, x_t_style, y_t_style,
                 x_t_color, y_t_color, use_size, marker_size, marker_max, 
                 marker_drop, marker_groupby, marker_on):

    if swap:
    	# Swapping the x and y axes names and values
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp

    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    line = slope*df[xaxis_column_name]+intercept


    threshold_shape = []
    x_color = 'rgba({}, {}, {}, {})'.format(
        x_t_color['rgb']['r'],
        x_t_color['rgb']['g'],
        x_t_color['rgb']['b'],
        x_t_color['rgb']['a'],)

    y_color = 'rgba({}, {}, {}, {})'.format(
        y_t_color['rgb']['r'],
        y_t_color['rgb']['g'],
        y_t_color['rgb']['b'],
        y_t_color['rgb']['a'],)

    #if users set a threshold for X, then show this line
    if X_T !=None:
    	threshold_shape.append(dict(
    	type='line',
    	x0=X_T,
    	x1=X_T,
    	y0=df[yaxis_column_name].min(),
    	y1=df[yaxis_column_name].max(),
        line=dict(
            color=x_color,
            dash=x_t_style
        )
    	))

    #if users set a threshold for Y, then show this line
    if Y_T !=None:{
    	threshold_shape.append(dict(
    	type='line',
    	x0=df[xaxis_column_name].min(),
    	x1=df[xaxis_column_name].max(),
    	y0=Y_T,
    	y1=Y_T,
        line=dict(
            color=y_color,
            dash=y_t_style
        )
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

    if marker_on:
        for cat in df[marker_drop].unique():
            if marker_drop is not None:
                if cat == marker_groupby:
                    markers_shape[cat] = alignment_markers_dropdown
    
    if use_size:
        marker_data = np.array(df[marker_size], dtype='float64')
        marker_size = list(np.interp(marker_data, (marker_data.min(), marker_data.max()), (1, marker_max)))
    else:
        marker_size=15

    traces = []
    #if the data type of the group by column is object, it will show each different values with different colors
    if df[color_var].dtypes=='object' and not marker_on:
    	for i in df[color_var].unique():
    		df_by = df[df[color_var] == i]
    		traces.append(go.Scatter(
	    		x=df_by[xaxis_column_name],
	       		y=df_by[yaxis_column_name],
	       		mode=mode_t,	       		
	       		text=i,
	       		textposition='top center',
	       		opacity=OS/100,
	       		marker={
	       			'size': marker_size,
	       			'line': {'width' :0.5, 'color': 'white'},
	       			'symbol': alignment_markers_dropdown,
	       			'color': markers_choice[i],
	       		},
	       		name=i
	       	    )
            )
    elif df[color_var].dtypes=='object' and marker_on:
        for i in df[color_var].unique():
            for j in df[marker_drop].unique():
                df_by = df[df[color_var] == i][df[marker_drop] == j]
                traces.append(go.Scatter(
                    x=df_by[xaxis_column_name],
                    y=df_by[yaxis_column_name],
                    mode=mode_t,
                    text=i,
                    textposition='top center',
                    opacity=OS/100,
                    marker={
                        'size': marker_size,
                        'line': {'width' :0.5, 'color': 'white'},
                        'color': markers_choice[i],
                        'symbol':markers_shape[j]
                        },
                        name=str(i) + ' : ' + str(j)
                    )
                )
    #if the data type of the group by column is int or float, it will show the VS, and the color based on the X values
    elif (df[color_var].dtypes=='int64' or df[color_var].dtypes=='float64') and not marker_on:
	    traces.append(go.Scatter(
	    	x=df[xaxis_column_name],
	    	y=df[yaxis_column_name],
	    	mode=mode_t,
	    	text = color_var,
	    	opacity=OS/100,
	    	marker=dict(
	    		size = marker_size,
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
    elif (df[color_var].dtypes=='int64' or df[color_var].dtypes=='float64') and marker_on:
        for cat in df[marker_drop].unique():
            df_by = df[df[marker_drop] == cat]
            showScale = False
            if cat == df[marker_drop].unique()[-1]:
                showScale = LS
            traces.append(go.Scatter(
                x=df_by[xaxis_column_name],
                y=df_by[yaxis_column_name],
                mode=mode_t,
                text = color_var,
                opacity=OS/100,
                marker=dict(
                    size = marker_size,
                    line = {'width': 0.5, 'color': 'white'},
                    color = df[color_var],
                    colorscale = alignment_colorscale_dropdown,
                    colorbar=dict(
                        title=color_var
                        ),
                    showscale = showScale,
                    symbol = markers_shape[cat]
                ),
                name=cat,
            ))
        
    fit_color = 'rgba({}, {}, {}, {})'.format(
        fit_color_picker['rgb']['r'],
        fit_color_picker['rgb']['g'],
        fit_color_picker['rgb']['b'],
        fit_color_picker['rgb']['a'],)
    traces.append(go.Scatter(
    	x=df[xaxis_column_name],
        y=line,
        mode='lines',
        name='Y = {:.3f}*X + {:.3f}'.format(slope, intercept),
        marker=dict(
            size = 15,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white'},
            color = fit_color,
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
            'type': 'log' if xaxis_type else 'linear',
           	'showgrid': GL,
           	'zeroline': OL,
            'dtick': X_D
        },
        yaxis={
            'title': yaxis_column_name,
            'type': 'log' if yaxis_type else 'linear',
            'showgrid': GL,
            'zeroline': OL,
            'dtick': Y_D
        },
        title= xaxis_column_name + ' vs. ' + yaxis_column_name,
        showlegend = LD,
        shapes=threshold_shape,
        hovermode='closest',
        height=graph_height,
        width=graph_width
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