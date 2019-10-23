import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import dash_daq as daq
import colorlover as cl
import functions as func

# INITIAL VARIABLES
button_font_size='1.2em'
cardbody_font_size='1em'
cardheader_color='info'
cardbody_color='info'
main_panel_margin={'margin': '10px 0px'}
left_panel_margin={'width': '25%'}
right_panel_margin={'class': 'col-md-8', 'display':'block-inline'}
toggle_switch_color='#91c153'

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)


file_name='Rainier_Weather.csv'



def read_file(filename):
    try:
        if 'csv' in filename:
            dff = pd.read_csv(filename)
        elif ('xls' or 'xlsx') in filename:
            dff = pd.read_excel(filename)
    except Exception as e:
        print (e)
        return u'There was an error opening {}'.format(filename)
    return dff


df = read_file(file_name)

# Data without date and time
names = df.select_dtypes(exclude='number').columns.values

# Date and time in list xnames
datetime = []
for col in names:
    if 'date' in col.lower():
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        datetime = df[col]

# Other data in ynames
ynames = df.select_dtypes(include='number').columns.values

# Six defferent line styles to choose from
linestyle_list = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']

# Features that are Categorical
cat_features = df.select_dtypes(include = 'object').columns.values

# Users can choose lines only, lines and markers and lines, markers and text
LABELSTYLE_DICT = [
    {'label': 'Lines', 'value': 'lines'},
    {'label': 'Lines & Markers', 'value': 'lines+markers'},
    {'label': 'Lines, Markers & Text', 'value': 'lines+markers+text'}
]

# Marker styles users can choose from
MARKERS_DICT = [
    {'value': 'circle', 'label': 'Circle'},
    {'value': 'square', 'label': 'Square'},
    {'value': 'diamond', 'label': 'Diamond'},
    {'value': 'cross', 'label': 'Cross'},
    {'value': 'x', 'label': 'X'},
    {'value': 'triangle-up', 'label': 'Triangle-up'},
    {'value': 'pentagon', 'label': 'pentagon'},
    {'value': 'hexagon', 'label': 'hexagon'},
    {'value': 'hexagon2', 'label': 'hexagon2'},
    {'value': 'octagon', 'label': 'octagon'},
    {'value': 'star', 'label': 'star'},
    {'value': 'hexagram', 'label': 'hexagram'},
    {'value': 'star-triangle-up', 'label': 'star-triangle-up'},
    {'value': 'hourglass', 'label': 'hourglass'},
    {'value': 'bowtie', 'label': 'bowtie'},
]

marker_dict = {}
linestyle_dict = {}
gap_dict = {}
label_dict = {}
LINECOLOR_DICT = {}
linefill = {}
default_color = cl.to_rgb(cl.scales['5']['qual']['Set1'])
default_alpha = 0.65

toggle_switch_color = '#91c153'

col_idx = 0
for i in default_color:
    start_idx = i.find('(')
    i = i[start_idx+1:len(i)-1]
    i = i.split(",")
    i = 'rgba({},{},{},{})'.format(i[0], i[1], i[2], default_alpha)
    default_color[col_idx] = i
    col_idx += 1


app.layout = html.Div(className='row', children=[
    html.Div(children=[
        html.Div(className='container', children=[
            html.Div(className='accordion', children=[
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Select Data", id='line-group-1-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6('Choose Variables to see over time')),
                                dbc.CardBody(children=func.render_dropdown_valued_multi('select-variables', ynames, ynames[0]))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('use-group-by', 'Group Lines By Category?', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Select Group By')),
                                dbc.CardBody(children=func.render_dropdown_valued('line-select-groupby', cat_features, cat_features[0]))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='line-collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Plot Setting", id='line-group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('line-show-gridlines', 'Show Grid Lines', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('line-show-zeroline-y', 'Show Y Zero Line', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([ 
                                dbc.CardHeader(html.H6('Y Delta Ticks')),
                                dbc.CardBody(children=func.render_input_number_min('line-Y-dtick', 'Delta Ticks', 0))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ), 
                        ]),
                        id='line-collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Statistic Information", id='line-group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Data Transformation')),
                                dbc.CardBody(children=func.render_toggleswitch('line-data-transform', ['Linear', 'Logarithmic'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            )
                        ]),
                        id='line-collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ), # <== TO HERE
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Line Setting", id='line-group-4-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6('Select Category')),
                                dbc.CardBody(children=func.render_dropdown_blank('line-select-group'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('ALF', 'Line Fill', False))
                            ], style={'margin': '0px 0px 10px 0px'},className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardBody(children=func.render_booleanswitch('show-gaps', 'Show Gaps', False))
                            ], style={'margin': '0px 0px 10px 0px'},className='col-md-6',
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Line Style')),
                                dbc.CardBody(children=func.render_dropdown_format('line-style', linestyle_list))
                            ], style={'margin': '0px 0px 10px 0px'},className='col-md-6'
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Marker Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('line-alignment-markers-dropdown', MARKERS_DICT, 'circle'))
                            ], style={'margin': '0px 0px 10px 0px'},className='col-md-6'
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Label Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('line-alignment-labelstyle-dropdown', LABELSTYLE_DICT, 'lines'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Line Color')),
                                dbc.CardBody(children=func.render_colorpicker_small('line-colorpicker', '#FFFFFF', 0, 0, 255, 1))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='line-collapse-4'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader(
                        dbc.Button("Graph Setting", id='line-group-5-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Height')),
                                dbc.CardBody(children=func.render_slider('line-graph-height', 600, 1200, 600, 50, [600, 700, 800, 900, 1000, 1100, 1200]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H5('Graph Width')),
                                dbc.CardBody(children=func.render_slider('line-graph-width', 800, 1400, 800, 50, [800, 900, 1000, 1100, 1200, 1300, 1400]), style={'padding':'5% 5% 10% 5%'})
                            ], style={'width': '100%'}
                            ),
                            dbc.Card([ 
                                dbc.CardHeader(html.H6('Opacity')),
                                dbc.CardBody(children=func.render_slider('line-opacity-slider', 0, 100, 85, 1, []))
                            ], style={'width' : '100%'}
                            ), 
                        ]),
                        id='line-collapse-5'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='line-graphic',
                style={'width' : '90%', 'padding-left' : '3%'},
                config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'legendPosition' : True, 'legendText' : True, 'colorbarPosition' : True, 'colorbarTitleText' : True}}
            ),
        ])
    ], className='col-md-9'
    ),
], style=main_panel_margin)


