# Importing Libraries
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
cat_features = df.select_dtypes(exclude='number').columns.values

# Init Dash App
app = dash.Dash(__name__)

label_background_color = '#67acb7'
content_background_color = '#c0fdfb'
border_color = '#868686'
main_panel_padding = '10px 25px'
label_padding = '10px 10px 0px 10px'
toggle_switch_color = '#91c153'

default_alpha = 0.65
box_color_saved = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])

col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
    col_idx += 1

line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']

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
                            options=[{'label': i, 'value': i} for i in features],
                            value=str(features[0])
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
                        label=['Vertical', 'Horizontal'],
                        value=False,
                        size='35',
                        color=toggle_switch_color, ),
                ], style={
                    'padding': '10px 10px 5px 10px',
                    'text-align': 'center'}
                ),
            ], style=content_style_odd
            ),
            # Data Points and Outliers
            html.Div(className='row', children=[
                html.Div(className='col-md-6', children=[
                    html.H5('Data Points and Outliers')
                ], style=content_style_dropdown_inline
                ),
                # Outliers Configuration
                html.Div(className='col-md-6', children=[
                    dcc.Dropdown(
                        id='select-outliers',
                        options=[
                            {'label': 'Default', 'value': 'outliers'},
                            {'label': 'Only Wiskers', 'value': 'False'},
                            {'label': 'Suspected Outliers', 'value': 'suspectedoutliers'},
                            {'label': 'All Points', 'value': 'all'},
                        ],
                        value='outliers',
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
                html.Div(className='col-md-4', children=[
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
                html.Div(className='col-md-4', children=[
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
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-percentiles',
                        on=False,
                        # size='35',
                        label='Percentiles',
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
            # Show/hide Mean, SD
            html.Div(className='row', children=[
                # Show/hide Mean
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-mean',
                        on=False,
                        # size='35',
                        label='Mean',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
                # Show/hide SD
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-sd',
                        on=False,
                        # size='35',
                        label='Std. Dev.',
                        labelPosition='top',
                        color=toggle_switch_color,
                        style={
                            'padding': '10px',
                        }
                    ),
                ], style=content_style_odd
                ),
                # Show/hide Not Implement yet
                html.Div(className='col-md-4', children=[
                    daq.BooleanSwitch(
                        id='show-stats',
                        on=False,
                        # size='35',
                        label='Stats',
                        labelPosition='top',
                        color=toggle_switch_color,
                        # disabled=True,
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
                        html.H5('Select Box')
                    ],
                    ),
                    html.Div(className='row', children=[
                        dcc.RadioItems(
                            id='select-box',
                        )
                    ],
                    ),
                ],
                ),
                html.Div(className='col-md-8', children=[
                    daq.ColorPicker(
                        id='box-color',
                        label='Box Marker Color',
                        style={'background-color': 'white'},
                        value=dict(rgb=dict(r=222, g=110, b=75, a=default_alpha))
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
            ], style={'margin': '10px', 'padding': '50px 0px 0px 0px', }
            ),
            html.Div(className='row', children=[
                dcc.Graph(id='box-plot'),
            ],
            ),
        ], style={
            'padding': main_panel_padding,
            'background-color': '#ffffff', }
        ),
    ]),
])


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
    Output('show-stats', 'on'),
    [Input('select-outliers', 'value'), ]
)
def update_showstat(outliersshow):
    return False if outliersshow == 'all' else None


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
        Input('select-box', 'value'), Input('box-color', 'value'),
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,
    gridshow, xzeroline, yzeroline, legendshow,
    datapointsshow, is_vertical, is_log, outliersshow, is_ndatashow,
    is_percentileshow, is_meanshow, is_sdshow, is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, is_statshow, graph_height,
    selected_box, box_color
):
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
            print('selected_box : {}'.format(selected_box))
            print('box color 1 : {}'.format(box_color_saved))
            if i == selected_box:
                box_color_saved[i] = picker_box_color
                print('box color 2 : {}'.format(box_color_saved))
            # else:
            #    box_color_saved[i] = default_color[color_idx % 5]
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
        percentile_25.append(np.percentile((df[df[groupby] == i][variable]), 25))
        percentile_75.append(np.percentile((df[df[groupby] == i][variable]), 75))
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
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=gridshow,
                zeroline=yzeroline,
                type=type_y,
            ),
            title=main_title,
            showlegend=legendshow,
            height=graph_height,
            annotations=annots_ndata,
            shapes=treshold_shape,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
