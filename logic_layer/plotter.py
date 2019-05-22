import plotly
import plotly.graph_objs as go
from datetime import timedelta


class Plotter:

    def __init__(self):
        self.d = timedelta(days=1)

    def daily_plot(self, mode, x, y):
        self.graphic_object = go.Scatter(
            x=x,
            y=y,
            mode=mode)
        self.data = [self.graphic_object]

        self.layout = go.Layout(xaxis=dict(
            range=[x[0]-self.d,
                   x[-1]+self.d]
        ))

        self.fig = go.Figure(data=self.data, layout=self.layout)
        plotly.offline.plot(self.fig, filename='daily.html', auto_open=True)

    def scatter_plot(self, mode, x, y, title, x_axis_title, y_axis_title):
        self.graphic_object = go.Scatter(
            x=x,
            y=y,
            mode=mode)
        self.data = [self.graphic_object]

        self.layout = go.Layout(xaxis=dict(
            range=[x[0]-self.d,
                   x[-1]+self.d]),
            title=title,
            autosize=True,
            annotations=[
            dict(
                x=0.5,
                y=-0.065,
                showarrow=False,
                text=x_axis_title,
                xref='paper',
                yref='paper'
            ),
            dict(
                x=-0.03,
                y=0.5,
                showarrow=False,
                text="UNIT - {}".format(y_axis_title),
                textangle=-90,
                xref='paper',
                yref='paper')
        ])
        self.fig = go.Figure(data=self.data, layout=self.layout)
        plotly.offline.plot(self.fig, filename="%s.html" % title, auto_open=True)

    def yearly_plot(self, mode, x, y, title, x_axis_title, y_axis_title):
        self.graphic_object = go.Scatter(
            x=x,
            y=y,
            mode=mode)
        self.data = [self.graphic_object]

        self.layout = go.Layout(xaxis=dict(
            range=[x[0]-self.d,
                   x[-1]+self.d]),
            title=title,
            autosize=True,
            annotations=[
            dict(
                x=0.5,
                y=-0.09,
                showarrow=False,
                text=x_axis_title,
                xref='paper',
                yref='paper'
            ),
            dict(
                x=-0.04,
                y=0.5,
                showarrow=False,
                text="UNIT - %s" % y_axis_title,
                textangle=-90,
                xref='paper',
                yref='paper')
        ])
        self.fig = go.Figure(data=self.data, layout=self.layout)
        plotly.offline.plot(self.fig, filename='yearly.html', auto_open=True)
