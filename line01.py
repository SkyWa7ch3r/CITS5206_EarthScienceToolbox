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
xnames = []
for col in names:
    if 'date' in col.lower() or 'time' in col.lower():
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
        xnames.append(col)

# Other data in ynames
ynames = df.select_dtypes(include='number').columns.values

# Six defferent line styles to choose from
line_style = ['Solid', 'Dash', 'Dot', 'Long Dash', 'Dash Dot', 'Long Dash Dot']

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
    {'value': 'circle', 'label': 'circle'},
    {'value': 'square', 'label': 'square'},
    {'value': 'diamond', 'label': 'diamond'},
    {'value': 'cross', 'label': 'cross'},
    {'value': 'x', 'label': 'x'},
    {'value': 'triangle-up', 'label': 'triangle-up'},
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

#
LINECOLOR_DICT = {}
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
                        dbc.Button("Select Data", id='group-1-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6('X Axis Value')),
                                dbc.CardBody(children=func.render_dropdown_valued('xaxis-column', xnames, xnames[0]))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Y Axis Value')),
                                dbc.CardBody(children=func.render_dropdown_valued_multi('select-variables', ynames, ynames[0]))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Group By')),
                                dbc.CardBody(children=func.render_dropdown_valued('select-groupby', cat_features, str(cat_features[0])))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Data Transformation')),
                                dbc.CardBody(children=func.render_toggleswitch('data-transform', ['Linear', 'Logarithmic'], False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                        ]),
                        id='collapse-1'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ),
                dbc.Card([
                    dbc.CardHeader( # <== COPY BIG CARD FROM HERE
                        dbc.Button("Plot Setting", id='group-2-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6('Gaps')),
                                dbc.CardBody(children=func.render_booleanswitch('show-gaps', 'Show', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Line Fill')),
                                dbc.CardBody(children=func.render_booleanswitch('ALF', 'Show', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Grid Lines')),
                                dbc.CardBody(children=func.render_booleanswitch('show-gridlines', 'Show', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Y Zero Line')),
                                dbc.CardBody(children=func.render_booleanswitch('show-zeroline-y', 'Show', False))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([ # <-- copy from here
                                dbc.CardHeader(html.H6('Opacity')),
                                dbc.CardBody(children=func.render_slider('opacity-slider', 0, 100, 85, 1, []))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ), # <-- to here
                            dbc.Card([ # <-- copy card from here
                                dbc.CardHeader(html.H6('Y Delta Ticks')),
                                dbc.CardBody(children=func.render_input_number_min('Y-dtick', 'Delta Ticks', 0))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ), # <-- to here
                        ]),
                        id='collapse-2'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ), # <== TO HERE
                dbc.Card([ # <== COPY BIG CARD FROM HERE
                    dbc.CardHeader(
                        dbc.Button("Line Setting", id='group-3-toggle', color=cardheader_color, style={'font-size': button_font_size}, block=True,
                        )
                    ),
                    dbc.Collapse(
                        dbc.CardBody(children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6('Select Group')),
                                dbc.CardBody(children=func.render_radio_blank('select-group'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Color')),
                                dbc.CardBody(children=func.render_colorpicker('colorpicker', '#FFFFFF', 0, 0, 255, 1))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Line Style')),
                                dbc.CardBody(children=func.render_dropdown_format_valued('line-style', line_style))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([
                                dbc.CardHeader(html.H6('Marker Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-markers-dropdown', MARKERS_DICT, 'circle'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ),
                            dbc.Card([ # <-- copy from here
                                dbc.CardHeader(html.H6('Label Style')),
                                dbc.CardBody(children=func.render_dropdown_dict_valued('alignment-labelstyle-dropdown', LABELSTYLE_DICT, 'lines'))
                            ], style={'margin': '0px 0px 10px 0px'}
                            ), # <-- to here
                        ]),
                        id='collapse-3'
                    ),
                ], color=cardbody_color, outline=True, style={'font-size': cardbody_font_size} ), # <== TO HERE
            ])
        ])
    ], className='col-md-3'
    ),
    html.Div(children=[
        dbc.Row(children=[
            dcc.Graph(id='indicator-graphic',
                style={'width' : '90%', 'padding-left' : '3%'},
                config={'editable' : True, 'toImageButtonOptions': {'scale' : 10},'edits' : {'legendPosition' : True, 'legendText' : True, 'colorbarPosition' : True, 'colorbarTitleText' : True}}
            ),
        ])
    ], className='col-md-9', style={'width' : '90%'},
    ),
], style=main_panel_margin)


# Accordion Toggle Callback
@app.callback(
    [Output(f'collapse-{i}', 'is_open') for i in range(1,4)],
    [Input(f'group-{i}-toggle', 'n_clicks') for i in range(1,4)],
    [State(f'collapse-{i}', 'is_open') for i in range(1,4)]
)
def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return ""
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id ==  'group-1-toggle' and n1:
        return not is_open1, False, False
    elif button_id ==  'group-2-toggle' and n2:
        return False, not is_open2, False
    elif button_id ==  'group-3-toggle' and n3:
        return False, False, not is_open3
    return False, False, False

@app.callback(
    Output('colorpicker', 'value'),
    [Input('select-group', 'value')]
)
def update_line_color(yaxis):
    temp_str = LINECOLOR_DICT.get(yaxis, dict(rgb = dict(r = 222, g = 110, b = 75, a = default_alpha)))
    if isinstance(temp_str, str):
        start_idx = temp_str.find('(')
        temp_str = temp_str[start_idx+1:len(temp_str)-1]
        temp_str = temp_str.split(",")
        temp_str = dict(rgb = dict(r = temp_str[0], g = temp_str[1], b = temp_str[2], a = temp_str[3]))
    return temp_str


@app.callback(
    Output('select-group', 'options'),
    [Input('select-groupby', 'value')]
)
def update_group(groupby):
    idx = 0
    for i in df[groupby].unique():
        LINECOLOR_DICT[i] = default_color[idx % 5]
        idx += 1
    return [{'label': i, 'value': i} for i in df[groupby].unique()]


# Main callback
@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('select-variables', 'value'),
     Input('data-transform', 'value'),
     Input('show-gridlines', 'on'),
     Input('show-zeroline-y', 'on'),
     Input('alignment-markers-dropdown', 'value'),
     Input('alignment-labelstyle-dropdown', 'value'),
     Input('show-gaps', 'on'),
     Input('ALF', 'on'),
     Input('opacity-slider', 'value'),
     Input('colorpicker', 'value'),
     Input('line-style', 'value'),
     Input('select-groupby', 'value'),
     Input('Y-dtick', 'value'),
     Input('select-group', 'value')
     ])
def update_graph(xaxis_column_name, select_variables,
                 data_transform,
                 show_gridlines, show_zeroline_y,
                 alignment_markers_dropdown,
                 alignment_labelstyle_dropdown, show_gaps, ALF,
                 OS,
                 colorPicker,
                 line_style,
                 groupby,
                 y_dtick,
                 select_group
                 ):
    group_list = df[groupby].unique()

    type_y = None
    if data_transform:
        type_y = 'log'

    yaxis_list = ynames

    picker_line_color = 'rgba({}, {}, {}, {})'.format(
        colorPicker['rgb']['r'],
        colorPicker['rgb']['g'],
        colorPicker['rgb']['b'],
        colorPicker['rgb']['a'])

    color_idx = 0
    for i in group_list:
        if select_group is not None:
            if i == select_group:
                LINECOLOR_DICT[i] = picker_line_color
            # else:
            #    box_color_saved[i] = default_color[color_idx % 5]
        color_idx += 1

    # Variable to change gaps
    ConnectGaps = True
    if show_gaps:
         ConnectGaps = False

    # Variable to change line fill
    Fill = "none"
    if ALF:
        Fill = "toself"

    # Variables for label styles
    lineStyle = dict()
    markerOnly = dict()
    if alignment_labelstyle_dropdown == 'lines':
        markerOnly = None
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)
    elif alignment_labelstyle_dropdown == 'lines+markers':
        markerOnly = dict(
            size = 8,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white', 'dash': line_style},
            symbol = alignment_markers_dropdown
        )
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)
    else:
        markerOnly = dict(
            size = 8,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white', 'dash': line_style},
            symbol = alignment_markers_dropdown
        )
        lineStyle = dict(color = 'rgba({}, {}, {}, {})'.format(
                colorPicker['rgb']['r'],
                colorPicker['rgb']['g'],
                colorPicker['rgb']['b'],
                colorPicker['rgb']['a'],),
                width = 3,
                dash = line_style)

    traces_list = []
    print("Select Vars: {}".format(select_variables))
    print("Vars Len: {}".format(len(select_variables)))
    for variable in select_variables:
        print("Var: {}".format(variable))
        for selection in group_list:
            traces_list.append(
                go.Scatter(
                    x=df[xaxis_column_name],
                    y=df[df[groupby] == selection][variable],
                    text=df[df[groupby] == selection][variable],
                    mode=alignment_labelstyle_dropdown,
                    name=str(variable).replace('[', '').replace(']', '').replace("\'", "")+': '+str(selection),
                    connectgaps = ConnectGaps,
                    fill = Fill,
                    opacity = OS/100,
                    marker = markerOnly,
                    line = dict(color=LINECOLOR_DICT[selection], width=3, dash=line_style)
                    )
                )

    return {
        'data': traces_list,
        'layout': go.Layout(
            xaxis={
                #'title' : xaxis_title,
                'showgrid': show_gridlines,
                #'zeroline': show_zeroline_x,
                'rangeslider': {'visible': True}, 'type': 'date'
            },
            yaxis={
                #'title' : yaxis_title,
                'type' : type_y,
                'showgrid': show_gridlines,
                'zeroline': show_zeroline_y,
                'dtick': y_dtick
                # new
                #'range': [range1[0], range1[1]]
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            #title= title_1,
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
