import plotly.graph_objects as go
import math

def draw_line(figure, length, color, rotation=0, dash='solid', xOrigin=0, yOrigin=0, line_size=1):
    # Projection factor for x-axis and y-axis
    xPr = math.cos(math.radians(rotation))
    yPr = math.sin(math.radians(rotation))
    
    figure.add_trace(go.Scatter(x=[xOrigin, xOrigin+length*xPr], y=[yOrigin, yOrigin+length*yPr], mode='lines', line=dict(dash=dash, color=color, width=line_size), hoverinfo="none", showlegend=False))
    
    return figure

def plot_bg(colors, canvas_width=750, canvas_height=750):
    base = 100
    space = 0.35*base
    xPr = math.cos(math.radians(60))
    yPr = math.sin(math.radians(60))
    
    fig = go.Figure()
    # frame
    fig.add_trace(go.Scatter(x=[-0.1*base, (2.1*base+space)], y=[-0.1*base*yPr, (2*base+space)*yPr+0.1*base], mode='markers', opacity=0, hoverinfo="none", showlegend=False))
    
    # perimeters
    col_idx=0
    for i in range(2):
        for j in range(2):
            fig = draw_line(figure=fig, length=base, rotation=j*60, xOrigin=i*(base+space), color=colors[col_idx], line_size=1.5)
            col_idx += 1
        fig = draw_line(figure=fig, length=base, rotation=120, xOrigin=base+i*(base+space), color=colors[col_idx], line_size=1.5)
        col_idx += 1
    
    for i in range(2):
        fig = draw_line(figure=fig, length=base, rotation=(-1)**i*60, xOrigin=(base+space)*xPr, yOrigin=(base+space)*yPr, color=colors[6], line_size=1.5)
        fig = draw_line(figure=fig, length=base, rotation=(-1)**i*120, xOrigin=(2*base+space)-(base+space)*xPr, yOrigin=(base+space)*yPr, color=colors[6], line_size=1.5)
    
    # grid lines
    for i in range(4):
        fig = draw_line(figure=fig, length=0.2*(i+1)*base, rotation=120, xOrigin=0.2*(i+1)*base, yOrigin=0, dash='dot', color=colors[0])
        fig = draw_line(figure=fig, length=0.2*(4-i)*base, rotation=0, xOrigin=0.2*(i+1)*base*xPr, yOrigin=0.2*(i+1)*base*yPr, dash='dot', color=colors[1])
        fig = draw_line(figure=fig, length=0.2*(4-i)*base, rotation=60, xOrigin=0.2*(i+1)*base, yOrigin=0, dash='dot', color=colors[2])
        
        fig = draw_line(figure=fig, length=0.2*(i+1)*base, rotation=120, xOrigin=0.2*(i+1)*base+(base+space), yOrigin=0, dash='dot', color=colors[4])
        fig = draw_line(figure=fig, length=0.2*(4-i)*base, rotation=0, xOrigin=0.2*(i+1)*base*xPr+(base+space), yOrigin=0.2*(i+1)*base*yPr, dash='dot', color=colors[5])
        fig = draw_line(figure=fig, length=0.2*(4-i)*base, rotation=60, xOrigin=0.2*(i+1)*base+(base+space), yOrigin=0, dash='dot', color=colors[3])
        
        fig = draw_line(figure=fig, length=base, rotation=60, xOrigin=(0.2*(i+1)*base + (base+space))*xPr, yOrigin=((base+space)-(0.2*(i+1)*base))*yPr, dash='dot', color=colors[6])
        fig = draw_line(figure=fig, length=base, rotation=-60, xOrigin=(0.2*(i+1)*base + (base+space))*xPr, yOrigin=((base+space)+(0.2*(i+1)*base))*yPr, dash='dot', color=colors[6])
        
    # tick labels
    annots = []
    for i in range(6):
        annots.append(go.layout.Annotation(x=i*0.2*base, y=0, text=str(100-i*20), font=dict(color=colors[0]), showarrow=False, xanchor='center', yanchor='top'),)
        annots.append(go.layout.Annotation(x=i*0.2*base*xPr, y=i*0.2*base*yPr, text=(i*20), font=dict(color=colors[1]), showarrow=False, xanchor='right', yanchor='bottom'),)
        annots.append(go.layout.Annotation(x=i*0.2*base*xPr+(0.5*base), y=(5-i)*0.2*base*yPr, text=(i*20), font=dict(color=colors[2]), showarrow=False, xanchor='left', yanchor='bottom'),)
        
        annots.append(go.layout.Annotation(x=i*0.2*base+(base+space), y=0, text=str(i*20), font=dict(color=colors[3]), showarrow=False, xanchor='center', yanchor='top'),)
        annots.append(go.layout.Annotation(x=i*0.2*base*xPr+(base+space), y=i*0.2*base*yPr, text=(100-i*20), font=dict(color=colors[4]), showarrow=False, xanchor='right', yanchor='bottom'),)
        annots.append(go.layout.Annotation(x=i*0.2*base*xPr+(1.5*base+space), y=(5-i)*0.2*base*yPr, text=(100-i*20), font=dict(color=colors[5]), showarrow=False, xanchor='left', yanchor='bottom'),)
        
        annots.append(go.layout.Annotation(x=((base+space)+(i*0.2*base))*xPr, y=((base+space)+(i*0.2*base))*yPr, text=(i*20), font=dict(color=colors[6]), showarrow=False, xanchor='right', yanchor='bottom'),)
        annots.append(go.layout.Annotation(x=((3*base+space)-((5-i)*0.2*base))*xPr, y=((base+space)+((5-i)*0.2*base))*yPr, text=(100-i*20), font=dict(color=colors[6]), showarrow=False, xanchor='left', yanchor='bottom'),)
        
    annots.append(go.layout.Annotation(x=(base/2), y=-(0.07*base), text="Calcium", font=dict(color=colors[0]), showarrow=False, xanchor='center', yanchor='top'),)
    annots.append(go.layout.Annotation(x=(base/2)*xPr+2, y=(base/2)*yPr+10, text="Magnesium", font=dict(color=colors[1]), showarrow=False, textangle=-60, xanchor='right', yanchor='middle'),)
    annots.append(go.layout.Annotation(x=base-(base/2*xPr)-5, y=(base/2)*yPr+10, text="Natrium + Kalium", font=dict(color=colors[2]), showarrow=False, textangle=60, xanchor='left', yanchor='middle'),)
    
    annots.append(go.layout.Annotation(x=(base/2+(base+space)), y=-(0.07*base), text="Chloride", font=dict(color=colors[3]), showarrow=False, xanchor='center', yanchor='top'),)
    annots.append(go.layout.Annotation(x=(base/2)*xPr+(base+space)+10, y=(base/2)*yPr+10, text="Carbonate + Bicarbonate", font=dict(color=colors[4]), showarrow=False, textangle=-60, xanchor='right', yanchor='middle'),)
    annots.append(go.layout.Annotation(x=(2*base+space)-(base/2*xPr)+2, y=(base/2)*yPr+10, text="Sulfate", font=dict(color=colors[5]), showarrow=False, textangle=60, xanchor='left', yanchor='middle'),)
    
    annots.append(go.layout.Annotation(x=(1.5*base+space)*xPr+7, y=(1.5*base+space)*yPr+10, text="Sulfate + Chloride", font=dict(color=colors[6]), showarrow=False, textangle=-60, xanchor='right', yanchor='middle'),)
    annots.append(go.layout.Annotation(x=(2*base)-(1.5*base)*xPr+10, y=(1.5*base+space)*yPr+7, text="Calcium + Magnesium", font=dict(color=colors[6]), showarrow=False, textangle=60, xanchor='left', yanchor='middle'),)
    
    fig.update_layout(
        annotations = annots
        )
    
    # canvas config
    bgcolor='aliceblue'
    fig.update_layout(autosize=False, width=canvas_width, height=canvas_height,
                      plot_bgcolor=bgcolor,
                      legend=go.layout.Legend(
                          x=0, y=1, traceorder='normal', bgcolor=bgcolor))
    
    fig.update_xaxes(showticklabels=False, showgrid=False, zeroline=False)
    fig.update_yaxes(showticklabels=False, showgrid=False, zeroline=False)
    
    return fig

