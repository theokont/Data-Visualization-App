from PySide2.QtCore import QDate, Qt, QStringListModel
from PySide2.QtWidgets import (QApplication, QCalendarWidget,
                               QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
                               QLayout, QWidget, QPushButton, QLineEdit, QVBoxLayout,
                               QMessageBox)
from datetime import datetime
import os
from data_layer.selects import Extractor
import sys
from data_layer.create_db import DatabaseInteraction
from logic_layer.parse_script import XMLImporter
from logic_layer.plotter import Plotter
import pyperclip


class Window(QWidget):
    go_list = []
    unit = None

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

        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(layout)
        self.previewLayout.setRowMinimumHeight(0,
                                               self.calendar.sizeHint().height())
        self.previewLayout.setColumnMinimumWidth(0,
                                                 self.calendar.sizeHint().width())

        self.setWindowTitle("Data Visualization Application")

    def createCalendarBox(self):
        self.previewGroupBox = QGroupBox("Custom Plot")

        # db_entry_layout
        self.db_entry_layout = QHBoxLayout()
        self.db_entry_field = QLineEdit("tasos.db")
        self.db_entry_label = QLabel("Set Sensor")
        self.db_entry_set_button = QPushButton("Set")

        # Create available db QComboBox
        self.avail_db_combo = QComboBox()
        self.avail_db_combo.addItems(self.available_db_combo())
        self.avail_db_combo_reload = QPushButton("Reload")

        # Create QHBoxLayout for avail_db_combo
        self.avail_db_combo_layout = QHBoxLayout()
        # self.avail_db_combo_layout.addWidget(self.avail_db_combo)
        # self.avail_db_combo_layout.addWidget(self.avail_db_combo_reload)

        # Adds widgets to db_entry_ayout QHBoxLayout
        self.db_entry_layout.addWidget(self.db_entry_label)
        # self.db_entry_layout.addWidget(self.db_entry_field)
        self.db_entry_layout.addWidget(self.avail_db_combo)
        self.db_entry_layout.addWidget(self.avail_db_combo_reload)
        self.db_entry_layout.addWidget(self.db_entry_set_button)

        self.db_entry_set_button.clicked.connect(self.set_db_entry_button_script)

        # Calendar Widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)

        # Create main layout
        self.previewLayout = QGridLayout()

        # Creating sub layouts and adding their widgets
        self.cal_options = QGridLayout()

        self.chart_label = QLabel("&Chart")
        self.calendar_chart_field = QComboBox()
        self.calendar_chart_field.addItem("Lines")
        self.calendar_chart_field.addItem("Lines and Markers")
        self.calendar_chart_field.addItem("Scatter")
        self.calendar_chart_field.addItem("Bars")
        self.chart_label.setBuddy(self.calendar_chart_field)

        # Mode Layout
        self.h_mode_layout = QHBoxLayout()
        self.h_mode_layout.addWidget(self.chart_label)
        self.h_mode_layout.addWidget(self.calendar_chart_field)

        self.from_to_dates_layout = QVBoxLayout()

        # From Layout
        self.from_date_layout = QHBoxLayout()
        self.from_date_label = QLabel("From")
        self.from_date = QDateEdit()
        self.update_from_date = QPushButton("Set Date")
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
        self.update_to_date = QPushButton("Set Date")
        self.to_date.setDisplayFormat('MMM d yyyy')
        self.to_date.setDate(self.calendar.selectedDate())
        self.update_to_date.clicked.connect(self.to_selectedDateChanged)

        # Multiple graphic objects layout
        self.multi_go_label = QLabel("Plot multiple graph objects")
        self.multi_go_layout = QHBoxLayout()
        self.multi_go_add_button = QPushButton("Add Graph Object")
        self.multi_go_clear_button = QPushButton("Clear Graph Objects")
        self.multi_go_plot_button = QPushButton("Plot Graph Objects")

        # Adds widges to multi_go_layout
        self.multi_go_layout.addWidget(self.multi_go_add_button)
        self.multi_go_layout.addWidget(self.multi_go_clear_button)
        # self.multi_go_layout.addWidget(self.multi_go_plot_button)

        # Adds widgets to to_date_layout QHBoxLayout
        self.to_date_layout.addWidget(self.to_date)
        self.to_date_layout.addWidget(self.update_to_date)

        # Add widgets and QHBoxLayout to our QVBoxLayout
        self.from_to_dates_layout.addWidget(self.from_date_label)
        self.from_to_dates_layout.addLayout(self.from_date_layout)
        self.from_to_dates_layout.addWidget(self.to_date_label)
        self.from_to_dates_layout.addLayout(self.to_date_layout)

        self.custom_plot_button = QPushButton("Custom Plot")

        # self.available_db_combo()

        # self.cal_options.addLayout(self.avail_db_combo_layout, 0, 0)
        self.cal_options.addLayout(self.db_entry_layout, 0, 0)
        self.cal_options.addLayout(self.h_mode_layout, 1, 0)
        self.cal_options.addLayout(self.from_to_dates_layout, 2, 0)
        self.cal_options.addWidget(self.custom_plot_button, 3, 0)

        self.multi_qvbox_layout = QVBoxLayout()
        self.multi_qvbox_layout.addWidget(self.multi_go_label)
        self.multi_qvbox_layout.addLayout(self.multi_go_layout)
        self.multi_qvbox_layout.addWidget(self.multi_go_plot_button)

        self.avail_db_combo_reload.clicked.connect(self.reload_db_combo)
        self.custom_plot_button.clicked.connect(self.custom_plot_script)
        # Connect multi_go buttons
        self.multi_go_add_button.clicked.connect(self.add_go_script)
        self.multi_go_clear_button.clicked.connect(self.clear_go_script)
        self.multi_go_plot_button.clicked.connect(self.multi_go_plot_script)

        # Create QVBoxLayout that contains a QHBoxLayout with min,max,avg,count,sum
        self.stats_label = QLabel("Get Stats from The Selected Sensor and Dates")
        self.max = QPushButton("Get Max")
        self.min = QPushButton("Get Min")
        self.avg = QPushButton("Get Average")
        self.count = QPushButton("Get Count Of Measurements")
        self.sum = QPushButton("Get Total Sum")
        self.avg_to_max = QPushButton("Get Count Between Avg-Max")

        self.stats_first_qhbox_layout = QHBoxLayout()
        self.stats_first_qhbox_layout.addWidget(self.min)
        self.stats_first_qhbox_layout.addWidget(self.max)
        self.stats_first_qhbox_layout.addWidget(self.avg)

        self.stats_second_qhbox_layout = QHBoxLayout()
        self.stats_second_qhbox_layout.addWidget(self.count)
        self.stats_second_qhbox_layout.addWidget(self.sum)
        self.stats_second_qhbox_layout.addWidget(self.avg_to_max)

        self.stats_qvbox_layout = QVBoxLayout()
        self.stats_qvbox_layout.addWidget(self.stats_label)
        self.stats_qvbox_layout.addLayout(self.stats_first_qhbox_layout)
        self.stats_qvbox_layout.addLayout(self.stats_second_qhbox_layout)

        # Connect stats buttons when clicked
        self.min.clicked.connect(self.get_min_script)
        self.max.clicked.connect(self.get_max_script)
        self.avg.clicked.connect(self.get_avg_script)
        self.count.clicked.connect(self.get_count_script)
        self.sum.clicked.connect(self.get_sum_script)
        self.avg_to_max.clicked.connect(self.get_avg_to_max_count_script)

        # Add widgets and sub layout to main layout
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignTop)  # , Qt.AlignCenter
        self.previewLayout.addLayout(self.cal_options, 0, 1)
        self.previewLayout.addLayout(self.stats_qvbox_layout, 1, 0)
        self.previewLayout.addLayout(self.multi_qvbox_layout, 1, 1)
        self.previewGroupBox.setLayout(self.previewLayout)

    def get_avg_to_max_count_script(self):
        avgToMax_from_date = str(self.from_date.date().toPython())
        avgToMax_to_date = str(self.to_date.date().toPython())
        avgToMax_error = "Something went wrong while retrieving the percentage"
        avgToMax_db = self.avail_db_combo.currentText() + ".db"
        avgToMax_extr = Extractor(avgToMax_db)

        try:
            total_count = avgToMax_extr.get_count(avgToMax_from_date, avgToMax_to_date)
            avgToMax_avg = avgToMax_extr.get_avg(avgToMax_from_date, avgToMax_to_date)
            avgToMax_max = avgToMax_extr.get_max(avgToMax_from_date, avgToMax_to_date)
            atm_avg = avgToMax_avg[0][0]
            atm_max = avgToMax_max[0][0]
            avgToMax_count = avgToMax_extr.get_avg_to_max_count(
                str(atm_avg), str(atm_max), avgToMax_from_date, avgToMax_to_date)
            avgToMax_percentage = (avgToMax_count[0][0]/total_count[0][0])
            print(avgToMax_count[0][0], total_count[0][0])
            avgToMax_success = True
        except Exception as ex:
            avgToMax_success = False
            avgToMax_error = ex
        avgToMax_msg = QMessageBox()

        if avgToMax_success:
            avgToMax_msg.setIcon(QMessageBox.Information)
            avgToMax_msg.setText(
                "Percentage of values between average and max for the selected sensor and dates")
            avgToMax_msg.setInformativeText(
                "Avg to Max percentage: {0} %".format(avgToMax_percentage*100))
            avgToMax_msg.setWindowTitle("Avg to Max percentage")
            copy_avgToMax_to_clip = avgToMax_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            avgToMax_msg.setStandardButtons(QMessageBox.Close)
            avgToMax_msg.setDefaultButton(copy_avgToMax_to_clip)
        else:
            avgToMax_msg.setIcon(QMessageBox.Critical)
            avgToMax_msg.setText("Getting Avg to Max Percentage Failed!")
            avgToMax_msg.setInformativeText(
                "Getting Avg to Max percentage from {0} failed!".format(self.avail_db_combo.currentText()))
            avgToMax_msg.setWindowTitle("ERROR!")
            avgToMax_msg.setDetailedText("ERROR:\n {0}".format(avgToMax_error))
            avgToMax_msg.setStandardButtons(QMessageBox.Abort)

        avgToMax_retval = avgToMax_msg.exec_()
        copy_avgToMax_to_clip.clicked.connect(self.copy_to_clipboard(avgToMax_percentage))
        avgToMax_msg.show()

    def get_sum_script(self):
        sum_from_date = str(self.from_date.date().toPython())
        sum_to_date = str(self.to_date.date().toPython())
        sum_error = "Something went wrong while retrieving sum"
        sum_db = self.avail_db_combo.currentText() + ".db"
        sum_extr = Extractor(sum_db)

        try:
            sum_stat = sum_extr.get_sum(sum_from_date, sum_to_date)
            sum_success = True
        except Exception as ex:
            sum_success = False
            sum_error = ex
        sum_msg = QMessageBox()

        if sum_success:
            sum_msg.setIcon(QMessageBox.Information)
            sum_msg.setText("Sum value for the selected sensor and dates")
            sum_msg.setInformativeText(
                "Sum value: {0}".format(sum_stat[0][0]))
            sum_msg.setWindowTitle("sum Value")
            copy_sum_to_clip = sum_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            sum_msg.setStandardButtons(QMessageBox.Close)
            sum_msg.setDefaultButton(copy_sum_to_clip)
        else:
            sum_msg.setIcon(QMessageBox.Critical)
            sum_msg.setText("Getting Sum Value Failed!")
            sum_msg.setInformativeText(
                "Getting sum value from {0} failed!".format(self.avail_db_combo.currentText()))
            sum_msg.setWindowTitle("ERROR!")
            sum_msg.setDetailedText("ERROR:\n {0}".format(sum_error))
            sum_msg.setStandardButtons(QMessageBox.Abort)

        sum_retval = sum_msg.exec_()
        copy_sum_to_clip.clicked.connect(self.copy_to_clipboard(sum_stat[0][0]))
        sum_msg.show()

    def get_count_script(self):
        count_from_date = str(self.from_date.date().toPython())
        count_to_date = str(self.to_date.date().toPython())
        count_error = "Something went wrong while retrieving count"
        count_db = self.avail_db_combo.currentText() + ".db"
        count_extr = Extractor(count_db)

        try:
            count_stat = count_extr.get_count(count_from_date, count_to_date)
            count_success = True
        except Exception as ex:
            count_success = False
            count_error = ex
        count_msg = QMessageBox()

        if count_success:
            count_msg.setIcon(QMessageBox.Information)
            count_msg.setText("Count value for the selected sensor and dates")
            count_msg.setInformativeText(
                "count value: {0}".format(count_stat[0][0]))
            count_msg.setWindowTitle("Count Value")
            copy_count_to_clip = count_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            count_msg.setStandardButtons(QMessageBox.Close)
            count_msg.setDefaultButton(copy_count_to_clip)
        else:
            count_msg.setIcon(QMessageBox.Critical)
            count_msg.setText("Getting Count Value Failed!")
            count_msg.setInformativeText(
                "Getting count value from {0} failed!".format(self.avail_db_combo.currentText()))
            count_msg.setWindowTitle("ERROR!")
            count_msg.setDetailedText("ERROR:\n {0}".format(count_error))
            count_msg.setStandardButtons(QMessageBox.Abort)

        count_retval = count_msg.exec_()
        copy_count_to_clip.clicked.connect(self.copy_to_clipboard(count_stat[0][0]))
        count_msg.show()

    def get_avg_script(self):
        avg_from_date = str(self.from_date.date().toPython())
        avg_to_date = str(self.to_date.date().toPython())
        avg_error = "Something went wrong while retrieving avg"
        avg_db = self.avail_db_combo.currentText() + ".db"
        avg_extr = Extractor(avg_db)

        try:
            avg_stat = avg_extr.get_avg(avg_from_date, avg_to_date)
            avg_success = True
        except Exception as ex:
            avg_success = False
            avg_error = ex
        avg_msg = QMessageBox()

        if avg_success:
            avg_msg.setIcon(QMessageBox.Information)
            avg_msg.setText("Avg value for the selected sensor and dates")
            avg_msg.setInformativeText(
                "Avg value: {0}".format(avg_stat[0][0]))
            avg_msg.setWindowTitle("Avg Value")
            copy_avg_to_clip = avg_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            avg_msg.setStandardButtons(QMessageBox.Close)
            avg_msg.setDefaultButton(copy_avg_to_clip)
        else:
            avg_msg.setIcon(QMessageBox.Critical)
            avg_msg.setText("Getting Avg Value Failed!")
            avg_msg.setInformativeText(
                "Getting avg value from {0} failed!".format(self.avail_db_combo.currentText()))
            avg_msg.setWindowTitle("ERROR!")
            avg_msg.setDetailedText("ERROR:\n {0}".format(avg_error))
            avg_msg.setStandardButtons(QMessageBox.Abort)

        avg_retval = avg_msg.exec_()
        copy_avg_to_clip.clicked.connect(self.copy_to_clipboard(avg_stat[0][0]))
        avg_msg.show()

    def get_max_script(self):
        max_from_date = str(self.from_date.date().toPython())
        max_to_date = str(self.to_date.date().toPython())
        max_error = "Something went wrong while retrieving max"
        max_db = self.avail_db_combo.currentText() + ".db"
        max_extr = Extractor(max_db)

        try:
            max_stat = max_extr.get_max(max_from_date, max_to_date)
            max_success = True
        except Exception as ex:
            max_success = False
            max_error = ex
        max_msg = QMessageBox()

        if max_success:
            max_msg.setIcon(QMessageBox.Information)
            max_msg.setText("Max value for the selected sensor and dates")
            max_msg.setInformativeText(
                "Max value: {0}".format(max_stat[0][0]))
            max_msg.setWindowTitle("Max Value")
            copy_max_to_clip = max_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            max_msg.setStandardButtons(QMessageBox.Close)
            max_msg.setDefaultButton(copy_max_to_clip)
        else:
            max_msg.setIcon(QMessageBox.Critical)
            max_msg.setText("Getting Max Value Failed!")
            max_msg.setInformativeText(
                "Getting max value from {0} failed!".format(self.avail_db_combo.currentText()))
            max_msg.setWindowTitle("ERROR!")
            max_msg.setDetailedText("ERROR:\n {0}".format(max_error))
            max_msg.setStandardButtons(QMessageBox.Abort)

        max_retval = max_msg.exec_()
        copy_max_to_clip.clicked.connect(self.copy_to_clipboard(max_stat[0][0]))
        max_msg.show()

    def get_min_script(self):
        min_from_date = str(self.from_date.date().toPython())
        min_to_date = str(self.to_date.date().toPython())
        min_error = "Something went wrong while retrieving min"
        min_db = self.avail_db_combo.currentText() + ".db"
        min_extr = Extractor(min_db)

        try:
            min_stat = min_extr.get_min(min_from_date, min_to_date)
            min_success = True
        except Exception as ex:
            min_success = False
            min_error = ex
        min_msg = QMessageBox()

        if min_success:
            min_msg.setIcon(QMessageBox.Information)
            min_msg.setText("Min value for the selected sensor and dates")
            min_msg.setInformativeText(
                "Min value: {0}".format(min_stat[0][0]))
            min_msg.setWindowTitle("Min Value")
            copy_min_to_clip = min_msg.addButton(
                self.tr("Copy to clipboard"), QMessageBox.AcceptRole)
            min_msg.setStandardButtons(QMessageBox.Close)
            min_msg.setDefaultButton(copy_min_to_clip)
        else:
            min_msg.setIcon(QMessageBox.Critical)
            min_msg.setText("Getting Min Value Failed!")
            min_msg.setInformativeText(
                "Getting min value from {0} failed!".format(self.avail_db_combo.currentText()))
            min_msg.setWindowTitle("ERROR!")
            min_msg.setDetailedText("ERROR:\n {0}".format(min_error))
            min_msg.setStandardButtons(QMessageBox.Abort)

        min_retval = min_msg.exec_()
        copy_min_to_clip.clicked.connect(self.copy_to_clipboard(min_stat[0][0]))
        min_msg.show()

    def copy_to_clipboard(self, var):
        pyperclip.copy(var)

    def add_go_script(self):

        current_index_chart = self.calendar_chart_field.currentIndex()
        if current_index_chart == 0:
            chart_mode = "lines"
        elif current_index_chart == 1:
            chart_mode = "lines+markers"
        elif current_index_chart == 2:
            chart_mode = "markers"
        elif current_index_chart == 3:
            chart_mode = "Bars"
        else:
            cm_error = "Something went wrong"
            print(cm_error)

        multi_go_db = self.avail_db_combo.currentText() + ".db"
        multi_go_extr = Extractor(multi_go_db)
        multi_go_plt = Plotter()
        multi_go_lists = []
        # converts Qdate object to python date object
        go_from_date = str(self.from_date.date().toPython())
        go_to_date = str(self.to_date.date().toPython())

        multi_go_lists = multi_go_extr.custom_select(go_from_date, go_to_date)

        if chart_mode == "lines" or chart_mode == "lines+markers" or chart_mode == "markers":
            go_data = multi_go_plt.go_scatter(
                chart_mode, multi_go_lists[0], multi_go_lists[1], multi_go_db)
            Window.go_list.append(go_data)
            if Window.unit is None:
                Window.unit = multi_go_lists[2][0]
        elif chart_mode == "Bars":
            go_data = multi_go_plt.go_bar(
                chart_mode, multi_go_lists[0], multi_go_lists[1], multi_go_db)
            Window.go_list.append(go_data)
            if Window.unit is None:
                Window.unit = multi_go_lists[2][0]
        else:
            print("Something went wrong")

    def clear_go_script(self):
        Window.go_list.clear()
        Window.unit = None

    def multi_go_plot_script(self):
        multi_go_plt = Plotter()
        current_index_chart = self.calendar_chart_field.currentIndex()
        if current_index_chart == 0:
            chart_mode = "lines"
        elif current_index_chart == 1:
            chart_mode = "lines+markers"
        elif current_index_chart == 2:
            chart_mode = "markers"
        elif current_index_chart == 3:
            chart_mode = "Bars"
        else:
            cm_error = "Something went wrong"
            print(cm_error)

        if chart_mode == "lines" or chart_mode == "lines+markers" or chart_mode == "markers":
            multi_go_plt.go_plot("Multiple Graphs",
                                 "TIME", Window.unit, Window.go_list)
        elif chart_mode == "Bars":
            multi_go_plt.go_bar_plot("Multiple Graphs",
                                     "TIME", Window.unit, Window.go_list)
        else:
            print("Something went wrong")
        Window.go_list.clear()
        Window.unit = None

    def custom_plot_script(self):
        current_index_chart = self.calendar_chart_field.currentIndex()

        if current_index_chart == 0:
            chart_mode = "lines"
        elif current_index_chart == 1:
            chart_mode = "lines+markers"
        elif current_index_chart == 2:
            chart_mode = "markers"
        elif current_index_chart == 3:
            chart_mode = "Bars"
        else:
            cm_error = "Something went wrong"
            print(cm_error)

        custom_db = self.avail_db_combo.currentText() + ".db"
        custom_extr = Extractor(custom_db)
        custom_plt = Plotter()
        custom_plot_lists = []
        custom_plot_title = custom_db[:-3]
        # converts Qdate object to python date object
        custom_from_date = str(self.from_date.date().toPython())
        custom_to_date = str(self.to_date.date().toPython())

        custom_plot_lists = custom_extr.custom_select(custom_from_date, custom_to_date)

        if chart_mode == "lines" or chart_mode == "lines+markers" or chart_mode == "markers":
            custom_plt.scatter_plot(
                chart_mode, custom_plot_lists[0], custom_plot_lists[1], custom_plot_title,
                "TIME", custom_plot_lists[2][0])
        elif chart_mode == "Bars":
            custom_plt.bar_plot(custom_plot_lists[0], custom_plot_lists[1], custom_plot_title,
                                "TIME", custom_plot_lists[2][0])
        else:
            print("Something went wrong")

    def setup_database_dialog(self):
        # Create Groupbox
        self.db_dialog_groupbox = QGroupBox("Sensor Declaration and Data Import")

        # Create widgets

        self.db_label = QLabel("Provide a name for the sensor")
        self.path_label = QLabel("Provide path to search for .xml files")

        self.db_field = QLineEdit("")
        self.path_field = QLineEdit(str(os.path.dirname(os.path.realpath(__file__))))
        self.button = QPushButton("Get started")

        # Create layout and add widgets
        self.db_dialog_layout = QVBoxLayout()
        self.db_dialog_layout.addWidget(self.db_label)
        self.db_dialog_layout.addWidget(self.db_field)
        self.db_dialog_layout.addWidget(self.path_label)
        self.db_dialog_layout.addWidget(self.path_field)
        self.db_dialog_layout.addWidget(self.button)

        # Set dialog layout
        self.db_dialog_groupbox.setLayout(self.db_dialog_layout)

        self.db_field.textChanged.connect(self.db_field_changed)
        self.button.clicked.connect(self.run_script)

    def run_script(self):
        error = "Error parsing files or path"
        db = self.db_field.text() + ".db"
        db_interaction = DatabaseInteraction(db)  # returns object of class DatabaseInteraction
        path = self.path_field.text()
        xml_importer = XMLImporter(db_interaction.name, path)
        try:
            success = xml_importer.import_xml()
        except Exception as ex:
            success = False
            error = ex
        msg = QMessageBox()

        if success:
            msg.setIcon(QMessageBox.Information)
            msg.setText("Sensor declaration successful")
            msg.setInformativeText("The sensor: {0} has been created.".format(self.db_field.text()))
            msg.setWindowTitle("Sensor declared!")
            msg.setDetailedText("The details are as follows:\nSensor name: {0} \nPath of .xml "
                                "files: {1}".format(self.db_field.text(), path))
            msg.setStandardButtons(QMessageBox.Ok)
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Sensor declaration failed!")
            msg.setInformativeText(
                "Declaration of the sensor: {0} failed!".format(self.db_field.text()))
            msg.setWindowTitle("Sensor declaration failed!")
            msg.setDetailedText("ERROR:\n {0}".format(error))
            msg.setStandardButtons(QMessageBox.Abort)

        retval = msg.exec_()
        msg.show()

    def database_utilities(self):
        # Create Groupbox
        self.db_util_groupbox = QGroupBox("Utilities")

        # Create Widgets
        self.db_update_label = QLabel("Select the Sensor you wish to update")
        self.path_label = QLabel("Xml File Path")
        self.update_path_field = QLineEdit(str(os.path.dirname(os.path.realpath(__file__))))
        self.update_button = QPushButton("Update")
        self.update_title = QLabel("Update Sensor")
        # self.db_clear_field = QLineEdit("example.db")
        self.db_clear_label = QLabel("Select Sensor")
        self.clear_button = QPushButton("Remove")
        self.clear_title = QLabel("Remove a sensor")

        # Create available db QComboBox for update
        self.update_avail_db_combo = QComboBox()
        self.update_avail_db_combo.addItems(self.available_db_combo())
        self.update_avail_db_combo_reload = QPushButton("Reload")

        # Create available db QComboBox for clear table
        self.clear_avail_db_combo = QComboBox()
        self.clear_avail_db_combo.addItems(self.available_db_combo())
        self.clear_avail_db_combo_reload = QPushButton("Reload")

        # Add Widgets

        self.db_util_db_update = QHBoxLayout()
        self.db_util_db_update.addWidget(self.db_update_label)
        self.db_util_db_update.addWidget(self.update_avail_db_combo)
        self.db_util_db_update.addWidget(self.update_avail_db_combo_reload)

        self.db_util_path = QHBoxLayout()
        self.db_util_path.addWidget(self.path_label)
        self.db_util_path.addWidget(self.update_path_field)

        self.db_util_clear = QHBoxLayout()
        self.db_util_clear.addWidget(self.db_clear_label)
        self.db_util_clear.addWidget(self.clear_avail_db_combo)
        self.db_util_clear.addWidget(self.clear_avail_db_combo_reload)

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

        self.update_button.clicked.connect(self.update_script)
        self.clear_button.clicked.connect(self.clear_table_script)
        self.update_avail_db_combo_reload.clicked.connect(self.reload_db_combo)
        self.clear_avail_db_combo_reload.clicked.connect(self.reload_db_combo)

    def update_script(self):
        db = self.update_avail_db_combo.currentText() + ".db"
        database_interaction = DatabaseInteraction(db)
        path = self.update_path_field.text()
        xml_importer = XMLImporter(database_interaction.name, path)
        update_error = "Something went wrong during update"

        try:
            success = xml_importer.import_xml()
        except Exception as ex:
            success = False
            update_error = ex
        update_msg = QMessageBox()

        if success:
            update_msg.setIcon(QMessageBox.Information)
            update_msg.setText("Sensor update successful")
            update_msg.setInformativeText("The sensor: {0} has been updated.".format(db[:-3]))
            update_msg.setWindowTitle("Sensor updated!")
            update_msg.setDetailedText("The details are as follows:\Sensor name: {0} \nPath of .xml "
                                       "files: {1}".format(db[:-3], path))
            update_msg.setStandardButtons(QMessageBox.Ok)
        else:
            update_msg.setIcon(QMessageBox.Critical)
            update_msg.setText("Sensor update failed!")
            update_msg.setInformativeText("Update of the sensor: {0} failed!".format(db[:-3]))
            update_msg.setWindowTitle("Sensor update failed!")
            update_msg.setDetailedText("ERROR:\n {0}".format(update_error))
            update_msg.setStandardButtons(QMessageBox.Abort)

        update_retval = update_msg.exec_()
        update_msg.show()

    def ready_plots(self):
        # Create Groupbox
        self.ready_plt_groupbox = QGroupBox("Ready-to-use plots")

        # Create Widgets
        self.choose_db_label = QLabel(
            "Provide the database that contains the data you wish to plot")
        self.choose_db_field = QLineEdit("")
        self.chart_label = QLabel("Chart")
        self.chart_field = QComboBox()
        self.chart_field.addItem("Lines")
        self.chart_field.addItem("Lines and Markers")
        self.chart_field.addItem("Scatter")
        self.chart_field.addItem("Bars")
        self.plot_mode_label = QLabel("Choose what time period to plot")
        self.plot_mode_field = QComboBox()
        self.plot_mode_field.addItem("Daily")
        self.plot_mode_field.addItem("Weekly")
        self.plot_mode_field.addItem("Monthly")
        self.plot_mode_field.addItem("Yearly")
        self.plot_button = QPushButton("Plot")

        # Create available db QComboBox for ready-plots
        self.ready_plot_avail_db_combo = QComboBox()
        self.ready_plot_avail_db_combo.addItems(self.available_db_combo())
        self.ready_plot_avail_db_combo_reload = QPushButton("Reload")

        # Add QComboBox and QPushButton to a QHBoxLayout
        self.ready_plot_qhbox_layout = QHBoxLayout()
        self.ready_plot_qhbox_layout.addWidget(self.ready_plot_avail_db_combo)
        self.ready_plot_qhbox_layout.addWidget(self.ready_plot_avail_db_combo_reload)

        # Add Widgets
        self.plot_vbox_layout = QVBoxLayout()
        self.plot_vbox_layout.addWidget(self.choose_db_label)
        self.plot_vbox_layout.addLayout(self.ready_plot_qhbox_layout)
        self.plot_vbox_layout.addWidget(self.chart_label)
        self.plot_vbox_layout.addWidget(self.chart_field)
        self.plot_vbox_layout.addWidget(self.plot_mode_label)
        self.plot_vbox_layout.addWidget(self.plot_mode_field)
        self.plot_vbox_layout.addWidget(self.plot_button)

        # Set layout to groupbox
        self.ready_plt_groupbox.setLayout(self.plot_vbox_layout)
        self.plot_button.clicked.connect(self.ready_plot_script)
        self.ready_plot_avail_db_combo_reload.clicked.connect(self.reload_db_combo)

    def db_field_changed(self):
        self.db_field.setText(self.db_field.text())

    def db_clear_field_changed(self):
        self.db_clear_field.setText(self.db_clear_field.text())

    def db_update_field_changed(self):
        self.db_update_field.setText(self.db_update_field.text())

    def from_selectedDateChanged(self):
        self.from_date.setDate(self.calendar.selectedDate())

    def to_selectedDateChanged(self):
        self.to_date.setDate(self.calendar.selectedDate())

    def clear_table_script(self):
        clear_error = "Something went wrong during clearing sensor"
        db = self.clear_avail_db_combo.currentText() + ".db"

        try:
            # db_int.clear_table()
            os.remove(db)
            clear_success = True
        except Exception as ex:
            clear_success = False
            clear_error = ex
        clear_msg = QMessageBox()

        if clear_success:
            clear_msg.setIcon(QMessageBox.Information)
            clear_msg.setText("Sensor has been removed")
            clear_msg.setInformativeText(
                "The {0} sensor have been removed.".format(db[:-3]))
            clear_msg.setWindowTitle("Sensor has been removed!")
            clear_msg.setStandardButtons(QMessageBox.Ok)
        else:
            clear_msg.setIcon(QMessageBox.Critical)
            clear_msg.setText("Removing sensor has failed!")
            clear_msg.setInformativeText("Removing the sensor: {0} has failed!".format(db[:-3]))
            clear_msg.setWindowTitle("Removing this sensor has failed!")
            clear_msg.setDetailedText("ERROR:\n {0}".format(clear_error))
            clear_msg.setStandardButtons(QMessageBox.Abort)

        clear_retval = clear_msg.exec_()
        clear_msg.show()

    def set_db_entry_button_script(self):
        db_name_fixed = self.avail_db_combo.currentText() + ".db"
        self.db = DatabaseInteraction(db_name_fixed)
        extr = Extractor(self.db.name)
    # Create datetime objects of the first and last strings of date
        self.datetime_first = datetime.strptime(extr.select_first_row()[
            0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.datetime_last = datetime.strptime(extr.select_last_row()[
            0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
        self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
        self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
        self.calendar.setMinimumDate(self.first_row)
        self.calendar.setMaximumDate(self.last_row)

        self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
        self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
        self.calendar.setMinimumDate(self.first_row)
        self.calendar.setMaximumDate(self.last_row)

    def reload_db_combo(self):
        self.avail_db_combo.clear()
        self.avail_db_combo.addItems(self.available_db_combo())
        self.clear_avail_db_combo.clear()
        self.clear_avail_db_combo.addItems(self.available_db_combo())
        self.update_avail_db_combo.clear()
        self.update_avail_db_combo.addItems(self.available_db_combo())
        self.ready_plot_avail_db_combo.clear()
        self.ready_plot_avail_db_combo.addItems(self.available_db_combo())

    def available_db_combo(self):

        db_files = []
        db_list_model = QStringListModel()

        for subdir, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for file in files:
                filepath = subdir + os.path.sep + file

                if filepath.endswith(".db"):
                    if filepath not in db_files:
                        db_files.append(file[:-3])

        db_list_model.setStringList(db_files)

        return db_list_model.stringList()

    def ready_plot_script(self):
        db = self.ready_plot_avail_db_combo.currentText() + ".db"
        extr = Extractor(db)
        plt = Plotter()
        ready_plot_title = db[:-3]

        if self.chart_field.currentIndex() == 0:
            chart_mode = "lines"
        elif self.chart_field.currentIndex() == 1:
            chart_mode = "lines+markers"
        elif self.chart_field.currentIndex() == 2:
            chart_mode = "markers"
        elif self.chart_field.currentIndex() == 3:
            chart_mode = "Bars"
        else:
            print("Something went wrong")

        if self.plot_mode_field.currentIndex() == 0:
            plot_mode = "daily_select"
        elif self.plot_mode_field.currentIndex() == 1:
            plot_mode = "weekly_select"
        elif self.plot_mode_field.currentIndex() == 2:
            plot_mode = "monthly_select"
        elif self.plot_mode_field.currentIndex() == 3:
            plot_mode = "yearly_select"
        else:
            print("Something went wrong")

        plot_lists = []
        # Extract from the database the data for x-y axis and the unit
        plot_lists = extr.extract(plot_mode)

        if chart_mode == "lines" or chart_mode == "lines+markers" or chart_mode == "markers":
            plt.scatter_plot(chart_mode, plot_lists[0], plot_lists[1],
                             ready_plot_title, "TIME", plot_lists[2][0])
        elif chart_mode == "Bars":
            plt.bar_plot(plot_lists[0], plot_lists[1], ready_plot_title, "TIME", plot_lists[2][0])
        else:
            print("Something went wrong")


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())
