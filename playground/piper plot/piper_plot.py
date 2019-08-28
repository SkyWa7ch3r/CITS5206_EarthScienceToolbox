import plotly.graph_objects as go
import math

def piper_plot(canvas_width=800, canvas_height=800, line_width=1.5, grid_width=1, grid_dash='dot'):
    fig = go.Figure()
    
    # triangle base line length
    a = 5
    
    # Projection factor for x-axis and y-axis
    xPr = math.cos(math.radians(60))
    yPr = math.sin(math.radians(60))
    
    # line width for perimeter line and grid line
    line_width = line_width
    grid_width = grid_width
    
    # left terniary perimeter
    lt_color1='#726da8'
    lt_color2='#bd4089'
    lt_color3='#6a8d73'
    dash=grid_dash
    fig.add_trace(go.Scatter(x=[0, a], y=[0, 0], mode='lines', hoverinfo="none", line=dict(color=lt_color1, width=line_width)))
    fig.add_trace(go.Scatter(x=[0, a/2], y=[0, a*yPr], mode='lines', hoverinfo="none", line=dict(color=lt_color2, width=line_width)))
    fig.add_trace(go.Scatter(x=[a/2, a], y=[a*yPr, 0], mode='lines', hoverinfo="none", line=dict(color=lt_color3, width=line_width)))
    
    # left terniary grid lines
    fig.add_trace(go.Scatter(x=[0.2*a*xPr, 0.2*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr, 0.4*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr, 0.6*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr, 0.8*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color1, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.2*a*xPr, 0.2*a*xPr + 0.8*a], y=[0.2*a*yPr, 0.2*a*yPr], mode='lines', hoverinfo='none', line=dict(color=lt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr, 0.4*a*xPr + 0.6*a], y=[0.4*a*yPr, 0.4*a*yPr], mode='lines', hoverinfo='none', line=dict(color=lt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr, 0.6*a*xPr + 0.4*a], y=[0.6*a*yPr, 0.6*a*yPr], mode='lines', hoverinfo='none', line=dict(color=lt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr, 0.8*a*xPr + 0.2*a], y=[0.8*a*yPr, 0.8*a*yPr], mode='lines', hoverinfo='none', line=dict(color=lt_color2, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 0.2*a, 0.2*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 0.4*a, 0.4*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 0.6*a, 0.6*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 0.8*a, 0.8*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=lt_color3, width=grid_width, dash=dash)))
    
    # right terniary perimeter
    rt_color1='#bb4430'
    rt_color2='#264653'
    rt_color3='#337357'
    fig.add_trace(go.Scatter(x=[1.25*a, 2.25*a], y=[0, 0], mode='lines', hoverinfo="none", line=dict(color=rt_color1, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.25*a, 1.75*a], y=[0, a*yPr], mode='lines', hoverinfo="none", line=dict(color=rt_color2, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.75*a, 2.25*a], y=[a*yPr, 0], mode='lines', hoverinfo="none", line=dict(color=rt_color3, width=line_width)))
    
    # right terniary grid lines
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 1.25*a, 0.2*a + 1.25*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 1.25*a, 0.4*a + 1.25*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 1.25*a, 0.6*a + 1.25*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 1.25*a, 0.8*a + 1.25*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 1.25*a, 0.2*a*xPr + 0.8*a + 1.25*a], y=[0.2*a*yPr, 0.2*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 1.25*a, 0.4*a*xPr + 0.6*a + 1.25*a], y=[0.4*a*yPr, 0.4*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 1.25*a, 0.6*a*xPr + 0.4*a + 1.25*a], y=[0.6*a*yPr, 0.6*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 1.25*a, 0.8*a*xPr + 0.2*a + 1.25*a], y=[0.8*a*yPr, 0.8*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 0.2*a + 1.25*a, 0.2*a + 1.25*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 0.4*a + 1.25*a, 0.4*a + 1.25*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 0.6*a + 1.25*a, 0.6*a + 1.25*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 0.8*a + 1.25*a, 0.8*a + 1.25*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
       
    # upper diamond perimeter
    ud_color='#42213d'
    fig.add_trace(go.Scatter(x=[1.25*a*xPr, 2.25*a*xPr], y=[1.25*a*yPr, 2.25*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.25*a*xPr, 1.125*a], y=[1.25*a*yPr, 0.25*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.125*a, 2.25*a*xPr + 0.5*a], y=[2.25*a*yPr, 1.25*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.125*a, 2.25*a*xPr + 0.5*a], y=[0.25*a*yPr, 1.25*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    
    # canvas
    fig.add_trace(
        go.Scatter(x=[-1,2.25*a+1, 2.25*a+1, -1], y=[-0.5,-0.5, 2*a, 2*a], mode='markers', opacity=0, hoverinfo="none"))
    
    fig.update_layout(
        autosize=False,
        width=canvas_width,
        height=canvas_height,
        showlegend=False
        )
    
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    
    return fig