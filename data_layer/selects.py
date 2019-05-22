from data_layer.create_db import DatabaseInteraction
from datetime import datetime
# from plotter import Plotter
# will be removed
# from create_db import DatabaseInteraction
# import plotly
# import plotly.graph_objs as go
# from datetime import timedelta


class Extractor:

    def __init__(self, db_name):

        # self.plt = Plotter()
        self.db = DatabaseInteraction(db_name)
# tha pairnei mono to mode mallon kai tha epistrefei o,ti xreiazomai gia na ta steilei stin plotter!

    def extract(self, mode):

        if mode == "get_max_all":
            self.get_max_all()
        elif mode == "get_min_all":
            self.get_min_all()
        elif mode == "get_count_all":
            self.get_count_all()
        elif mode == "get_sum_all":
            self.get_sum_all()
        elif mode == "get_avg_all":
            self.get_avg_all()
        elif mode == "weekly_select":
            weekly = []
            weekly = self.weekly_select()
            return weekly

        elif mode == "monthly_select":
            monthly = []
            monthly = self.monthly_select()
            return monthly

        elif mode == "yearly_select":
            yearly = []
            yearly = self.yearly_select()
            return yearly

        elif mode == "daily_select":
            daily = []
            daily = self.daily_select()
            return daily
        else:
            error = "Something went wrong"
            return error
        # (mode, self.daily_select()[0], self.daily_select()[1], "Daily", "TIME", self.daily_select()[2][0])

    # Get maximum of values by unit

    def get_max_all(self):
        query = "SELECT MAX(VALUE) as MAX, UNIT FROM sensor GROUP BY UNIT"
        max_all = self.db.select_values(query)
        return max_all

    # Get minimum of values by unit

    def get_min_all(self):
        query = "SELECT MIN(VALUE) as MIN, UNIT FROM sensor GROUP BY UNIT"
        min_all = self.db.select_values(query)
        return min_all

    # Get number of rows by unit

    def get_count_all(self):
        query = "SELECT COUNT(*) as COUNT, UNIT FROM sensor GROUP BY UNIT"
        count_all = self.db.select_values(query)
        return count_all

    # Sum of all values by unit

    def get_sum_all(self):
        query = "SELECT SUM(VALUE) as SUM_OF_UNIT_VALUES, UNIT FROM sensor GROUP BY UNIT"
        sum_all = self.db.select_values(query)
        return sum_all

    # Average of the values by unit

    def get_avg_all(self):
        query = "SELECT AVG(VALUE) as AVG_OF_VALUES, UNIT FROM sensor GROUP BY UNIT"
        avg_all = self.db.select_values(query)
        return avg_all

    def select_first_row(self):
        query = "SELECT TIME FROM sensor ORDER BY TIME LIMIT 1"
        first_row = self.db.select_values(query)
        return first_row

    def select_last_row(self):
        query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
        last_row = self.db.select_values(query)
        return last_row

    def weekly_select(self):
        last_date_query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
        last_date = self.db.select_values(last_date_query)

        weekly_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
            last_date[0][0] + "\", '-7 days') AND TIME <= DATETIME(\"" + \
            last_date[0][0] + "\")"
        weekly = self.db.select_values(weekly_query)

        weekly_plot_x = []
        weekly_plot_y = []
        weekly_plot = weekly

        for index1 in range(len(weekly_plot)):
            weekly_plot_x.append(weekly_plot[index1][2])

        for index2 in range(len(weekly_plot)):
            weekly_plot_y.append(int(weekly_plot[index2][1]))

        weekly_datetime_x = []
        for i in range(len(weekly_plot_x)):
            weekly_datetime_x.append(datetime.strptime(
                weekly_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

        return weekly_datetime_x, weekly_plot_y, weekly_plot[0]

    def monthly_select(self):
        query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
        last_date = self.db.select_values(query)

        monthly_query = "SELECT * FROM sensor WHERE TIME >= DATETIME(\"" + \
            last_date[0][0] + "\", 'start of month') AND TIME <= DATETIME(\"" +\
            last_date[0][0] + "\")"

        monthly = self.db.select_values(monthly_query)

        # Here we create the 2 lists that are going to be plotly's arguments
        # monthly
        monthly_plot_x = []
        monthly_plot_y = []
        monthly_plot = monthly

        for i in range(len(monthly_plot)):
            monthly_plot_x.append(monthly_plot[i][2])

        for i in range(len(monthly_plot)):
            monthly_plot_y.append(int(monthly_plot[i][1]))

        monthly_datetime_x = []
        for i in range(len(monthly_plot_x)):
            monthly_datetime_x.append(datetime.strptime(
                monthly_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

        return monthly_datetime_x, monthly_plot_y, monthly[0]

    def yearly_select(self):
        query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
        last_date = self.db.select_values(query)

        yearly_query = "SELECT * FROM sensor WHERE TIME BETWEEN DATETIME(\"" + \
            last_date[0][0] + "\", 'start of year') AND DATETIME(\"" +\
            last_date[0][0] + "\")"

        yearly = self.db.select_values(yearly_query)

        # yearly
        yearly_plot_x = []
        yearly_plot_y = []
        yearly_plot = yearly
        for i in range(len(yearly_plot)):
            yearly_plot_x.append(yearly_plot[i][2])

        for i in range(len(yearly_plot)):
            yearly_plot_y.append(int(yearly_plot[i][1]))

        yearly_datetime_x = []
        for i in range(len(yearly_plot_x)):
            yearly_datetime_x.append(datetime.strptime(
                yearly_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

        return yearly_datetime_x, yearly_plot_y, yearly[0]

    def daily_select(self):
        query = "SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"
        last_date = self.db.select_values(query)

        daily_query = "SELECT * FROM sensor WHERE TIME BETWEEN DATETIME(\"" + \
            last_date[0][0] + "\", '-1 day') AND DATETIME(\"" +\
            last_date[0][0] + "\")"

        daily = self.db.select_values(daily_query)

        # Here we create the 2 lists that are going to be plotly's arguments
        # daily
        daily_plot_x = []
        daily_plot_y = []
        daily_plot = daily
        for i in range(len(daily_plot)):
            daily_plot_x.append(daily_plot[i][2])

        for i in range(len(daily_plot)):
            daily_plot_y.append(int(daily_plot[i][1]))

        daily_datetime_x = []
        for i in range(len(daily_plot_x)):
            daily_datetime_x.append(datetime.strptime(daily_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

        return daily_datetime_x, daily_plot_y, daily[0]


# pp.pprint(monthly_plot_y)


# pp.pprint(yearly_plot_y)
# Create a new list with monthly X axis converted in datetime objects

# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Scatter(
#     x=daily_datetime,
#     y=daily_plot_y,
#     mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[daily_datetime[0]-d,
#                           daily_datetime[-1]+d]
#                    ))
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='daily.html', auto_open=True)
# ---------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Scatter(
#     x=test_datetime,
#     y=monthly_plot_y,
#     mode='lines')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[test_datetime[0]-d,
#                           test_datetime[-1]+d]
#                    ),
#                    title="Alpine_K81_Height",
#                    autosize=True,
#                    annotations=[
#     dict(
#         x=0.5,
#         y=-0.09,
#         showarrow=False,
#         text="nope",
#         xref='paper',
#         yref='paper'
#     ),
#     dict(
#         x=-0.04,
#         y=0.5,
#         showarrow=False,
#         text='Custom y-axis title',
#         textangle=-90,
#         xref='paper',
#         yref='paper'
#     )
# ]
# )
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='monthly.html', auto_open=True)
# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Scatter(
#     x=yearly_datetime,
#     y=yearly_plot_y,
#     mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#     range=[yearly_datetime[0]-d,
#            yearly_datetime[-1]+d]
# ))
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)
# ---------------------------------------------------------------------------------
# d = timedelta(days=1)
# trace1 = go.Bar(
#     x=yearly_datetime,
#     y=yearly_plot_y,
#     # orientation='h'
# )
#
# # mode='markers')
# data = [trace1]
# layout = go.Layout(xaxis=dict(
#                    range=[yearly_datetime[0]-d,
#                           yearly_datetime[-1]+d])
#
#                    # bargap=0.001,
#
#                    )
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)
# ---------------------------------------------------------------------------------
if __name__ == "__main__":

    # plt = Plotter()
    extr = Extractor("sensor_data.db")
    yearly = []
    attemp = []
    yearly = extr.yearly_select()
    attemp = extr.attempt()
    if attemp == yearly:
        print("yes")
    attempt_x = attemp[0]
    # attempt_x.sort(key=lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%fZ"))
    attempt_x.sort()
    # if attemp[0][0] < attemp[0][-1]:
    #     print("yes it is")
    # else:
    #     print("no its not")
    # print(attemp[0])
    # print(len(attemp[1]) == len(attemp[0]))
    d = timedelta(days=1)
    trace1 = go.Scatter(
        x=attempt_x,
        y=attemp[1],
        mode='lines')
    data = [trace1]
    # fig = go.Figure(data=data, layout=layout)
    plotly.offline.plot(data, filename='yearly.html', auto_open=True)
    # plt.plot_data('lines', daily_select()[0], daily_select()[1])
    # plt.scatter_plot('lines+markers', yearly[0], yearly[1], "Daily", "TIME", yearly[2][0])
    # print(daily[0])

# ---------------------------------------------------------------------------------
# data = [
#     go.Bar(
#         y=yearly_plot_y,
#         x=yearly_datetime
#     )
# ]
#
# layout = go.Layout(
#     title='Sampled Results',
#     bargap=0.2)
#
# fig = go.Figure(data=data, layout=layout)
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)

# ---------------------------------------------------------------------------------


# ---- PLOT DATA USING PLOTLY (works but got issues with how it shows the bars) -----

# Store in plot_data the Bar Graphic Object
# plot_data=[go.Bar(x=test_datetime, y=monthly_plot_y)]

# Plot the Bar Graphic Object
# plotly.offline.plot(fig, filename='yearly.html', auto_open=True)

# print(type(monthly_plot_y[0]))

# -----------------------------------------------------------------------------------


# get_max_all()
# get_min_all()
# get_count_all()
# get_sum_all()
# get_avg_all()
# weekly_select()
# "SELECT TIME, CASE WHEN DATETIME(%s, '-7 days') \
#      == DATETIME(%s) THEN 'TRUE' END FROM sensor" % (last_date, wtf)

# """SELECT CASE
#  WHEN DATEDIFF(week, %s, TIME) == 1 THEN 'TRUE'
#  ELSE 'FALSE'
#  END
# , *
# FROM sensor""" % last_date
#

# last_date_query = """SELECT TIME FROM sensor ORDER BY TIME DESC LIMIT 1"""
# last_date = db.select_values(last_date_query)
# print(last_date)

# lista = db.select_all()
# # pp.pprint(lista)
#
# weekly = []
# for dates in range(len(lista)):
#     if datetime.strptime(lista[dates][-1], "%Y-%m-%dT%H:%M:%S.0%fZ") < \
#             datetime.strptime(lista[-1][-1], "%Y-%m-%dT%H:%M:%S.0%fZ"):
#         weekly.append(lista[dates][-1])
#     # dummy = datetime.strptime(lista[date][-1], "%Y-%m-%dT%H:%M:%S.0%fZ")
#
#     # print(lista[dates][-1])
# print(weekly)
#
# """SELECT *
# FROM sensor
# WHERE TIME BETWEEN DATETIME("2015-12-09T18:02:44.000000Z", '-7 days')\
# AND DATETIME ("2015-12-09T18:02:44.000000Z") """
