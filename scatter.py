import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import plotly.express as px
from scipy import stats
from numpy import arange,array,ones
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


file_name='../../UWA_acid_base_table.xlsx'

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



app.layout = html.Div([
    html.Div([
        html.Div([
        	#set an option to choose the X value
        	html.H6("Choose X value:"),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in cnames],
                value=cnames[0],
            ),

            #set an option to choose the Y value
            html.H6("Choose Y Value:"),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in cnames],
                value=cnames[-1],
            )
            
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
        	#set a radio to choose linear or logarithmic for X
        	html.H6("Linear or Logarithmic:"),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            ),

            #set a radio to choose linear or logarithmic for Y
            html.H6("Linear or Logarithmic:"),
            dcc.RadioItems(
                id='yaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value='Linear',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        html.Div([
        	#set an input box for inputing title
        	html.H6("Input a Title:"),
            dcc.Input(
                id="title",
                type="text",
                placeholder="title")
            ],
        	style={'width': '33%', 'float': 'left', 'display': 'inline-block'}),

        html.Div([
        	#set an input box for inputing X label
        	html.H6("Input X Label:"),
        	dcc.Input(
                id="x_label",
                type="text")
        	],
        	style={'width': '33%', 'float': 'center', 'display': 'inline-block'}),

        html.Div([
        	#set an input box for inputing Y label
        	html.H6("Input Y Label:"),
            dcc.Input(
                id="y_label",
                type="text")
            ],
            style={'width': '33%', 'float': 'right', 'display': 'inline-block'}),

        html.H6("Change Marker Style:"),
        dcc.Dropdown(
        	#set an option for choosing the markers' style
            id='alignment-markers-dropdown',
            className='markers-controls-block-dropdown',
            options=MARKERS_DICT,
            value='circle',
    		),

        html.H6("Functional Buttons:"),
        html.Div([
        	#set a button for swaping X and Y
            html.Button('Swap Axes', id='swap'),
            #set a button for showing the linear fit
            html.Button('Show Linear Best Fit', id='linear'),
            #set a button for hiding or showing the grid line
            html.Button('Toggle Grid Lines', id='GL'),
            #set a button for hiding or showing the zero line
            html.Button('Toggle Zero Marker', id='OL'),
            #set a button for hiding or showing legends
            html.Button('Show Legend', id='LD')
            ], style={'width': '100%', 'display': 'inline-block'}),

        html.H6("Change Opacity:"),
        html.Div([
        	dcc.Slider(
        		id='opacity-slider',
        		min=0,
        		max=100,
        		value=70,
        		)
        	]),

        html.H6("Change Distance of X ticks:"),
        html.Div([
        	dcc.Input(
                id="X-dtick",
                type="number")
        	]),

        html.H6("Change Distance of Y ticks:"),
        html.Div([
        	dcc.Input(
                id="Y-dtick",
                type="number")
        	]),

    	html.Div([
    		html.H6("Change Colorscale:"),
        	dcc.Dropdown(
        		#set an option for choosing the colorscale
            	id='alignment-colorscale-dropdown',
            	className='app-controls-block-dropdown',
            	options=COLORSCALES_DICT,
            	value='Blackbody',
            	),

        	html.Div("Color and Hover Text Grouping"),
        	dcc.Dropdown(
				id='color-drop',
				options=[{'label': i, 'value': i} for i in df.columns],
				value=df.columns[0],
				)
    		]),
    ], style={'width': '45%', 'height':'100%', 'display': 'inline-block', 'float': 'left'}),

    html.Div([
    	dcc.Graph(
    		id='indicator-graphic'
    		),
    	], style={'width': '50%', 'height':'100%', 'display': 'inline-block', 'float': 'right'})
])


@app.callback(
    Output('x_label', 'value'),
    [Input('xaxis-column', 'value')])
def set_cities_options(X_c):
    return X_c

@app.callback(
    Output('y_label', 'value'),
    [Input('yaxis-column', 'value')])
def set_cities_options(Y_c):
    return Y_c

@app.callback(
    Output('indicator-graphic', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('xaxis-type', 'value'),
     Input('yaxis-type', 'value'),
     Input('title', 'value'),
     Input('alignment-colorscale-dropdown', 'value'),
     Input('swap', 'n_clicks'),
     Input('linear', 'n_clicks'),
     Input('x_label', 'value'),
     Input('y_label', 'value'),
     Input('GL', 'n_clicks'),
     Input('OL', 'n_clicks'),
     Input('alignment-markers-dropdown', 'value'),
     Input('color-drop', 'value'),
     Input('LD', 'n_clicks'),
     Input('opacity-slider', 'value'),
     Input('X-dtick', 'value'),
     Input('Y-dtick', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 title_1, alignment_colorscale_dropdown, 
                 swap, linear, x_label, y_label, GL, OL, 
                 alignment_markers_dropdown, color_var, LD, OS, X_D, Y_D):
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    line = slope*df[xaxis_column_name]+intercept


    if swap != None and int(swap) % 2 == 1:
    	# Swapping the x and y axes names and values
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp
        tmp1 = x_label
        x_label = y_label
        y_label = tmp1
        tmp2 = X_D
        X_D = Y_D
        Y_D = tmp2


    # Showing the fit linear
    l_click = False
    if linear != None and int(linear) % 2 == 1:
        l_click = True
    
    # Showing the grid line
    G_click = False
    if GL != None and int(GL) % 2 == 1:
        G_click = True

    # Showing the zero line
    O_click = False
    if OL != None and int(OL) % 2 == 1:
        O_click = True

    # Showing the zero line
    LD_click = True
    if LD != None and int(LD) % 2 == 1:
        LD_click = False

    return {
        'data': [go.Scatter(
            x=df[xaxis_column_name],
            y=df[yaxis_column_name],
            mode='markers',
            text=df[color_var],
            opacity=OS/100,
            marker=dict(
                size = 15,
                opacity = 0.5,
                line = {'width': 0.5, 'color': 'white'},
                color = df[color_var],
                colorscale = alignment_colorscale_dropdown,
                showscale = LD_click,
                symbol = alignment_markers_dropdown
            ),

        ),
        
        go.Scatter(
                x=df[xaxis_column_name],
                y=line,
                mode='lines',
                marker=dict(
                    size = 15,
                    opacity = 0.5,
                    line = {'width': 0.5, 'color': 'white'},
                    color = 'black',
                    colorscale = alignment_colorscale_dropdown,
                    showscale = LD_click,
            ),
                name='Fit',
                visible=l_click
                    )
        ],

        'layout': go.Layout(
            xaxis={
                'title': x_label,
                'type': 'linear' if xaxis_type == 'Linear' else 'log',
                'showgrid': G_click,
                'zeroline': O_click,
                'dtick': X_D
            },
            yaxis={
                'title': y_label,
                'type': 'linear' if yaxis_type == 'Linear' else 'log',
                'showgrid': G_click,
                'zeroline': O_click,
                'dtick': Y_D
            },
            title= title_1,
            showlegend = LD_click,
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)
