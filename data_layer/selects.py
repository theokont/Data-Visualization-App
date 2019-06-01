from data_layer.create_db import DatabaseInteraction
from datetime import datetime


class Extractor:

    def __init__(self, db_name):
        self.db = DatabaseInteraction(db_name)

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
        # "SELECT AVG(VALUE) as AVG_OF_VALUES, UNIT FROM sensor GROUP BY UNIT"
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

    def custom_select(self, from_time, to_time):
        custom_query = "SELECT * FROM sensor WHERE TIME BETWEEN  DATE(\"" + \
            from_time + "\") AND DATE(\"" + \
            to_time + "\")"
        custom = self.db.select_values(custom_query)

        custom_plot_x = []
        custom_plot_y = []
        custom_datetime_x = []

        for i in range(len(custom)):
            custom_plot_x.append(custom[i][2])

        for i in range(len(custom)):
            custom_plot_y.append(custom[i][1])

        for i in range(len(custom_plot_x)):
            custom_datetime_x.append(datetime.strptime(
                custom_plot_x[i], "%Y-%m-%dT%H:%M:%S.%fZ"))

        return custom_datetime_x, custom_plot_y, custom[0]

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
