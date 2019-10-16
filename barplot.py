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
bar_color_saved = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
dtick_value = None
plottype = " "

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

# Function: Render radio items for plottype
# Input: id
# Output: dcc.RadioItems
def render_radio_plotype(id):
    return dcc.RadioItems(
        id=id,
        options=[
            {'label': 'Single', 'value': 'Single'},
            {'label': 'Percentage', 'value': 'Stacked_Percentage'},
            {'label': 'Side by Side', 'value': 'Side_by_Side'},
            {'label': 'Stacked', 'value': 'Stacked'},
        ],
        value='plottype',
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

# MAIN APP HERE
# Loading Data
file_name = r'C:\Users\james\Downloads\PANDAAS\UWA_acid_base_table.xlsx'
df = read_file(file_name)


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
                                dbc.CardBody(children=render_radio('select-variable', cat_features))
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
                        dbc.Button("Select Bar Plot Type", id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Bar Plot Type')),
                                dbc.CardBody(children=render_radio_plotype('select-barplot'))
                            ],
                            ),
                        ]),
                        id='collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Graph Setting", id='group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Graph Orientation')),
                                dbc.CardBody(children=render_toggleswitch('graph-alignment', ['Horizontal','Vertical'], True))
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
                        id='collapse-4'
                    ),
                ], color='info', outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Statistic Information", id='group-5-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Data Transformation')),
                                dbc.CardBody(children=render_toggleswitch('data-transform', ['Linear', 'Logarithmic'], False))
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Frequency')),
                                dbc.CardBody(children=render_booleanswitch_nolab('show-ndata', False))
                            ],
                            ),
                        ]),
                        id='collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Threshold Setting", id='group-6-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
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
                        id='collapse-6'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button(
                            "Color Setting", id='group-7-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H2('Select Bar')),
                                dbc.CardBody(children=render_radio_blank('select-bar'))
                            ], className='col-md-6', style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H2('Bar Color')),
                                dbc.CardBody(children=render_colorpicker('bar-color', 'white', 0, 0, 255, 0.65))
                            ],
                            ),
                        ]),
                        id='collapse-7'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} )
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='bar-plot'),
        ])
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

# Turn Y Tick Disabled when in Logarithmic and Enabled when in Linear
# Turn Y Tick Value to None when in Logarithmic end recall previous value when turn back to Linear
@app.callback(
    [Output('delta-tick', 'disabled'),
     Output('delta-tick', 'value')],
    [Input('data-transform', 'value')]
)
def update_delta_tick_disabled(is_log):
    return is_log, None if is_log else dtick_value

