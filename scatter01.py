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
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], 1)
    default_color[col_idx] = i
    col_idx += 1

marker_symbols = ['Circle', 'Square', 'Diamond', 'Cross', 'X', 'Triangle-Up', 'Pentagon', 'Hexagon', 'Star']
selected_subgroup_color = {}
selected_subgroup_marker = {}

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


file_name=r'E:\Users\demas\project5206\UWA_acid_base_table.xlsx'

df = pd.read_excel(file_name)

cnames = df.select_dtypes(include='number').columns.values

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
                            ],
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_radio_valued('xaxis-type', options=['Linear', 'Log'], value='Linear' ))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Axis Value')),
                                dbc.CardBody(children=func.render_dropdown_valued('yaxis-column', options=cnames, value=cnames[-1] ))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_radio_valued('yaxis-type', options=['Linear', 'Log'], value='Linear' ))
                            ], style={'height': '20em'}
                            ),
                        ],
                        ), id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size, }
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Plot Setting', id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Swap Axis')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('swap', False))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Grid Lines')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('GL', True))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Zero Lines')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('OL', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Label')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LB', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Legend')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LD', True))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Colorscale Legend')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('LS', True))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Change Colorscale')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-colorscale-dropdown', COLORSCALES_DICT, 'Greys'))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Opacity')),
                                dbc.CardBody(children=func.render_slider('opacity-slider', 0, 100, 70, 1, []))
                            ]
                            ),
                        ],
                        ), id='collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Customised Lines', id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Axis Threshold')),
                                dbc.CardBody(children=func.render_input_number('X-thredshold', 'X Axis Threshold'))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Axis Threshold')),
                                dbc.CardBody(children=func.render_input_number('Y-thredshold', 'Y Axis Threshold'))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Linear Best Fit Line')),
                                dbc.CardBody(children=func.render_booleanswitch_nolab('linear', False))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Best Fit Line Style')),
                                dbc.CardBody(children=func.render_dropdown_dict('change-dash', DASH_DICT))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Tick Distance')),
                                dbc.CardBody(children=func.render_input_number_min('X-dtick', 'X Axis Delta Tick', 0))
                            ]
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Tick Distance')),
                                dbc.CardBody(children=func.render_input_number_min('Y-dtick', 'Y Axis Delta Tick', 0))
                            ]
                            ),
                        ],
                        ), id='collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size}
                ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button('Plot Style', id='group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True, )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Color and Hover Text Group')),
                                dbc.CardBody(children=func.render_dropdown_valued('color-drop', df.columns, df.columns[0]))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Select Sub-group')),
                                dbc.CardBody(children=func.render_dropdown_blank('selected-groupby'))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Sub-group Marker Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-markers-dropdown', MARKERS_DICT, 'circle'))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Sub-group Color')),
                                dbc.CardBody(children=func.render_colorpicker('my-color-picker', '#ffffff', 22, 222, 160, 1))
                            ],
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Title')),
                                dbc.CardBody(children=func.render_input('title', 'Title'))
                            ], style={'display': 'none'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('X Axis Label')),
                                dbc.CardBody(children=func.render_input('x_label', 'X Axis label'))
                            ], style={'display': 'none'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Y Axis Label')),
                                dbc.CardBody(children=func.render_input('y_label', 'Y Axis label'))
                            ], style={'display': 'none'}
                            ),
                        ],
                        ), id='collapse-4'
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
                    config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'titleText': True}},
            ),
        ],
        ),
    ], className='col-md-9'),
], )

# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,5)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,5)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,5)]
)
def toggle_accordion(n1, n2, n3, n4, is_open1, is_open2, is_open3, is_open4):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False, False
    elif button_id ==  'group-2-toggle' and n2:
        return False, not is_open2, False, False
    elif button_id ==  'group-3-toggle' and n3:
        return False, False, not is_open3, False
    elif button_id ==  'group-4-toggle' and n4:
        return False, False, False, not is_open4
    return False, False, False, False

