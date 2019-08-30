import piper_plot as pp

fig = pp.plot_background(triangle_base_length = 5)
fig = pp.plot_point(x=[25], y=[47], fig=fig, triangle_base_length = 5)
fig.show()