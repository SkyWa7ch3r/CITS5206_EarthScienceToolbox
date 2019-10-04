
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
app.config.suppress_callback_exceptions = True

label_background_color = '#67acb7'
content_background_color = '#c0fdfb'
border_color = '#868686'
main_panel_padding = '10px 25px'
label_padding = '10px 10px 0px 10px'
toggle_switch_color = '#91c153'

box_color_saved = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])

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
                        dcc.Checklist(
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
    Output('bar-plot', 'figure'),
    [
        Input('select-variable', 'value'), Input('select-groupby', 'value'),
        Input('main-title', 'value'), Input('xaxis-title', 'value'),
        Input('yaxis-title', 'value'), Input('show-gridlines', 'on'),
        Input('show-zeroline-x', 'on'), Input('show-zeroline-y', 'on'),
        Input('show-legend', 'on'), Input('show-percentiles', 'on'),
        Input('graph-alignment', 'value'), Input('data-transform', 'value')
    ]
)
def update_figure(
    variable, groupby, main_title, xaxis_title, yaxis_title,
    gridshow, xzeroline, yzeroline, legendshow,
    datapointsshow, is_vertical, is_log
):
    # Title and axises label modificator
    if xaxis_title is None:
        xaxis_title = groupby

    if yaxis_title is None:
        yaxis_title = str("Count")

    if main_title is None:
        main_title = str(groupby)

    # Initialising data list
    group_list = df[groupby].unique()
    data_list = []
    pct = []

    # Generate barplot
    for i in group_list:
        pct.append(df[df[groupby]==i][groupby].count()),
        if (not is_vertical):
            data_list.append(
                go.Bar(
                    x=pct,
                    y=group_list,
                    name=i,
                    orientation='h',
                    text =pct,
                    textposition ="auto",
                    legendgroup= i         
                )
            )
            pct =[]    
        else:
            data_list.append(
                go.Bar(
                    x=group_list,
                    y=pct,
                    name=i,
                    text=pct,
                    textposition ="auto",
                    legendgroup= i
                )
            ) 
            pct =[]  
      
    # Returning figure
    return{
        'data': data_list,
        'layout': go.Layout(
            xaxis=go.layout.XAxis(
                title=xaxis_title,
                showgrid=gridshow,
                zeroline=xzeroline,
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=gridshow,
                zeroline=yzeroline,
            ),
          #  barmode=,
            title=main_title,
            showlegend=legendshow,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