@app.callback(
    [Output('selected-groupby', 'options'),
    Output('alignment-colorscale-dropdown', 'disabled'),
    Output('my-color-picker','disabled'),
    Output('LS', 'disabled')
    ],
    [Input('color-drop', 'value'),]
    )
def traces_groupby(color_drop):
    if df[color_drop].dtypes =='object':
        idx = 0
        selected_subgroup_color.clear()
        selected_subgroup_marker.clear()
        for i in df[color_drop].unique():
            selected_subgroup_color[i] = default_color[idx % num_of_color]
            selected_subgroup_marker[i] = marker_symbols[idx % 9]
            idx += 1
        return [{'label': i, 'value': i} for i in df[color_drop].unique()], True, False, True
    else:
        return [{'label': color_drop, 'value': color_drop}], False, True, False

@app.callback(
    Output('my-color-picker', 'value'),
    [
     Input('selected-groupby', 'value')
    ]
)
def update_color_picker(sub_group):
    if sub_group is None:
        return dict(rgb=dict(r=222, g=110, b=75, a=1))
    else:
        temp_str = selected_subgroup_color.get(sub_group, 'rgb(222,110,75,1)')
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb=dict(r=temp_str[0], g=temp_str[1], b=temp_str[2], a=temp_str[3]))
        return temp_str


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
    Output('x_label', 'value'),
    [Input('xaxis-column', 'value')])
def set_xaxis_column(X_c):
    return X_c

@app.callback(
    Output('y_label', 'value'),
    [Input('yaxis-column', 'value')])
def set_yaxis_column(Y_c):
    return Y_c

@app.callback(
    Output('title', 'value'),
    [
    Input('xaxis-column', 'value'),
    Input('yaxis-column', 'value'),
    ])
def set_title(X_c, Y_c):
    return "{} vs {}".format(X_c, Y_c)

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('title', 'value'),
     Input('alignment-colorscale-dropdown', 'value'),
     Input('swap', 'on'),
     Input('linear', 'on'),
     Input('x_label', 'value'),
     Input('y_label', 'value'),
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
     Input('change-dash', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 title_1, alignment_colorscale_dropdown,
                 swap, linear, x_label, y_label, GL, OL,
                 alignment_markers_dropdown, color_var, LD, OS, X_D, Y_D, X_T, Y_T, G_t, C_P, LB, LS, CD):

    if swap:
        # Swapping the x and y axes names and values
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp
        tmp1 = x_label
        x_label = y_label
        y_label = tmp1

    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    slope=np.around(slope, decimals=2)
    intercept=np.around(intercept, decimals=2)
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

    traces = []
    #if the data type of the group by column is object, it will show each different values with different colors
    if df[color_var].dtypes=='object':
        for i in df[color_var].unique():
            df_by = df[df[color_var] == i]
            print(C_P)
            if i == G_t:
                selected_subgroup_color[i]='rgba({}, {}, {}, {})'.format(C_P['rgb']['r'], C_P['rgb']['g'], C_P['rgb']['b'], C_P['rgb']['a'])
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
                    'color': selected_subgroup_color[i],
                    #'color': 'rgba({}, {}, {}, {})'.format(C_P['rgb']['r'], C_P['rgb']['g'], C_P['rgb']['b'], C_P['rgb']['a']),
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
                        'color': selected_subgroup_color[i],
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
                color = df[xaxis_column_name],
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
        name='Y = {}*X + {}'.format(slope, intercept),
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
            'title': x_label,
            'type': 'linear' if xaxis_type == 'Linear' else 'log',
            'showgrid': GL,
            'zeroline': OL,
            'dtick': X_D
        },
        yaxis={
            'title': y_label,
            'type': 'linear' if yaxis_type == 'Linear' else 'log',
            'showgrid': GL,
            'zeroline': OL,
            'dtick': Y_D
        },
        title= title_1,
        showlegend = LD,
        shapes=threshold_shape,
        hovermode='closest',
        legend=(dict(x=1.15, y=0.9) if LS else dict(x=1, y=1)) if LD else None,
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
