# Importing Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output

# Read File Function,
# @param: File name (csv or excel)
# @return: Pandas Dataframe
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

# Loading Data
file_name = 'data1.xlsx'
df = read_file(file_name)

# Loading Numeric Data from Dataframe
features=df.select_dtypes(include='number').columns.values
# Loading non-Numeric Data from Dataframe
cat_features=df.select_dtypes(exclude='number').columns.values

# Init Dash App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Generate Dash Layout
app.layout = html.Div([
    # Left Menu
    html.Div([
        html.H5('Variable:'),
        dcc.Dropdown(
            id='dd_features',
            options=[{'label':i, 'value':i} for i in features],
            value=str(features[0])
        ),
        html.H5('Group By:'),
        dcc.Dropdown(
            id='dd_group',
            options=[{'label':i, 'value':i} for i in cat_features],
            value=str(cat_features[0])
        ),
        html.H5('Main Title:'),
        dcc.Input(id='main_title', value='Main Title', type='text'),
        html.H5('X-Axis Title:'),
        dcc.Input(id='xaxis_title', value='X Axis Title', type='text'),
        html.H5('Y-Axis Title:'),
        dcc.Input(id='yaxis_title', value='Y Axis Title', type='text'),
        html.H5('Data Transform:'),
        dcc.RadioItems(
            id='data_transform',
            options=[
                {'label': 'Linear', 'value':'lin'},
                {'label': 'Logarithm', 'value':'log'},
                ],
                value='lin'
            ),
        html.H5('Graph Orientation:'),
        dcc.RadioItems(
            id='graph_orient',
            options=[
                {'label': 'Vertical', 'value':'v'},
                {'label': 'Horizontal', 'value':'h'},
                ],
            value='v'
            ),
        html.H5('Extra Markers:'),
        dcc.Checklist(
            id='extra_markers',
            options=[
                {'label':'Mean', 'value':'mean'},
                {'label':'Std. Dev.', 'value':'sd'},
                ],
                value=[]
            ),
        html.H5('Show Legend:'),
        dcc.RadioItems(
            id='show_legend',
            options=[{'label': i, 'value': i} for i in ['True', 'False']],
            value='True'
            ),
        html.H5('Color Scale:'),
        dcc.Dropdown(
            id='color-scale',
            options=[{'label':i, 'value':i} for i in ['Colors01', 'Colors02']
            ],        
            value='Colors01'
            ),
        html.H5('Opacity:'),
        dcc.Slider(
            id='opacity-slider',
            min=0,
            max=100,
            marks={i: '{}'.format(i) for i in range(0,101,100)},
            value=0
            ),
        html.Div(id='opacity-value', style={'padding':'10px'})
    ], style={'width':'30%', 'display':'inline-block'}),
    
    # Right Graph
    html.Div([
        html.H5('Right Panel'),
        dcc.Graph(id='box-plot')
    ], style={'width':'70%', 'display':'inline-block', 'vertical-align':'top'})
], style={'padding':'10px'})

@app.callback(
    Output('opacity-value', 'children'),
    [Input('opacity-slider','value'),
    ]
)
def update_value(opacity_value):
    return html.H6(opacity_value)
    


@app.callback(
    Output('box-plot', 'figure'),
    [Input('dd_features', 'value'),
     Input('dd_group', 'value'),
     Input('main_title', 'value'),
     Input('xaxis_title', 'value'),
     Input('yaxis_title', 'value'),
     Input('data_transform', 'value'),
     Input('graph_orient', 'value'),
     Input('extra_markers', 'value'),
     Input('show_legend', 'value'),
     Input('opacity-slider', 'value'),
     Input('color-scale', 'value'),
    ]
)
def update_figure(
    variable, groupby, 
    main_title, xaxis_title, yaxis_title, 
    transform, orient, extra,
    show_legend,
    alpha, color_scale):
    
    group_list=df[groupby].unique()
    data_list=[]
    # Extra Markers Options
    if ('sd' in extra):
        box_mean='sd'
    elif ('mean' in extra):
        box_mean=bool(True)
    else:
        box_mean=bool(False)
        
    # Change Variable and Group By
    
    if (color_scale=='Colors01'):
        colors = [
        'rgba(93, 164, 200, 0.5)', 
        'rgba(255, 144, 14, 0.5)', 
        'rgba(44, 160, 101, 0.5)', 
        'rgba(255, 65, 54, 0.5)', 
        'rgba(207, 114, 255, 0.5)', 
        'rgba(127, 96, 0, 0.5)', 
        'rgba(255, 140, 184, 0.5)', 
        'rgba(79, 90, 117, 0.5)', 
        'rgba(222, 223, 0, 0.5)',
        'rgba(255, 195, 18,0.5)', 
        'rgba(196, 229, 56,0.5)', 
        'rgba(18, 203, 196,0.5)', 
        'rgba(253, 167, 223,0.5)', 
        'rgba(237, 76, 103,0.5)', 
        'rgba(163, 203, 56,0.5)', 
        'rgba(18, 137, 167,0.5)', 
        'rgba(217, 128, 250,0.5)', 
        'rgba(181, 52, 113,0.5)',
        ]
    else:
        colors = [
        'rgba(239, 87, 119,0.5)',
        'rgba(87, 95, 207,0.5)',
        'rgba(75, 207, 250,0.5)',
        'rgba(52, 231, 228,0.5)',
        'rgba(11, 232, 129,0.5)',
        'rgba(245, 59, 87,0.5)',
        'rgba(60, 64, 198,0.5)',
        'rgba(15, 188, 249,0.5)',
        'rgba(0, 216, 214,0.5)',
        'rgba(5, 196, 107,0.5)',
        'rgba(255, 192, 72,0.5)',
        'rgba(255, 94, 87,0.5)',
        'rgba(210, 218, 226,0.5)',
        'rgba(255, 221, 89,0.5)',
        'rgba(72, 84, 96,0.5)',
        'rgba(255, 168, 1,0.5)',
        'rgba(255, 211, 42,0.5)',
        'rgba(255, 63, 52,0.5)',
        'rgba(128, 142, 155,0.5)',
        'rgba(30, 39, 46,0.5)',
        ]
    
    color_idx=0
    for i in group_list:
        if (orient=='h'):
            data_list.append(
                go.Box(
                    x=df[df[groupby]==i][variable],
                    name=i,
                    boxmean=box_mean
                )
            )
        else:
            data_list.append(
                go.Box(
                    y=df[df[groupby]==i][variable],
                    name=i,
                    boxmean=box_mean,
                    fillcolor=colors[color_idx],
                    marker={'color':colors[color_idx]}
                )
            )
        color_idx+=1
    if show_legend=='True':
        show_legend=True
    else:
        show_legend=False    
    
    return{
        'data':data_list,
        'layout':go.Layout(
            xaxis=go.layout.XAxis(
                title=xaxis_title
            ),
            yaxis=go.layout.YAxis(
                title=yaxis_title,
                showgrid=True,
                type='linear' if transform=='lin' else 'log',
            ),
            title=main_title,
            showlegend=show_legend,
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)