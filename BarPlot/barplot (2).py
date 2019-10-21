
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash_daq as daq
from dash.dependencies import Input, Output
import colorlover as cl


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



# Loading Data
file_name = r'C:\Users\james\Downloads\PANDAAS\UWA_acid_base_table.xlsx'
df = read_file(file_name)

# Loading non-Numeric Data from Dataframe
cat_features = df.select_dtypes(exclude='number').columns.values

# Init Dash App
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

label_background_color = '#67acb7'
content_background_color = '#c0fdfb'
border_color = '#868686'
main_panel_padding = '10px 25px'
label_padding = '10px 10px 0px 10px'
toggle_switch_color = '#91c153'
line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']
default_alpha = 0.65
bar_color_saved = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
# generate default colors list
col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},,{})'.format(i[0], i[1], i[2],default_alpha)
    default_color[col_idx] = i
    col_idx += 1


content_style_even = {
    'margin': '0px',
    'border-width': '2px',
    'border-color': border_color,
    'border-style': 'solid',
    'background-color': border_color, }

content_style_odd = {
    'margin': '0px',
    'border-width': '2px',
    'border-color': border_color,
    'border-style': 'solid',
    'background-color': content_background_color, }

content_style_dropdown_inline = {
    'margin': '0px',
    'padding': '10px', }

