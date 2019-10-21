# IMPORT LIBRARIES
import dash_core_components as dcc
import dash_daq as daq

# VARIABLES
toggle_switch_color='#91c153'

# Function: Render drop down list
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown(id, options):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': i} for i in options],
        className='card h-100' )

# Function: Render drop down list
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown_dict(id, options):
    return dcc.Dropdown(id=id, options=options,
        className='card h-100' )

# Function: Render drop down list with selected value
# Input: id, [options], value
# Output: dcc.Dropdown
def render_dropdown_valued(id, options, value):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': i} for i in options], value=value,
        className='card h-100' )

# Function: Render drop down list with selected value
# Input: id, [options], value
# Output: dcc.Dropdown
def render_dropdown_dict_valued(id, options, value):
    return dcc.Dropdown(id=id, options=options, value=value,
        className='card h-100' )

# Function: Render drop down list without any options
# Input: id
# Output: dcc.Dropdown
def render_dropdown_blank(id):
    return dcc.Dropdown(id=id)


# Function: Render drop down list with label formatting (remove space between words and turn to lower case)
# Input: id, [options]
# Output: dcc.Dropdown
def render_dropdown_format(id, options):
    return dcc.Dropdown(id=id, options=[{'label': i, 'value': (i.replace(" ", "")).lower()} for i in options],
        className='card h-100' )

# Function: Render radio items
# Input: id, [options]
# Output: dcc.RadioItems
def render_radio(id, options):
    return dcc.RadioItems(id=id, options=[{'label': i, 'value': i} for i in options],
        value=str(options[0]), labelStyle={'display': 'block'} )

# Function: Render radio items with selected value
# Input: id, [options], value
# Output: dcc.RadioItems
def render_radio_valued(id, options, value):
    return dcc.RadioItems(id=id, options=[{'label': i, 'value': i} for i in options],
        value=value, labelStyle={'display': 'block'} )

# Function: Render radio items for data points and outlies
# Input: id
# Output: dcc.RadioItems
def render_radio_outliers(id):
    return dcc.RadioItems(
        id=id,
        options=[
            {'label': 'Default', 'value': 'outliers'},
            {'label': 'Only Wiskers', 'value': 'False'},
            {'label': 'Suspected Outliers', 'value': 'suspectedoutliers'},
            {'label': 'All Points', 'value': 'all'},
        ],
        value='outliers',
        labelStyle={'display': 'block'} )

# Function: Render radio items contain id only
# Input: id
# Output: dcc.RadioItems
def render_radio_blank(id):
    return dcc.RadioItems(id=id, labelStyle={'display': 'block'} )

# Function: Render radio items with label formatting (remove space between words and turn to lower case)
# Input: id, [options]
# Output: dcc.RadioItems
def render_radio_format(id, options):
    return dcc.RadioItems(
        id=id,
        options=[{'label': i, 'value': (i.replace(" ", "")).lower()} for i in options],
        value=(str(options[0]).replace(" ", "")).lower(),
        labelStyle={'display': 'block'}, )

# Function: Render text input
# Input: id, placeholder
# Output: dcc.Input
def render_input(id, placeholder):
    return dcc.Input(id=id, type='text', placeholder=placeholder, style={'width': '100%'})

# Function: Render number input
# Input: id, placeholder
# Output: dcc.Input
def render_input_number(id, placeholder):
    return dcc.Input(id=id, type='number', min=0, placeholder=placeholder, style={'width': '100%'})

# Function: Render number input with costum minimum value
# Input: id, placeholder, min
# Output: dcc.Input
def render_input_number_min(id, placeholder, min):
    return dcc.Input(id=id, type='number', min=min, placeholder=placeholder, step=0.1, style={'width': '100%'})

# Function: Render text input with delay feature, will callback after enter key pressed or input area loss its focus
# Input: id, placeholder
# Output: dcc.RadioItems
def render_input_delay(id, placeholder):
    return dcc.Input(id=id, type='text', placeholder=placeholder, debounce=True, style={'width': '100%'})

# Function: Render toggle switch
# Input: id, [labels], value
# Output: daq.ToggleSwitch
def render_toggleswitch(id, labels, value):
    return daq.ToggleSwitch(id=id, label=labels, value=value, color=toggle_switch_color, )

# Function: Render boolean switch
# Input: id, label, on
# Output: daq.BooleanSwitch
def render_booleanswitch(id, label, on):
    return daq.BooleanSwitch(id=id, label=label, on=on, labelPosition='top', color=toggle_switch_color, )

# Function: Render boolean switch without label
# Input: id, on
# Output: daq.BooleanSwitch
def render_booleanswitch_nolab(id, on):
    return daq.BooleanSwitch(id=id, on=on, color=toggle_switch_color, )

# Function: Render slider
# Input: id, min, max, value, step, label
# Output: daq.Slider
def render_slider(id, min, max, value, step, marks):
    mymark={}
    for i in marks:
        mymark[i]=str(i)
    return daq.Slider(id=id, min=min, max=max, value=value, step=step, marks=mymark )

# Function: Render Range slider
# Input: id, min, max, [value], step, {marks}
# Output: dcc.RangeSlider
def render_range_slider(id, min, max, value, step, marks):
    return dcc.RangeSlider(id=id, min=min, max=max, value=value, step=step, marks=marks )

# Function: Render color picker
# Input: id, min, max, value, step, label
# Output: daq.ColorPicker
def render_colorpicker(id, color, r, g, b, a):
    value=dict(rgb=dict(r=r, g=g, b=b, a=a))
    return daq.ColorPicker(id=id, value=value)

# Function: Render numeric Input
# Input: id, min, max, value
# Output: daq.NumericInput
def render_numinput(id, min, max, value):
    return daq.NumericInput(id=id, min=min, max=max, value=value )

# Function: Render numeric Input just minimum value
# Input: id, min
# Output: daq.NumericInput
def render_numinput_justmin(id, min):
    return daq.NumericInput(id=id, min=min, className='w-100')