# Accordion Toggle Callback
@app.callback(
    [Output(f'line-collapse-{i}', 'is_open') for i in range(1,6)],
    [Input(f'line-group-{i}-toggle', 'n_clicks') for i in range(1,6)],
    [State(f'line-collapse-{i}', 'is_open') for i in range(1,6)]
)
def toggle_accordion(n1, n2, n3, n4, n5, is_open1, is_open2, is_open3, is_open4, is_open5):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'line-group-1-toggle' and n1:
        return not is_open1, False, False, False, False
    elif button_id ==  'line-group-2-toggle' and n2:
        return False, not is_open2, False, False, False
    elif button_id ==  'line-group-3-toggle' and n3:
        return False, False, not is_open3, False, False
    elif button_id ==  'line-group-4-toggle' and n4:
        return False, False, False, not is_open4, False
    elif button_id ==  'line-group-5-toggle' and n5:
        return False, False, False, False, not is_open5
    return False, False, False, False, False

@app.callback(
    Output('line-colorpicker', 'value'),
    [Input('line-select-group', 'value'),]
)
def update_line(select_group):
    temp_str = LINECOLOR_DICT.get(select_group, dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb = dict(r = temp_str[0], g = temp_str[1], b = temp_str[2], a = temp_str[3]))
    return temp_str


@app.callback(
    [Output('line-select-group', 'options'),
    Output('line-select-groupby', 'disabled')],
    [Input('line-select-groupby', 'value'),
    Input('use-group-by', 'on'),
    Input('select-variables', 'value')]
)
def update_group(groupby, usegroup, selected):
    idx = 0
    if usegroup:
        groups = []
        for s in selected:
            for i in df[groupby].unique():
                LINECOLOR_DICT[s + ' : '+ i] = default_color[idx % 5]
                marker_dict[s + ' : '+ i] = MARKERS_DICT[idx % 5]['value']
                linestyle_dict[s + ' : '+ i] = linestyle_list[idx % 6].replace(' ', '').lower()
                gap_dict[s + ' : '+ i] = True
                label_dict[s + ' : '+ i] = LABELSTYLE_DICT[0]['value']
                linefill[s + ' : '+ i] = False
                idx += 1
                groups.append(s + ' : '+ i)
            return [{'label': i, 'value': i} for i in groups], False
    else:
        for i in selected:
            LINECOLOR_DICT[i] = default_color[idx % 5]
            marker_dict[i] = MARKERS_DICT[idx % 5]['value']
            linestyle_dict[i] = linestyle_list[idx % 6].replace(' ', '').lower()
            gap_dict[i] = True
            label_dict[i] = LABELSTYLE_DICT[0]['value']
            linefill[i] = False
            idx += 1
        return [{'label': i, 'value': i} for i in selected], True


