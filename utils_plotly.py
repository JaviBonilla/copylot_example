import numpy as np
import parula as par
import plotly.graph_objs as go


def matplotlib_to_plotly(c_map, pl_entries):
    h = 1.0/(pl_entries-1)
    pl_color_scale = []

    for k in range(pl_entries):
        c = list(map(np.uint8, np.array(c_map(k * h)[:3]) * 255))
        pl_color_scale.append([k*h, 'rgb'+str((c[0], c[1], c[2]))])

    return pl_color_scale


def fig_receiver_flux(m, width, height, title='', z_min=None, z_max=None, show_scale=True, num_digits=4):
    color_scale = matplotlib_to_plotly(par.parula_map, 255)
    base_x = -width * 0.5
    base_y = 0
    len_x = len(m)
    len_y = len(m[0])
    inc_x = width/len_x
    inc_y = height/len_y
    x = [base_x + inc_x * x for x in range(len_x+1)]
    y = [base_y + inc_y * y for y in range(len_y+1)]
    z = [[round(i, 2) for i in row] for row in m]

    hover_text = []
    for yi, yy in enumerate(y):
        hover_text.append([])
        for xi, xx in enumerate(x):
            if yi < len_y and xi < len_x:
                hover = f'x: ({round(x[xi+1], num_digits)}, {round(x[xi], num_digits)}) m<br>' \
                        f'y: ({round(y[yi+1], num_digits)}, {round(y[yi], num_digits)}) m<br>' \
                        f'Flux: {z[xi][yi]} kW/m<sup>2</sup><br>'
                hover_text[-1].append(hover)

    layout = go.Layout(
        plot_bgcolor='white', title=title,
        xaxis=dict(title='Horizontal position (m)', hoverformat=',.2f', ticksuffix=" m",
                   separatethousands=True, showgrid=False),
        yaxis=dict(title='Vertical position (m)', hoverformat=',.2f', ticksuffix=" m",
                   separatethousands=True, scaleanchor='x', showgrid=False))
    trace = go.Heatmap(x=x, y=y, z=z, showscale=show_scale, colorscale=color_scale, colorbar={"title": 'Incident flux'},
                       hoverinfo='text', hovertext=hover_text)
    fig = go.Figure(data=[trace], layout=layout)
    fig.update_traces(colorbar_ticksuffix=' kW/m<sup>2</sup>', selector=dict(type='heatmap'))
    fig.update_xaxes(autorange="reversed")
    if z_min is not None and z_max is not None:
        fig.data[0].update(zmin=z_min, zmax=z_max)

    return fig