# Bar Color Selector Callback
@app.callback(
    Output('bar-color', 'value'),
    [Input('select-bar', 'value')]
)
def update_bar_color_selector(bar):
    temp_str = bar_color_saved.get(bar, dict(rgb=dict(r=222, g=110, b=75, a=default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb=dict(r=temp_str[0], g=temp_str[1], b=temp_str[2], a=temp_str[3]))
    return temp_str

# Bar Selector Callback
@app.callback(
    Output('select-bar', 'options'),
    [Input('select-groupby', 'value'), ]
)
def update_select_bar(groupby):

    idx = 0
    if(plottype=="Single"):
        variable = groupby
        for i in df[variable].unique():
            bar_color_saved[i] = default_color[idx % 5]
            idx += 1
        return [{'label': i, 'value': i} for i in df[variable].unique()]

    else :
        for i in df[groupby].unique():
            bar_color_saved[i] = default_color[idx % 5]
            idx += 1
        return [{'label': i, 'value': i} for i in df[groupby].unique()]

# Threshold Line Callback
@app.callback(
    Output('treshold-value', 'value'),
    [Input('show-treshold', 'on'),
     ]
)
def update_treshold_value(
    is_tresholdshow
):
    return '25' if is_tresholdshow else ' '

# Figure Callback
@app.callback(
    Output('bar-plot', 'figure'),
    [
        Input('select-variable', 'value'),
        Input('select-groupby', 'value'),
        Input('main-title', 'value'),
        Input('xaxis-title', 'value'),
        Input('yaxis-title', 'value'),
        Input('select-barplot', 'value'),
        Input('show-gridlines', 'on'),
        Input('show-zeroline-x', 'on'),
        Input('show-zeroline-y', 'on'),
        Input('show-legend', 'on'),
        Input('graph-alignment', 'value'),
        Input('data-transform', 'value'),
        Input('show-ndata', 'on'),
        Input('show-treshold', 'on'),
        Input('treshold-value', 'value'),
        Input('treshold-style', 'value'),
        Input('treshold-line-color', 'value'),
        Input('treshold-line-size', 'value'),
        Input('graph-height', 'value'),
        Input('graph-width', 'value'),
        Input('select-bar', 'value'),
        Input('bar-color', 'value'),
        Input('grid-width', 'value'),
        Input('delta-tick', 'value'),
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,plottype,
    gridshow, xzeroline, yzeroline, legendshow,
    is_vertical, is_log,is_ndatashow,is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, graph_height,
    graph_width, selected_bar, bar_color, grid_width, dtick
):
    # Update dtick_value
    if dtick != None:
        dtick_value = dtick

    # Title and axis default title
    if(plottype=="Single"):
        if xaxis_title is None:
            xaxis_title = str("Count")

        if yaxis_title is None:
            yaxis_title = variable

        if main_title is None:
            main_title = str("BARPLOT")
    elif(plottype=="Stacked_Percentage"):
        if xaxis_title is None:
            xaxis_title = str("Percentage % ")

        if yaxis_title is None:
            yaxis_title = variable

        if main_title is None:
            main_title = str("BARPLOT")

    else:
        if xaxis_title is None:
            xaxis_title = str("Count")

        if yaxis_title is None:
            yaxis_title = variable

        if main_title is None:
            main_title = str("BARPLOT")


    # Initialising data list
    data_list = []
    pct = []
    cnt = []
    pct_text = []
    cnt_idx = []
    cnt_text = []
    n_data = []
    annots_idx = 0
    annots_ndata=[]

    # Computing N Data
    max_n = 100
    max_n = 1.05*np.log10(max_n) if is_log else 1.05*max_n


    picker_bar_color = 'rgba({}, {}, {}, {})'.format(
        bar_color['rgb']['r'],
        bar_color['rgb']['g'],
        bar_color['rgb']['b'],
        bar_color['rgb']['a'],)

    color_idx = 0
    if(plottype=="Single"):
        group_list = df[variable].unique()
        var_list = df[variable].unique()
        groupby=variable
    else :
        group_list = df[groupby].unique()
        var_list = df[variable].unique()
    # Generate barplot
    idx=0
    if(plottype== "Stacked_Percentage"):
        print(plottype)
        for i in group_list:
            pct_idx=0
            if selected_bar is not None:
                print('selected_bar : {}'.format(selected_bar))
                print('bar color 1 : {}'.format(bar_color_saved))
                if i == selected_bar:
                    bar_color_saved[i] = picker_bar_color
                    print('bar color 2 : {}'.format(bar_color_saved))
            color_idx += 1

            for j in var_list:
                count_all=df[df[variable]==j][variable].count()
                count_me=df[df[variable]==j][df[groupby]==i][groupby].count()
                pct.append(count_me*100/count_all)
                pct_text.append("{}%".format(round(count_me*100/count_all)))
            if (is_vertical):
                data_list.append(
                        go.Bar(
                            x=var_list,
                            y=pct,
                            name=i,
                            text =pct_text if is_ndatashow else None,
                            textposition ="auto",
                        )
                    )
                pct=[]
                idx +=1
                pct_idx += 1
                pct_text=[]
            else:
                data_list.append(
                        go.Bar(
                            x=pct,
                            y=var_list,
                            name=i,
                            orientation='h',
                            text =pct_text if is_ndatashow else None,
                            textposition ="auto",
                        )
                    )
                pct =[]
                idx +=1
                pct_idx += 1
                pct_text=[]
            # Counting number of data for each category
            df_shape= df[df[groupby] == i][variable].shape
            n_data.append(df_shape[0])

            # Generating annotations of n of data
            annots_ndata.append(go.layout.Annotation(
                x=annots_idx if is_vertical else max_n,
                y=max_n if is_vertical else annots_idx,
                xref='x',
                yref='y',
                text='N = {}'.format(n_data[annots_idx]),
                showarrow=False,
                ax=0 if is_vertical else annots_idx,
                ay=annots_idx if is_vertical else 0,
                )
            )
            annots_idx = annots_idx + 1

        if(not is_ndatashow):
            annots_ndata= []

        annots_ndata= annots_ndata


    elif(plottype=="Side_by_Side" or plottype== "Stacked"):
        for i in group_list:
            if selected_bar is not None:
                print('selected_bar : {}'.format(selected_bar))
                print('bar color 1 : {}'.format(bar_color_saved))
                if i == selected_bar:
                    bar_color_saved[i] = picker_bar_color
                    print('bar color 2 : {}'.format(bar_color_saved))
            color_idx += 1

            cnt_idx=0
            for j in var_list:
                count_all=df[df[variable]==j][variable].count()
                count_me=df[df[variable]==j][df[groupby]==i][groupby].count()
                cnt.append(count_me)
                cnt_text.append("{}".format(count_me))
            if (is_vertical):
                data_list.append(
                        go.Bar(
                            x=var_list,
                            y=cnt,
                            name=i,
                            text =cnt_text if is_ndatashow else None,
                            textposition ="auto",
                        )
                    )
                cnt = []
                idx +=1
                cnt_idx += 1
                cnt_text=[]
            else:
                data_list.append(
                        go.Bar(
                            x=cnt,
                            y=var_list,
                            name=i,
                            orientation='h',
                            text =cnt_text if is_ndatashow else None,
                            textposition ="auto",
                        )
                    )
                idx +=1
                cnt_idx += 1
                cnt = []
                cnt_text=[]
    else:
        for i in var_list:
            if selected_bar is not None:
                print('selected_bar : {}'.format(selected_bar))
                print('bar color 1 : {}'.format(bar_color_saved))
                if i == selected_bar:
                    bar_color_saved[i] = picker_bar_color
                    print('bar color 2 : {}'.format(bar_color_saved))
            color_idx += 1
            pct.append(df[df[variable]==i][variable].count()),

            if (not is_vertical):
                data_list.append(
                    go.Bar(
                        x=[pct[0]],
                        y=[var_list[idx]],
                        name=i,
                        orientation='h',
                        text =pct if is_ndatashow else None,
                        textposition ="auto",
                    )
                )
                pct =[]
                idx += 1
            else:
                data_list.append(
                    go.Bar(
                        x=[var_list[idx]],
                        y=[pct[0]],
                        name=i,
                        text=pct if is_ndatashow else None,
                        textposition ="auto",
                    )
                )
                pct =[]
                idx += 1
    # Change Orientation
    type_x = None
    type_y = None
    if (is_vertical):
        xaxis_title, yaxis_title = yaxis_title, xaxis_title
        type_y = 'log' if is_log else None

    else:
        type_x = 'log' if is_log else None

    if (plottype== "Side_by_Side"):
            is_side = True
    else:
            is_side = False

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
            x0=-0.5 if is_vertical else treshold_value,
            x1=len(var_list)-0.5 if is_vertical else treshold_value,
            y0=treshold_value if is_vertical else -0.5,
            y1=treshold_value if is_vertical else len(var_list)-0.5,
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
                dtick=None if is_vertical else dtick,
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=gridshow,
                zeroline=yzeroline,
                type=type_y,
                gridwidth=grid_width,
                gridcolor='lightgrey',
                dtick=dtick if is_vertical else None,
            ),
            barmode = "group" if is_side else "stack",
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
