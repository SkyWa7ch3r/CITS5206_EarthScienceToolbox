# Importing Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash_daq as daq
from dash.dependencies import Input, Output


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

# Init Dash App
app = dash.Dash(__name__)

label_background_color = '#67acb7'
content_background_color = '#c0fdfb'
border_color = '#868686'
main_panel_padding = '10px 25px'
label_padding = '10px 10px 0px 10px'
toggle_switch_color = '#91c153'

line_style = ['solid', 'dash', 'dot', 'longdash', 'dashdot', 'longdashdot']

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
                        label=['Horizontal', 'Vertical'],
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
                        label='N Data',
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
                                label='Treshold',
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
                            options=[{'label': i, 'value': i} for i in line_style],
                            value=str(line_style[0]),
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
                        label='Treshold Color',
                        style={'background-color': 'white'},
                        value=dict(rgb=dict(r=0, g=0, b=255, a=1))
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
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,
    gridshow, xzeroline, yzeroline, legendshow,
    datapointsshow, is_vertical, is_log, outliersshow, is_ndatashow,
    is_percentileshow, is_meanshow, is_sdshow, is_tresholdshow, treshold_value,
    treshold_style, treshold_color, treshold_size, is_statshow, graph_height
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
    percentile_5 = []
    percentile_10 = []
    percentile_90 = []
    percentile_95 = []
    annots_ndata = []
    annots_mean = []
    annots_median = []
    annots_idx = 0

    # Computing N Data
    max_n = df[variable].max()
    max_n = np.log(max_n/10) if is_log else 1.1*max_n
    # Generate boxplot
    for i in group_list:
        if (not is_vertical):
            data_list.append(
                go.Box(
                    y=df[df[groupby] == i][variable],
                    name=i,
                    boxpoints=showpoints,
                    boxmean='sd' if is_sdshow else None,
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
                )
            )

        # Counting percentiles
        percentile_5.append(np.percentile((df[df[groupby] == i][variable]), 5))
        percentile_10.append(np.percentile((df[df[groupby] == i][variable]), 10))
        percentile_90.append(np.percentile((df[df[groupby] == i][variable]), 90))
        percentile_95.append(np.percentile((df[df[groupby] == i][variable]), 95))

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
            text='N = {}'.format(n_data[annots_idx]),
            showarrow=False,
            )
        )

        # Generating annotations of mean
        annots_mean.append(go.layout.Annotation(
            x=data_mean[annots_idx] if is_vertical else annots_idx,
            y=annots_idx if is_vertical else data_mean[annots_idx],
            xref='x',
            yref='y',
            text='Mean: {}'.format(data_mean[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (100/len(group_list))*5,
            ay=(100/len(group_list))*2 if is_vertical else 0,
            arrowhead=6,
        ))

        # Generating annotations of mean
        annots_median.append(go.layout.Annotation(
            x=data_median[annots_idx] if is_vertical else annots_idx,
            y=annots_idx if is_vertical else data_median[annots_idx],
            xref='x',
            yref='y',
            text='Med: {}'.format(data_median[annots_idx]),
            showarrow=True,
            ax=0 if is_vertical else (-100/len(group_list))*4,
            ay=(-100/len(group_list))*2 if is_vertical else 0,
            arrowhead=7,
        ))

        annots_idx = annots_idx + 1

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

    if (not is_ndatashow):
        annots_ndata = []

    if (not is_statshow):
        annots_mean = []
        annots_median = []

    annots_ndata = annots_ndata + annots_mean + annots_median

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
