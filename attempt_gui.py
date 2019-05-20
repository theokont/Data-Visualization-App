# let this be my example for multi layer Gui

from PySide2.QtCore import QDate, QLocale, Qt
# from PySide2 import QtCore
from PySide2.QtGui import QFont, QTextCharFormat
from PySide2.QtWidgets import (QApplication, QCalendarWidget, QCheckBox,
                               QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLayout, QWidget, QPushButton, QMainWindow, QLineEdit, QVBoxLayout,
                               QMessageBox)
from datetime import datetime
import os
from data_layer.selects import Extractor
import sys
from data_layer.create_db import DatabaseInteraction
from logic_layer.parse_script import XMLImporter
from logic_layer.plotter import Plotter


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createCalendarBox()
        self.setup_database_dialog()
        self.database_utilities()
        self.ready_plots()

        layout = QGridLayout()
        layout.addWidget(self.db_dialog_groupbox, 0, 0)
        layout.addWidget(self.previewGroupBox, 0, 1)
        layout.addWidget(self.db_util_groupbox, 1, 0)
        layout.addWidget(self.ready_plt_groupbox, 1, 1)

        # layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)
        self.previewLayout.setRowMinimumHeight(0,
                                               self.calendar.sizeHint().height())
        self.previewLayout.setColumnMinimumWidth(0,
                                                 self.calendar.sizeHint().width())

        self.setWindowTitle("Data Visualization Application")

    def createCalendarBox(self):
        extr = Extractor("sensor_data.db")
        # Create datetime objects of the first and last strings of date
        self.datetime_first = datetime.strptime(extr.select_first_row()[
            0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.datetime_last = datetime.strptime(extr.select_last_row()[
            0][0], "%Y-%m-%dT%H:%M:%S.%fZ")

        self.previewGroupBox = QGroupBox("Custom Plot")

        self.calendar = QCalendarWidget()
        self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
        self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
        self.calendar.setMinimumDate(self.first_row)
        self.calendar.setMaximumDate(self.last_row)
        self.calendar.setGridVisible(True)

        # Create main layout
        self.previewLayout = QGridLayout()
        # Creating sub layouts and adding their widgets
        self.cal_options = QGridLayout()

        self.chart_label = QLabel("&Chart")
        self.chart_field = QComboBox()
        self.chart_field.addItem("Lines")
        self.chart_field.addItem("Lines and Markers")
        self.chart_field.addItem("Scatter")
        self.chart_field.addItem("Bars")
        self.chart_label.setBuddy(self.chart_field)

        # Mode Layout
        self.h_mode_layout = QHBoxLayout()
        self.h_mode_layout.addWidget(self.chart_label)
        self.h_mode_layout.addWidget(self.chart_field)

        self.from_to_dates_layout = QVBoxLayout()

        # From Layout
        self.from_date_layout = QHBoxLayout()
        self.from_date_label = QLabel("From")
        self.from_date = QDateEdit()
        self.update_from_date = QPushButton("Update Date")
        self.from_date.setDisplayFormat('MMM d yyyy')
        self.from_date.setDate(self.calendar.selectedDate())
        self.update_from_date.clicked.connect(self.from_selectedDateChanged)
        # self.calendar.selectionChanged.connect(self.from_selectedDateChanged)

        # Adds widgets to from_date_layout QHBoxLayout
        self.from_date_layout.addWidget(self.from_date)
        self.from_date_layout.addWidget(self.update_from_date)

        # To layout
        self.to_date_layout = QHBoxLayout()
        self.to_date_label = QLabel("To")
        self.to_date = QDateEdit()
        self.update_to_date = QPushButton("Update Date")
        self.to_date.setDisplayFormat('MMM d yyyy')
        self.to_date.setDate(self.calendar.selectedDate())
        self.update_to_date.clicked.connect(self.to_selectedDateChanged)

        # Adds widgets to to_date_layout QHBoxLayout
        self.to_date_layout.addWidget(self.to_date)
        self.to_date_layout.addWidget(self.update_to_date)

        # self.calendar.selectionChanged.connect(self.to_selectedDateChanged)

        # Add widgets and QHBoxLayout to our QVBoxLayout
        self.from_to_dates_layout.addWidget(self.from_date_label)
        self.from_to_dates_layout.addLayout(self.from_date_layout)
        self.from_to_dates_layout.addWidget(self.to_date_label)
        self.from_to_dates_layout.addLayout(self.to_date_layout)

        self.custom_plot_button = QPushButton("Custom Plot")

        self.cal_options.addLayout(self.h_mode_layout, 0, 0)
        self.cal_options.addLayout(self.from_to_dates_layout, 1, 0)
        self.cal_options.addWidget(self.custom_plot_button, 2, 0)
        # self.cal_options.setAlignment(Qt.AlignRight)

        # self.calendar.currentPageChanged.connect(self.reformatCalendarPage)

        # Add widgets and sub layout to main layout
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
        self.previewLayout.addLayout(self.cal_options, 0, 1)
        self.previewGroupBox.setLayout(self.previewLayout)

    def setup_database_dialog(self):
        # Create Groupbox
        self.db_dialog_groupbox = QGroupBox("Database Creation and Data Import")

        # Create widgets

        self.db_label = QLabel("Provide a name for the database, e.g. sensor_db.db")
        self.path_label = QLabel("Provide path to search for .xml files")
        # self.unit_label = QLabel("Provide the unit of the measurements")

        # self.unit_field = QLineEdit("unit")
        self.db_field = QLineEdit("sensor_db.db")
        self.path_field = QLineEdit(str(os.path.dirname(os.path.realpath(__file__))))
        self.button = QPushButton("Get started")

        # Create layout and add widgets
        self.db_dialog_layout = QVBoxLayout()
        # self.db_dialog_layout.addWidget(self.unit_label)
        # self.db_dialog_layout.addWidget(self.unit_field)
        self.db_dialog_layout.addWidget(self.db_label)
        self.db_dialog_layout.addWidget(self.db_field)
        self.db_dialog_layout.addWidget(self.path_label)
        self.db_dialog_layout.addWidget(self.path_field)
        self.db_dialog_layout.addWidget(self.button)

        # Set dialog layout
        self.db_dialog_groupbox.setLayout(self.db_dialog_layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.run_script)

    def run_script(self):
        error = "Error parsing files or path"
        db = self.db_field.text()
        db_interaction = DatabaseInteraction(db)  # returns object of class DatabaseInteraction
        # unit = self.unit_field.text()
        path = self.path_field.text()
        xml_importer = XMLImporter(db_interaction, path)
        try:
            success = xml_importer.import_xml()
        except Exception as ex:
            success = False
            error = ex
        msg = QMessageBox()

        if success:
            msg.setIcon(QMessageBox.Information)
            msg.setText("Database import successful")
            msg.setInformativeText("The database: {0} has been created.".format(db))
            msg.setWindowTitle("Database imported!")
            msg.setDetailedText("The details are as follows:\nDatabase \
            name: {0}\nUnit of sensors: {1}\nPath of .xml "
                                "files: {2}".format(db, unit, path))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Database import failed!")
            msg.setInformativeText("Creation of the database: {0} failed!".format(db))
            msg.setWindowTitle("Database import failed!")
            msg.setDetailedText("ERROR:\n {0}".format(error))
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort)

        # retval = msg.exec_()
        msg.show()

    def database_utilities(self):
        # Create Groupbox
        self.db_util_groupbox = QGroupBox("Database Utilities")

        # Create Widgets
        self.db_update_field = QLineEdit("example.db")
        self.db_update_label = QLabel("Enter the Database you wish to update")
        self.path_label = QLabel("Xml File Path")
        self.path_field = QLineEdit(str(os.path.dirname(os.path.realpath(__file__))))
        self.update_button = QPushButton("Update")
        self.update_title = QLabel("Update Database")
        self.db_clear_field = QLineEdit("example.db")
        self.db_clear_label = QLabel("Enter Database name")
        self.clear_button = QPushButton("Clear Table")
        self.clear_title = QLabel("Clear the table of a Database")

        # Add Widgets

        self.db_util_db_update = QHBoxLayout()
        self.db_util_db_update.addWidget(self.db_update_label)
        self.db_util_db_update.addWidget(self.db_update_field)

        self.db_util_path = QHBoxLayout()
        self.db_util_path.addWidget(self.path_label)
        self.db_util_path.addWidget(self.path_field)

        self.db_util_clear = QHBoxLayout()
        self.db_util_clear.addWidget(self.db_clear_label)
        self.db_util_clear.addWidget(self.db_clear_field)

        self.db_util_vbox_layout = QVBoxLayout()
        self.db_util_vbox_layout.addWidget(self.update_title)
        self.db_util_vbox_layout.addLayout(self.db_util_db_update)
        self.db_util_vbox_layout.addLayout(self.db_util_path)
        self.db_util_vbox_layout.addWidget(self.update_button)
        self.db_util_vbox_layout.addWidget(self.clear_title)
        self.db_util_vbox_layout.addLayout(self.db_util_clear)
        self.db_util_vbox_layout.addWidget(self.clear_button)

        # Set dialog layout
        self.db_util_groupbox.setLayout(self.db_util_vbox_layout)

    def ready_plots(self):
        # Create Groupbox
        self.ready_plt_groupbox = QGroupBox("Ready-to-use plots")

        # Create Widgets
        self.choose_db_label = QLabel(
            "Provide the database that contains the data you wish to plot")
        self.choose_db_field = QLineEdit("example.db")
        self.chart_label = QLabel("Chart")
        self.chart_field = QComboBox()
        self.chart_field.addItem("Lines")
        self.chart_field.addItem("Lines and Markers")
        self.chart_field.addItem("Scatter")
        self.chart_field.addItem("Bars")
        self.plot_mode_label = QLabel("Choose what chronic period to plot")
        self.plot_mode_field = QComboBox()
        self.plot_mode_field.addItem("Daily")
        self.plot_mode_field.addItem("Weekly")
        self.plot_mode_field.addItem("Monthly")
        self.plot_mode_field.addItem("Yearly")
        self.plot_button = QPushButton("Plot")

        # Add Widgets
        self.plot_vbox_layout = QVBoxLayout()
        self.plot_vbox_layout.addWidget(self.choose_db_label)
        self.plot_vbox_layout.addWidget(self.choose_db_field)
        self.plot_vbox_layout.addWidget(self.chart_label)
        self.plot_vbox_layout.addWidget(self.chart_field)
        self.plot_vbox_layout.addWidget(self.plot_mode_label)
        self.plot_vbox_layout.addWidget(self.plot_mode_field)
        self.plot_vbox_layout.addWidget(self.plot_button)

        # Set layout to groupbox
        self.ready_plt_groupbox.setLayout(self.plot_vbox_layout)
        self.plot_button.clicked.connect(self.ready_plot_script)

    def from_selectedDateChanged(self):
        self.from_date.setDate(self.calendar.selectedDate())

    def to_selectedDateChanged(self):
        self.to_date.setDate(self.calendar.selectedDate())

    def ready_plot_script(self):
        db = self.choose_db_field.text()
        extr = Extractor(db)
        plt = Plotter()
        # db_interaction = DatabaseInteraction(db)  # returns object of class DatabaseInteraction
        if self.chart_field == "Lines":
            chart_mode = "lines"
        elif self.chart_field == "Lines and Markers":
            chart_mode = "lines+markers"
        elif self.chart_field == "Scatter":
            chart_mode = "markers"
        else:
            cm_error = "Something went wrong"
            # return cm_error
            pass

        if self.plot_mode_field == "Daily":
            plot_mode = "daily_select"
        elif self.plot_mode_field == "Weekly":
            plot_mode = "weekly_select"
        elif self.plot_mode_field == "Monthly":
            plot_mode = "monthly_select"
        elif self.plot_mode_field == "Yearly":
            plot_mode = "yearly_select"
        else:
            pm_error = "Something went wrong"
            # return pm_error
            pass

        plot_lists = []
        # Extract from the database the data for x-y axis and the unit
        plot_mode = "monthly_select"
        chart_mode = "lines+markers"
        plot_lists = extr.extract(plot_mode)
        # print(plot_lists[0])
        # print("------------------------------------------------------------")
        # print(plot_lists[1])
        # print(plot_lists[2][0])
        plt.scatter_plot(chart_mode, plot_lists[0], plot_lists[1], db, "TIME", plot_lists[2][0])


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
