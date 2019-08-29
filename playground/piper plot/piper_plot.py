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
    fig.add_trace(go.Scatter(x=[1.35*a, 2.35*a], y=[0, 0], mode='lines', hoverinfo="none", line=dict(color=rt_color1, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.35*a, 1.85*a], y=[0, a*yPr], mode='lines', hoverinfo="none", line=dict(color=rt_color2, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.85*a, 2.35*a], y=[a*yPr, 0], mode='lines', hoverinfo="none", line=dict(color=rt_color3, width=line_width)))
    
    # right terniary grid lines
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 1.35*a, 0.2*a + 1.35*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 1.35*a, 0.4*a + 1.35*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 1.35*a, 0.6*a + 1.35*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 1.35*a, 0.8*a + 1.35*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color1, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 1.35*a, 0.2*a*xPr + 0.8*a + 1.35*a], y=[0.2*a*yPr, 0.2*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 1.35*a, 0.4*a*xPr + 0.6*a + 1.35*a], y=[0.4*a*yPr, 0.4*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 1.35*a, 0.6*a*xPr + 0.4*a + 1.35*a], y=[0.6*a*yPr, 0.6*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 1.35*a, 0.8*a*xPr + 0.2*a + 1.35*a], y=[0.8*a*yPr, 0.8*a*yPr], mode='lines', hoverinfo='none', line=dict(color=rt_color2, width=grid_width, dash=dash)))
    
    fig.add_trace(go.Scatter(x=[0.8*a*xPr + 0.2*a + 1.35*a, 0.2*a + 1.35*a], y=[0.8*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.6*a*xPr + 0.4*a + 1.35*a, 0.4*a + 1.35*a], y=[0.6*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.4*a*xPr + 0.6*a + 1.35*a, 0.6*a + 1.35*a], y=[0.4*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[0.2*a*xPr + 0.8*a + 1.35*a, 0.8*a + 1.35*a], y=[0.2*a*yPr, 0], mode='lines', hoverinfo='none', line=dict(color=rt_color3, width=grid_width, dash=dash)))
       
    # upper diamond perimeter
    ud_color='#42213d'
    fig.add_trace(go.Scatter(x=[1.35*a*xPr, 2.35*a*xPr], y=[1.35*a*yPr, 2.35*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.35*a*xPr, 1.175*a], y=[1.35*a*yPr, 0.35*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.175*a, 2.35*a*xPr + 0.5*a], y=[2.35*a*yPr, 1.35*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    fig.add_trace(go.Scatter(x=[1.175*a, 2.35*a*xPr + 0.5*a], y=[0.35*a*yPr, 1.35*a*yPr], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=line_width)))
    
    # upper diamond grid lines
    xTrans = a*xPr
    yTrans = a*yPr
    
    fig.add_trace(go.Scatter(x=[a/2+0.55*xTrans, a+0.55*xTrans], y=[a*yPr+0.55*yTrans, 0.55*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[a/2+0.75*xTrans, a+0.75*xTrans], y=[a*yPr+0.75*yTrans, 0.75*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[a/2+0.95*xTrans, a+0.95*xTrans], y=[a*yPr+0.95*yTrans, 0.95*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[a/2+1.15*xTrans, a+1.15*xTrans], y=[a*yPr+1.15*yTrans, 1.15*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))

    fig.add_trace(go.Scatter(x=[1.35*a-0.55*xTrans, 1.85*a-0.55*xTrans], y=[0.55*yTrans, a*yPr+0.55*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[1.35*a-0.75*xTrans, 1.85*a-0.75*xTrans], y=[0.75*yTrans, a*yPr+0.75*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[1.35*a-0.95*xTrans, 1.85*a-0.95*xTrans], y=[0.95*yTrans, a*yPr+0.95*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    fig.add_trace(go.Scatter(x=[1.35*a-1.15*xTrans, 1.85*a-1.15*xTrans], y=[1.15*yTrans, a*yPr+1.15*yTrans], mode='lines', hoverinfo="none", line=dict(color=ud_color, width=grid_width, dash=dash)))
    
    # canvas
    fig.add_trace(
        go.Scatter(x=[-1,2.25*a+1, 2.25*a+1, -1], y=[-0.5,-0.5, 2*a+1, 2*a+1], mode='markers', opacity=0, hoverinfo="none"))
    
    fig.update_layout(
        autosize=False,
        width=canvas_width,
        height=canvas_height,
        showlegend=False
        )
    
    # Axis label
    fig.update_layout(
        annotations=[
            # left terniary
            go.layout.Annotation(x=0, y=0, text='100', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=0.2*a, y=0, text='80', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=0.4*a, y=0, text='60', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=0.6*a, y=0, text='40', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=0.8*a, y=0, text='20', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=a, y=0, text='0', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='top'),
            
            go.layout.Annotation(x=0, y=0, text='0', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=0.2*xTrans, y=0.2*yTrans, text='20', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=0.4*xTrans, y=0.4*yTrans, text='40', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=0.6*xTrans, y=0.6*yTrans, text='60', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=0.8*xTrans, y=0.8*yTrans, text='80', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=xTrans, y=yTrans, text='100', font=dict(color=lt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            
            go.layout.Annotation(x=xTrans, y=yTrans, text='0', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=0.2*xTrans+0.8*a, y=0.2*yTrans, text='20', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=0.4*xTrans+0.6*a, y=0.4*yTrans, text='40', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=0.6*xTrans+0.4*a, y=0.6*yTrans, text='60', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=0.8*xTrans+0.2*a, y=0.8*yTrans, text='80', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=a, y=0, text='100', font=dict(color=lt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            
            # right terniary
            go.layout.Annotation(x=1.35*a, y=0, text='0', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=1.55*a, y=0, text='20', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=1.75*a, y=0, text='40', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=1.95*a, y=0, text='60', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=2.15*a, y=0, text='80', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            go.layout.Annotation(x=2.35*a, y=0, text='100', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='top'),
            
            go.layout.Annotation(x=1.35*a+0, y=0, text='0', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.2*xTrans, y=0.2*yTrans, text='20', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.4*xTrans, y=0.4*yTrans, text='40', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.6*xTrans, y=0.6*yTrans, text='60', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.8*xTrans, y=0.8*yTrans, text='80', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+xTrans, y=yTrans, text='100', font=dict(color=rt_color2), showarrow=False, xanchor='right', yanchor='bottom'),
            
            go.layout.Annotation(x=1.35*a+xTrans, y=yTrans, text='0', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.2*xTrans+0.8*a, y=0.2*yTrans, text='20', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.4*xTrans+0.6*a, y=0.4*yTrans, text='40', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.6*xTrans+0.4*a, y=0.6*yTrans, text='60', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+0.8*xTrans+0.2*a, y=0.8*yTrans, text='80', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=1.35*a+a, y=0, text='100', font=dict(color=rt_color3), showarrow=False, xanchor='left', yanchor='bottom'),
            
            # upper diamond
            go.layout.Annotation(x=1.35*xTrans, y=1.35*yTrans, text='0', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.55*xTrans, y=1.55*yTrans, text='20', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.75*xTrans, y=1.75*yTrans, text='40', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=1.95*xTrans, y=1.95*yTrans, text='60', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=2.15*xTrans, y=2.15*yTrans, text='80', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            go.layout.Annotation(x=2.35*xTrans, y=2.35*yTrans, text='100', font=dict(color=ud_color), showarrow=False, xanchor='right', yanchor='bottom'),
            
            go.layout.Annotation(x=2.35*xTrans, y=2.35*yTrans, text='100', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=2.55*xTrans, y=2.15*yTrans, text='80', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=2.75*xTrans, y=1.95*yTrans, text='60', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=2.95*xTrans, y=1.75*yTrans, text='40', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=3.15*xTrans, y=1.55*yTrans, text='20', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            go.layout.Annotation(x=3.35*xTrans, y=1.35*yTrans, text='0', font=dict(color=ud_color), showarrow=False, xanchor='left', yanchor='bottom'),
            
            go.layout.Annotation(x=a/2, y=-0.5, text='Calcium', font=dict(color=lt_color1), showarrow=False, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=1.85*a, y=-0.5, text='Chloride', font=dict(color=rt_color1), showarrow=False, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=xTrans/2-0.15*a, y=yTrans/2+0.05*a, text='Magnesium', font=dict(color=lt_color2), showarrow=False, textangle=-60, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=xTrans/2+0.65*a, y=yTrans/2+0.05*a, text='Natrium + Kalium', font=dict(color=lt_color3), showarrow=False, textangle=60, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=3.15*xTrans-0.15*a, y=yTrans/2+0.05*a, text='Carbonate + Bicarbonate', font=dict(color=rt_color2), showarrow=False, textangle=-60, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=3.15*xTrans+0.65*a, y=yTrans/2+0.05*a, text='Sulfate', font=dict(color=rt_color3), showarrow=False, textangle=60, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=1.85*xTrans-0.15*a, y=1.85*yTrans+0.05*a, text='Sulfate + Chloride', font=dict(color=ud_color), showarrow=False, textangle=-60, xanchor='center', yanchor='middle'),
            go.layout.Annotation(x=1.85*xTrans+0.65*a, y=1.85*yTrans+0.05*a, text='Calcium + Magnesium', font=dict(color=ud_color), showarrow=False, textangle=60, xanchor='center', yanchor='middle'),
            
            
            ]
        )
    
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    
    return fig