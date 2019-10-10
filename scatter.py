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
import dash_daq as daq


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

        

        html.H6("Functional Buttons:"),
        html.Div([
        	#set a button for swaping X and Y
        	daq.BooleanSwitch(label='Swap Axes', id='swap', on=False),
        	#set a button for showing the linear fit
            daq.BooleanSwitch(label='Show Linear Best Fit', id='linear', on=False),
            #set a button for hiding or showing the grid line
            daq.BooleanSwitch(label='Toggle Grid Lines', id='GL', on=False),
            #set a button for hiding or showing the zero line
            daq.BooleanSwitch(label='Toggle Zero Marker', id='OL', on=False),
            #set a button for hisding or showing the label
            daq.BooleanSwitch(label='Show Label', id='LB', on=False),
            #set a button for hiding or showing legends
            daq.BooleanSwitch(label='Show Legend', id='LD', on=True),
            ], style={'width': '100%', 'display': 'inline-block'}),

        html.H6("Change Opacity:"),
        html.Div([
        	#set a slider to change the opacity
        	dcc.Slider(
        		id='opacity-slider',
        		min=0,
        		max=100,
        		value=70,
        		)
        	]),

        html.H6("Change Distance of X ticks:"),
        html.Div([
        	#set an input to change the distance between x ticks
        	dcc.Input(
                id="X-dtick",
                type="number",
                min=1)
        	]),

        html.H6("Change Distance of Y ticks:"),
        html.Div([
        	#set an input to change the distance between y ticks
        	dcc.Input(
                id="Y-dtick",
                type="number",
                min=1)
        	]),

        html.H6("Add a thredshold for X:"),
        html.Div([
        	#set an input to add a threshold for X
        	dcc.Input(
        		id='X-thredshold',
        		type='number'
        		)
        	]),

        html.H6("Add a thredshold for Y:"),
        html.Div([
        	#set an input to add a threshold for Y
        	dcc.Input(
        		id='Y-thredshold',
        		type='number'
        		)
        	]),

    	html.Div([
    		

        	html.H6("Color and Hover Text Grouping"),
        	dcc.Dropdown(
				id='color-drop',
				options=[{'label': i, 'value': i} for i in df.columns],
				value=df.columns[0],
				),

        	html.H6("Change Marker Style:"),
        	dcc.Dropdown(
        		#set an option for choosing the markers' style
            	id='alignment-markers-dropdown',
            	className='markers-controls-block-dropdown',
            	options=MARKERS_DICT,
            	value='circle',
    			),

    		html.H6("Change Colorscale:"),
        	dcc.Dropdown(
        		#set an option for choosing the colorscale
            	id='alignment-colorscale-dropdown',
            	options=COLORSCALES_DICT,
            	value='Greys',
            	)
    		]),

    	html.Div([
    		html.H6("Chose a Trace (If the trace is number, selcet the color through the Colorscale):"),
    		dcc.RadioItems(
    			id='selected-groupby'
    			)
    		],
    		style={'width': '45%', 'float': 'left', 'display': 'inline-block'}),

    	html.Div([
    		html.H6("Chose a Color:"),
    		daq.ColorPicker(
    			id='my-color-picker',
    			value={
    			'rgb': {'a': 1, 'r': 22, 'b': 222, 'g': 160},
    			'hex': '#16a0de'
    			}
    			)
    		],
    		style={'float': 'right', 'display': 'inline-block'})
    ], style={'width': '45%', 'height':'100%', 'display': 'inline-block', 'float': 'left'}),


    html.Div([
    	dcc.Graph(
    		id='indicator-graphic'
    		),
    	], style={'width': '50%', 'height':'100%', 'display': 'inline-block', 'float': 'right'})
])

@app.callback(
	Output('selected-groupby', 'options'),
	[Input('color-drop', 'value'),]
	)
def traces_groupby(color_drop):
	if df[color_drop].dtypes =='object':
		return [{'label': i, 'value': i} for i in df[color_drop].unique()]
	else:
		return [{'label': color_drop, 'value': color_drop}]

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
     Input('LB', 'on'),])
def update_graph(xaxis_column_name, yaxis_column_name,
                 xaxis_type, yaxis_type,
                 title_1, alignment_colorscale_dropdown, 
                 swap, linear, x_label, y_label, GL, OL, 
                 alignment_markers_dropdown, color_var, LD, OS, X_D, Y_D, X_T, Y_T, G_t, C_P, LB):
    
    slope, intercept, r_value, p_value, std_err = stats.linregress(df[xaxis_column_name],df[yaxis_column_name])
    line = slope*df[xaxis_column_name]+intercept


    if swap:
    	# Swapping the x and y axes names and values
        tmp = xaxis_column_name
        xaxis_column_name = yaxis_column_name
        yaxis_column_name = tmp
        tmp1 = x_label
        x_label = y_label
        y_label = tmp1


    threshold_shape = []


    #if users set a thredshold for X, then show this line
    if X_T !=None:
    	threshold_shape.append(dict(
    	type='line',
    	x0=X_T,
    	x1=X_T,
    	y0=df[yaxis_column_name].min(),
    	y1=df[yaxis_column_name].max()
    	))

    #if users set a thredshold for Y, then show this line
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
    		if i == G_t:
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
	       			'color': C_P['hex']
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
		       			'symbol': alignment_markers_dropdown
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
	        	showscale = LD,
	        	symbol = alignment_markers_dropdown
	    	),
	    	name='{} VS {}'.format(xaxis_column_name, yaxis_column_name)
	    ))

    traces.append(go.Scatter(
    	x=df[xaxis_column_name],
        y=line,
        mode='lines',
        marker=dict(
            size = 15,
            opacity = 0.5,
            line = {'width': 0.5, 'color': 'white'},
            color = 'black',
            showscale = LD,
        ),
        name='Fit',
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
        legend=dict(x=-.1, y=1.2),
        showlegend = LD,
        shapes=threshold_shape,
        hovermode='closest'
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