# Main callback
@app.callback(
    Output('line-graphic', 'figure'),
    [Input('select-variables', 'value'),
     Input('line-data-transform', 'value'),
     Input('line-show-gridlines', 'on'),
     Input('line-show-zeroline-y', 'on'),
     Input('line-alignment-markers-dropdown', 'value'),
     Input('line-alignment-labelstyle-dropdown', 'value'),
     Input('show-gaps', 'on'),
     Input('ALF', 'on'),
     Input('line-opacity-slider', 'value'),
     Input('line-colorpicker', 'value'),
     Input('line-style', 'value'),
     Input('line-select-groupby', 'value'),
     Input('line-Y-dtick', 'value'),
     Input('line-select-group', 'value'),
     Input('use-group-by', 'on'),
     Input('line-graph-width', 'value'),
     Input('line-graph-height', 'value')
     ])
def update_graph(select_variables, data_transform,
                 show_gridlines, show_zeroline_y,
                 alignment_markers_dropdown, alignment_labelstyle_dropdown,
                 show_gaps, ALF, OS, colorPicker, line_style,
                 groupby, y_dtick, select_group, use_group_by,
                 width, height
                 ):
    if use_group_by == True:

        group_list = df[groupby].unique()
        type_y = None
        if data_transform:
            type_y = 'log'

        picker_line_color = 'rgba({}, {}, {}, {})'.format(
            colorPicker['rgb']['r'],
            colorPicker['rgb']['g'],
            colorPicker['rgb']['b'],
            colorPicker['rgb']['a'])

        traces_list = []
        for variable in select_variables:
            for selection in group_list:
                reference = variable + ' : '+ selection
                if reference == select_group:
                    LINECOLOR_DICT[reference] = picker_line_color
                    marker_dict[reference] = alignment_markers_dropdown
                    linestyle_dict[reference] = line_style
                    gap_dict[reference] = show_gaps
                    label_dict[reference] = alignment_labelstyle_dropdown
                    linefill[reference] = ALF
                traces_list.append(
                    go.Scatter(
                        x=datetime,
                        y=df[df[groupby] == selection][variable],
                        text=df[df[groupby] == selection][variable],
                        mode=label_dict[reference],
                        name=reference,
                        connectgaps = gap_dict[reference],
                        fill = "toself" if linefill[reference] else "none",
                        opacity = OS/100,
                        marker = dict(
                            size = 8,
                            opacity = 0.8,
                            symbol = marker_dict[reference]
                        ),
                        line = dict(color=LINECOLOR_DICT[reference], width=3, dash=linestyle_dict[reference])
                    )
                )    
        return {
            'data': traces_list,
            'layout': go.Layout(
                xaxis={
                    'title' : 'Time',
                    'showgrid': show_gridlines,
                    'rangeslider': {'visible': True}, 'type': 'date'
                },
                yaxis={
                    'title' : ', '.join(select_variables),
                    'type' : type_y,
                    'showgrid': show_gridlines,
                    'zeroline': show_zeroline_y,
                    'dtick': y_dtick
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                title= "Time-Series-Edit Me Last",
                hovermode='closest',
                height=height,
                width=width,
            )
        }

    else:
        type_y = None
        if data_transform:
            type_y = 'log'

        yaxis_list = ynames

        picker_line_color = 'rgba({}, {}, {}, {})'.format(
            colorPicker['rgb']['r'],
            colorPicker['rgb']['g'],
            colorPicker['rgb']['b'],
            colorPicker['rgb']['a'])

        Fill = "none"
        if ALF:
            Fill = "toself"

        traces_list = []
        for variable in select_variables:
            if select_group is not None:
                if variable == select_group:
                    LINECOLOR_DICT[variable] = picker_line_color
                    marker_dict[variable] = alignment_markers_dropdown
                    linestyle_dict[variable] = line_style
                    gap_dict[variable] = show_gaps
                    label_dict[variable] = alignment_labelstyle_dropdown
                    linefill[variable] = ALF
            traces_list.append(
                go.Scatter(
                    x=datetime,
                    y=df[variable],
                    text=df[variable],
                    mode=label_dict[variable],
                    name=str(variable).replace('[', '').replace(']', '').replace("\'", ""),
                    connectgaps = gap_dict[variable],
                    fill = "toself" if linefill[variable] else "none",
                    opacity = OS/100,
                    marker = dict(
                        size = 8,
                        opacity = 0.8,
                        symbol = marker_dict[variable]
                    ),
                    line = dict(color=LINECOLOR_DICT[variable], width=3, dash=linestyle_dict[variable])
                    )
                )

        return {
            'data': traces_list,
            'layout': go.Layout(
                xaxis={
                    'title' : 'Time',
                    'showgrid': show_gridlines,
                    'rangeslider': {'visible': True}, 
                    'type': 'date'
                },
                yaxis={
                    'title' : ', '.join(select_variables),
                    'type' : type_y,
                    'showgrid': show_gridlines,
                    'zeroline': show_zeroline_y,
                    'dtick': y_dtick
                },
                margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
                title= "Time-Series-Edit Me Last",
                hovermode='closest',
                height=height,
                width=width,
            )
        }   

if __name__ == '__main__':
    app.run_server(debug=True)