def plot_point(fig, x, y, name=''):
    #xPr = math.cos(math.radians(60))
    yPr = math.sin(math.radians(60))
    m1 = math.tan(math.radians(120))
    m2 = math.tan(math.radians(60))
    n = len(x)
    xPlot = []
    yPlot = []
    hovText = []
    xReal=0
    for i in range(n):
        if (x[i]<=100):
            yPlot.append(y[i]*yPr)
            xPlot.append((yPlot[i]/m1)+(100-x[i]))
            xLab = 'Calcium'
            yLab = 'Magnesium'
            zLab = 'Natrium + Kalium'
            hovText.append(xLab+': '+str(x[i])+'%<br>'+yLab+': '+str(y[i])+'%<br>'+zLab+': '+str(100-x[i]-y[i])+'%')
        elif (x[i]>100):
            xReal = x[i] - 100
            yPlot.append(y[i]*yPr)
            xPlot.append((yPlot[i]/m2)+(xReal+135))
            xLab = 'Chloride'
            yLab = 'Sulfate'
            zLab = 'Carbonate + Bicarbonate'
            hovText.append(xLab+': '+str(xReal)+'%<br>'+yLab+': '+str(y[i])+'%<br>'+zLab+': '+str(200-x[i]-y[i])+'%')
        
    fig.add_trace(
        go.Scatter(
            x=xPlot, y=yPlot, mode='markers',
            hovertext=hovText, hoverinfo='text', name=name
            ))
    
    return fig
        