border_style_dropdown_inline = {
    'border-width': '2px',
    'border-color': border_color,
    'border-style': 'solid',
    'background-color': '#ffffff',
}
app.layout = html.Div(children=[
    # Main Panel
    html.Div(className="row", children=[
        # Left Panel
        html.Div(className="col-md-3", children=[
            # Select Data Label
            html.Div(className="row", children=[
                html.Div(className="col-md-12", children=[
                    html.H5("Select Data")
                ], style={
                    'background-color': label_background_color, }
                )
            ], style={
                'padding': '0px',
                'margin': '0px', }
            ),
            # Select Data Drop Down
            html.Div(className="row", children=[
                # Variable Drop Down
                html.Div(className='col-md-6', children=[
                    html.Div(className="row", children=[
                        # Variable Drop Down Label
                        html.H5('Variable'),
                    ], style={
                        'padding': '0px 10px 0px 10px', }
                    ),
                    html.Div(className="row", children=[
                        # Variable Drop Down List
                        dcc.Dropdown(
                            id='select-variable',
                            options=[{'label': i, 'value': i} for i in cat_features],
                            value=str(cat_features[0])
                        ),
                    ], style={
                        'padding': '0px 5px 5px 5px', }
                    ),
                ], style=content_style_odd
                ),
                # Groupby Drop Down
                html.Div(className="col-md-6", children=[
                    html.Div(className="row", children=[
                        # Group Drop Down Label
                        html.H5('Group by'),
                    ], style={
                        'padding': '0px 10px 0px 10px', }
                    ),
                    html.Div(className="row", children=[
                        # Group Drop Down List
                        dcc.Dropdown(
                            id='select-groupby',
                            options=[{'label': i, 'value': i} for i in cat_features],
                            value=str(cat_features[0])
                        ),
                    ], style={
                        'padding': '0px 5px 5px 5px', }
                    ),
                ], style=content_style_odd
                ),
            ], style={
                'padding': '0px',
                'margin': '0px', }
            ),
            # Change Title Label
            html.Div(className="row", children=[
                html.Div(className="col-md-12", children=[
                    html.H5("Change Title and Axis Labels")
                ], style={
                    'padding': '0px 10px 0px 10px',
                    'background-color': label_background_color, }
                )
                ], style={
                    'padding': '0px',
                    'margin': '5px 0px 0px 0px', }
            ),
            # Title and Label Inputs
            html.Div(className='row', children=[
                html.Div(className="col-md-4", children=[
                    html.Div(className='row', children=[
                        # Title Label
                        html.Div(className='col-md-12', children=[
                            html.H5('Title Label')
                        ], style={'padding': '0px 0px 0px 5px'}
                        ),
                    ],
                    ),
                    html.Div(className='row', children=[
                        # Title Input
                        html.Div(className='col-md-12', children=[
                            dcc.Input(id='main-title', type='text', placeholder='Main Title', size='17'),
                        ], style={'padding': '0px 0px 5px 5px'}
                        ),
                    ],
                    ),
                ], style=content_style_odd
                ),
                html.Div(className="col-md-4", children=[
                    # X Axis Label Config
                    html.Div(className='row', children=[
                        # X Axis label
                        html.Div(className='col-md-12', children=[
                            html.H5('X Axis Label')
                        ], style={'padding': '0px 0px 0px 5px'}
                        ),
                    ],
                    ),
                    html.Div(className='row', children=[
                        # X Axis Input
                        html.Div(className='col-md-12', children=[
                            dcc.Input(id='xaxis-title', type='text', placeholder='X Axis Label', size='17'),
                        ], style={'padding': '0px 0px 5px 5px'}
                        ),
                    ],
                    ),
                ], style=content_style_odd
                ),
                html.Div(className="col-md-4", children=[
                    # Y Axis label Config
                    html.Div(className='row', children=[
                        # Y Axis label
                        html.Div(className='col-md-12', children=[
                            html.H5('Y Axis Label')
                        ], style={'padding': '0px 0px 0px 5px'}
                        ),
                    ],
                    ),
                    html.Div(className='row', children=[
                        # Y Axis Input
                        html.Div(className='col-md-12', children=[
                            dcc.Input(id='yaxis-title', type='text', placeholder='Y Axis Label', size='17'),
                        ], style={'padding': '0px 0px 5px 5px'}
                        ),
                    ],
                    ),
                ], style=content_style_odd
                ),
            ], style={
                'padding': '0px',
                'margin': '0px', }
            ),
            # Graph Setting Label
            html.Div(className='row', children=[
                html.Div(className="col-md-12", children=[
                    html.H5('Graph Setting'),
                ], style={
                    'padding': '0px 10px 0px 10px',
                    'background-color': label_background_color, }
                )
                ], style={
                    'padding': '0px',
                    'margin': '5px 0px 0px 0px', }
            ),
            # Data Transformation
            html.Div(className='row', children=[
                # Data Transoformation Label
                html.Div(className='col-md-5', children=[
                    html.H5('Data Transformation'),
                ], style={
                    'padding': '0px 10px 0px 10px',
                    'background-color': content_background_color, }
                ),
                # Data Transformation Toogle Switch
                html.Div(className='col-md-7', children=[
                    daq.ToggleSwitch(
                        id='data-transform',
                        label=['Linear', 'Logarithmic'],
                        value=False,
                        size='35',
                        color=toggle_switch_color, ),
                ], style={
                    'padding': '9px 10px 5px 10px',
                    'background-color': content_background_color, }
                ),
            ], style=content_style_odd
            ),
            # Graph Orientation
            html.Div(className='row', children=[
                # Graph Orientation Label
                html.Div(className='col-md-5', children=[
                    html.H5('Graph Orientation')
                ], style={
                    'padding': '0px 10px 0px 10px', }
                ),
                # Graph Orientation Toogle Switch
                html.Div(className='col-md-7', children=[
                    daq.ToggleSwitch(
                        id='graph-alignment',
                        label=['Horizontal', 'Vertical'],
                        value=True,
                        size='35',
                        color=toggle_switch_color, ),
                ], style={
                    'padding': '10px 10px 5px 10px',
                    'text-align': 'center'}
                ),
            ], style=content_style_odd
            ),
            # Plot type
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    html.H5('Select Bar Plot Type')
                ], style=content_style_dropdown_inline
                ),
                # types of plot
                html.Div(className='col-md-6', children=[
                    dcc.Dropdown(
                        id='select-plottype',
                        options=[
                            {'label': 'Single', 'value': 'Single'},
                            {'label': 'Stacked', 'value': 'Stacked'},
                            {'label': 'Side by Side', 'value': 'Side_by_Side'},
                            {'label': 'Percentage', 'value': 'Stacked_Percentage'},
                        ],
                        value='plottype',
                    ),
                ], style=content_style_dropdown_inline
                ),
            ], style={
                'padding': '0px',
                'margin': '0px',
                'border-width': '2px',
                'border-color': border_color,
                'border-style': 'solid',
                'background-color': content_background_color, }
            ),
            # enter ticks
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    html.H5('Enter data ticks')
                ], style=content_style_dropdown_inline
                ),
                # Outliers Configuration
                html.Div(className='col-md-6', children=[
                    dcc.Input(
                        id='dtick',
                        type='number',
                        placeholder='Enter dtick',
                        size='30',
                        min=1,
                    ),
                ], style=content_style_dropdown_inline
                ),
            ], style={
                'padding': '0px',
                'margin': '0px',
                'border-width': '2px',
                'border-color': border_color,
                'border-style': 'solid',
                'background-color': content_background_color, }
            ),
            # Show/hide Legend
            html.Div(className='row', children=[
                # Show/hide Legend Label
                html.Div(className='col-md-6', children=[
                    daq.BooleanSwitch(
                        id='show-legend',
                        on=True,
                        # size='35',
                        label='Legend',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
                # Show/hide Legend Toogle Switch
                html.Div(className='col-md-6', children=[
                    daq.BooleanSwitch(
                        id='show-ndata',
                        on=True,
                        # size='35',
                        label='Frequency',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
            ], style={
                'padding': '0px',
                'margin': '0px'}
            ),
            # Show/hide Lines
            html.Div(className='row', children=[
                # Show/hide Gridlines
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-gridlines',
                        on=True,
                        # size='35',
                        label='Gridlines',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
                # Show/hide X Axis Zerolines
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-zeroline-x',
                        on=True,
                        # size='35',
                        label='X Zeroline',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
                # Show/hide Y Axis Zerolines
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-zeroline-y',
                        on=True,
                        # size='35',
                        label='Y Zeroline',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
            ], style={
                'padding': '0px',
                'margin': '0px'}
            ),
            # Show/hide Treshold
            html.Div(className='row', children=[
                # Show/hide Treshold
                html.Div(className='col-md-4', children=[
                    html.Div(className='row', children=[
                        html.Div(className='col-md-12', children=[
                            daq.BooleanSwitch(
                                id='show-treshold',
                                on=False,
                                label='Threshold',
                                labelPosition='top',
                                color=toggle_switch_color,
                                style={
                                    'padding': '10px',
                                }
                            ),
                        ],
                        ),
                    ],
                    ),
                    html.Div(className='row', children=[
                        # Treshold value Label
                        html.Div(className='col-md-12', children=[
                            html.H5('Value')
                        ], style={'padding': '0px 0px 0px 5px'}
                        ),
                    ],
                    ),
                    html.Div(className='row', children=[
                        # Treshold Input
                        html.Div(className='col-md-12', children=[
                            dcc.Input(
                                id='treshold-value',
                                type='text',
                                placeholder='Enter here',
                                size='17',
                                disabled=True),
                        ], style={'padding': '0px 0px 5px 5px'}
                        ),
                    ],
                    ),
                    html.Div(className="row", children=[
                        # Treshold Drop Down Line Style
                        html.H5('Style'),
                    ], style={
                        'padding': '0px 10px 0px 10px', }
                    ),
                    html.Div(className="row", children=[
                        # Variable Drop Down List
                        dcc.Dropdown(
                            id='treshold-style',
                            options=[{'label': i, 'value': (i.replace(" ", "")).lower()} for i in line_style],
                            value=(str(line_style[0]).replace(" ", "")).lower(),
                            disabled=True
                        ),
                    ], style={
                        'padding': '0px 5px 5px 5px', }
                    ),
                    html.Div(className="row", children=[
                        # Treshold Drop Down Line Style
                        daq.NumericInput(
                            id='treshold-line-size',
                            min=1,
                            max=10,
                            value=2,
                            label='Size:',
                        ),
                    ], style={
                        'padding': '0px 10px 0px 10px', }
                    ),
                ],
                ),
                # Line color selection
                html.Div(className='col-md-8', children=[
                    daq.ColorPicker(
                        id='treshold-line-color',
                        label='Threshold Color',
                        style={'background-color': 'white'},
                        value=dict(rgb=dict(r=0, g=0, b=255, a=1))
                    )
                ], style={'padding': '10px 5px 5px 5px'}
                ),
            ], style=content_style_odd
            ),
            html.Div(className='row', children=[
                html.Div(className='col-md-4', children=[
                    html.Div(className='row', children=[
                        html.H5('Select bar')
                    ],
                    ),
                    html.Div(className='row', children=[
                        dcc.Checklist(
                            id='select-bar',
                        )
                    ],
                    ),
                ],
                ),
                html.Div(className='col-md-8', children=[
                    daq.ColorPicker(
                        id='bar-color',
                        label='Bar Marker Color',
                        style={'background-color': 'white'},
                        value=dict(rgb=dict(r=222, g=110, b=75, a=1))
                    )
                ], style={'padding': '10px 5px 5px 5px'}
                ),
            ], style=content_style_odd
            ),
        ], style={
            'padding': main_panel_padding,
            'background-color': '#ffffff', }
        ),
        # Right Panel
        html.Div(className="col-md-9", children=[
            html.Div(className='row', children=[
                daq.Slider(
                    id='graph-height',
                    min=600, max=1000, value=600, step=50,
                    handleLabel={"showCurrentValue": True, "label": "Height"},
                )
            ], style={'margin': '0px', 'padding': '50px 0px 0px 0px', }
            ),
            html.Div(className='row', children=[
                dcc.Graph(id='bar-plot'),
            ],
            ),
        ], style={
            'padding': main_panel_padding,
            'background-color': '#ffffff', }
        ),
    ]),
])
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


