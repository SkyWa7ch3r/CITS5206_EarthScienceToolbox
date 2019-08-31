import piper_plot_new as pp

colours=['#726da8', '#bd4089', '#6a8d73', '#bb4430', '#70c1b3', '#72779e', '#998b71']

fig_plot = pp.plot_bg(colors=colours)
fig_plot = pp.plot_point(fig=fig_plot, x=[60, 40, 120], y=[30, 10, 80], name='Site 1 blaa bla bal')
fig_plot = pp.plot_point(fig=fig_plot, x=[50, 70, 150], y=[25, 10, 40], name='Site 2')
fig_plot = pp.plot_point(fig=fig_plot, x=[40], y=[40], name='Site 3')
#fig_plot = pp.plot_point(fig=fig_plot, x=[20], y=[60])
#fig_plot = pp.plot_point(fig=fig_plot, x=[20], y=[30])
#fig_plot = pp.plot_point(fig=fig_plot, x=[40], y=[50])
#fig_plot = pp.plot_point(fig=fig_plot, x=[20], y=[80])
#fig_plot = pp.plot_point(fig=fig_plot, x=[20], y=[0])
fig_plot.show()