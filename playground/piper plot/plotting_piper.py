import piper_plot_new as pp

colours=['#726da8', '#bd4089', '#6a8d73', '#bb4430', '#70c1b3', '#72779e', '#998b71']

fig_plot = pp.plot_bg(colors=colours)
fig_plot = pp.plot_point(fig=fig_plot, x=[60], y=[30])
fig_plot.show()