@app.callback(
    Output('select-bar', 'options'),
    [Input('select-variable', 'value'), ]
)
def update_select_bar(variable):
    idx = 0
    for i in df[variable].unique():
        bar_color_saved[i] = default_color[idx % 5]
        idx += 1
    return [{'label': i, 'value': i} for i in df[variable].unique()]


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


@app.callback(
    [Output('treshold-value', 'disabled'),
     Output('treshold-style', 'disabled'), ],
    [Input('show-treshold', 'on'), ]
)
def update_treshold(
    is_tresholdshow
):
    return not is_tresholdshow, not is_tresholdshow


@app.callback(
    Output('bar-plot', 'figure'),
    [
        Input('select-variable', 'value'), Input('select-groupby', 'value'),
        Input('main-title', 'value'), Input('xaxis-title', 'value'),
        Input('yaxis-title', 'value'), Input('show-gridlines', 'on'),
        Input('show-zeroline-x', 'on'), Input('show-zeroline-y', 'on'),
        Input('show-legend', 'on'),
        Input('graph-alignment', 'value'), Input('data-transform', 'value'),
        Input('select-plottype','value'), Input('dtick','value'),
        Input('show-ndata', 'on'),
        Input('show-treshold', 'on'),
        Input('treshold-value', 'value'), Input('treshold-style', 'value'),
        Input('treshold-line-color', 'value'),
        Input('treshold-line-size', 'value'),
        Input('graph-height', 'value'),
        Input('select-bar', 'value'), Input('bar-color', 'value'),
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,
    gridshow, xzeroline, yzeroline, legendshow,
    is_vertical, is_log, plottype,dtick, is_ndatashow,
    is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, graph_height,
    selected_bar, bar_color
):
    # Title and axises label modificator
    if xaxis_title is None:
        xaxis_title = groupby

    if yaxis_title is None:
        yaxis_title = str("Count")

    if main_title is None:
        main_title = str(groupby)

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

    # max_n = 1.1*max_n

    picker_bar_color = 'rgba({}, {}, {})'.format(
        bar_color['rgb']['r'],
        bar_color['rgb']['g'],
        bar_color['rgb']['b'],
        bar_color['rgb']['a'],)
    #ask demas
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
    if(plottype=="Single"):
        print(plottype)
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
                        text =pct,
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
                        text=pct,
                        textposition ="auto",
                    )
                )
                pct =[]
                idx += 1
    elif(plottype== "Stacked_Percentage"):
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
                            text =pct_text,
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
                            text =pct_text,
                            textposition ="auto",
                        )
                    )
                pct =[]
                idx +=1
                pct_idx += 1
                pct_text=[]
            # Counting number of data for each category
            df_shape = df[df[groupby] == i][variable].shape
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


    else:
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
                            text =cnt_text,
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
                            text =cnt_text,
                            textposition ="auto",
                        )
                    )
                idx +=1
                cnt_idx += 1
                cnt = []
                cnt_text=[]


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
    # Returning figure
    return{
        'data': data_list,
        'layout': go.Layout(
            xaxis=go.layout.XAxis(
                title=xaxis_title,
                showgrid=gridshow,
                zeroline=xzeroline,
                type=type_x,
                dtick=dtick if is_vertical else None,
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=gridshow,
                zeroline=yzeroline,
                type=type_y,
                dtick=None if is_vertical else dtick,
            ),
            barmode= "group" if is_side else "stack",
            title=main_title,
            showlegend=legendshow,
            height=graph_height,
            annotations = annots_ndata,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
