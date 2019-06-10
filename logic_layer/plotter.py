import plotly
import plotly.graph_objs as go
from datetime import timedelta


class Plotter:

    def __init__(self):
        self.d = timedelta(days=1)

    def go_bar(self, mode, x, y, title):
        self.graphic_bar_object = go.Bar(
            x=x,
            y=y,
            name=title[:-3]
        )

        return self.graphic_bar_object

    def go_bar_plot(self, title, x_axis_title, y_axis_title, data):
        self.layout = go.Layout(
            title=title,
            autosize=True,
            annotations=[
                dict(
                    x=0.5,
                    y=-0.15,  # -0.065
                    showarrow=False,
                    text=x_axis_title,
                    xref='paper',
                    yref='paper'
                ),
                dict(
                    x=-0.1,  # -0.03
                    y=0.5,
                    showarrow=False,
                    text="UNIT - {}".format(y_axis_title),
                    textangle=-90,
                    xref='paper',
                    yref='paper')
            ],


            barmode='group',
            bargap=0.15,
            bargroupgap=0.1
        )

        self.fig = go.Figure(data=data, layout=self.layout)
        plotly.offline.plot(self.fig, filename="%s.html" % title, auto_open=True)

    def go_scatter(self, mode, x, y, title):
        self.graphic_object = go.Scatter(
            x=x,
            y=y,
            mode=mode,
            name=title[:-3])
        # self.data = [self.graphic_object]

        return self.graphic_object

    def go_plot(self, title, x_axis_title, y_axis_title, data):

        self.layout = go.Layout(  # xaxis=dict(
            # range=[x[0]-self.d,
            #        x[-1]+self.d]),
            title=title,
            autosize=True,
            annotations=[
                dict(
                    x=0.5,
                    y=-0.15,  # -0.065
                    showarrow=False,
                    text=x_axis_title,
                    xref='paper',
                    yref='paper'
                ),
                dict(
                    x=-0.1,  # -0.03
                    y=0.5,
                    showarrow=False,
                    text="UNIT - {}".format(y_axis_title),
                    textangle=-90,
                    xref='paper',
                    yref='paper')
            ])

        self.fig = go.Figure(data=data, layout=self.layout)
        plotly.offline.plot(self.fig, filename="%s.html" % title, auto_open=True)

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

    def bar_plot(self, x, y, title, x_axis_title, y_axis_title):
        self.graphic_object = go.Bar(
            x=x,
            y=y)
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
