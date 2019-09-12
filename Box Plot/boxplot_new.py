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
app = dash.Dash(__name__)

# Generate Dash Layout
app.layout = html.Div([
    # Left Panel - Menu
    html.Div([
        # Feature Selection
        
            # Feature
            html.Div([
                html.H5('Variable:'),
                dcc.Dropdown(
                    id='dd_features',
                    options=[{'label':i, 'value':i} for i in features],
                    value=str(features[0])
                    )
                ]),
            # Group By
            html.Div([
                html.H5('Group By:'),
                dcc.Dropdown(
                    id='dd_group',
                    options=[{'label':i, 'value':i} for i in cat_features],
                    value=str(cat_features[0])
                    )
                ]),
        
        # Title Modification
        
            # Main Title
            html.Div([
                html.H5('Main Title:'),
                dcc.Input(id='main_title', value='Main Title', type='text')
            ]),
            # X-axis
            html.Div([
                html.H5('X-Axis Title:'),
                dcc.Input(id='xaxis_title', value='X Axis Title', type='text')
            ]),
            # Y-axis
            html.Div([
                html.H5('Y-Axis Title:'),
                dcc.Input(id='yaxis_title', value='Y Axis Title', type='text')
            ]),
        
        # Data Transformation & Plot Orientation
        
            # Data Transform
            html.Div([
                html.H5('Data Transform:'),
                dcc.RadioItems(
                    id='data_transform',
                    options=[
                        {'label': 'Linear', 'value':'lin'},
                        {'label': 'Logarithm', 'value':'log'},
                    ],
                    value='lin'
                    )
                ], style={}
            ),
            # Plot Orientiation
            html.Div([
                html.H5('Graph Orientation:'),
                dcc.RadioItems(
                    id='graph_orient',
                    options=[
                        {'label': 'Vertical', 'value':'ver'},
                        {'label': 'Horizontal', 'value':'hor'},
                    ],
                    value='ver'
                    )
                ], style={}
            ),
       
        # Extra Markers

            # Mean and/or SD
            html.Div([
                html.H5('Extra Markers:'),
                dcc.Checklist(
                    id='extra_markers',
                    options=[
                        {'label':'Mean', 'value':'mean'},
                        {'label':'Std. Dev.', 'value':'sd'},
                    ],
                    value=[]
                )
            ]),

        # Legend

            # Show/Hide Legend
            html.Div([
                html.H5('Show Legend:'),
                dcc.RadioItems(
                    id='show_legend',
                    options=[{'label': i, 'value': i} for i in ['True', 'False']],
                    value='True'
                )
            ]),

        # Color Scale

            # Color Scale Dropdown
            html.Div([
                html.H5('Color Scale:'),
                dcc.Dropdown(
                    id='color_scale',
                    options=[{'label':i, 'value':i} for i in ['Viridis', 'Cividis']
                    ],
                    value='Viridis'
                )
            ]),

        # Alpha Channel/Opacity

            # Opacity Slider
            html.Div([
                html.H5('Opacity:'),
                dcc.Slider(
                    min=0,
                    max=100,
                    marks={i: '{}'.format(i) for i in range(0,101,10)},
                    value=0
                )
            ]),

    ], style={'width': '30%', 'display': 'inline-block', 'padding':'5px'}),
    # Right Panel - Graph
    html.Div([
        dcc.Graph(id='box-plot')
    ], style={'width': '70%', 'display': 'inline-block', 'padding':'5px'})
])


if __name__ == '__main__':
    app.run_server(debug=True)