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
        self.db_entry_label = QLabel("Set Database")
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
        self.multi_go_label = QLabel("Plot multiple graphic objects")
        self.multi_go_layout = QHBoxLayout()
        self.multi_go_add_button = QPushButton("Add Graphic Object")
        self.multi_go_clear_button = QPushButton("Clear Graphic Objects")
        self.multi_go_plot_button = QPushButton("Plot Graphic Objects")

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

        self.available_db_combo()

        # self.cal_options.addLayout(self.avail_db_combo_layout, 0, 0)
        self.cal_options.addLayout(self.db_entry_layout, 0, 0)
        self.cal_options.addLayout(self.h_mode_layout, 1, 0)
        self.cal_options.addLayout(self.from_to_dates_layout, 2, 0)
        self.cal_options.addWidget(self.custom_plot_button, 3, 0)
        self.cal_options.addWidget(self.multi_go_label, 4, 0)
        self.cal_options.addLayout(self.multi_go_layout, 5, 0)
        self.cal_options.addWidget(self.multi_go_plot_button, 6, 0)

        self.avail_db_combo_reload.clicked.connect(self.reload_db_combo)
        self.custom_plot_button.clicked.connect(self.custom_plot_script)
        # Connect multi_go buttons
        self.multi_go_add_button.clicked.connect(self.add_go_script)
        self.multi_go_clear_button.clicked.connect(self.clear_go_script)
        self.multi_go_plot_button.clicked.connect(self.multi_go_plot_script)

        # Add widgets and sub layout to main layout
        self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
        self.previewLayout.addLayout(self.cal_options, 0, 1)
        self.previewGroupBox.setLayout(self.previewLayout)

    # def debug_script(self):
    #     debug_from_date = str(self.from_date.date().toPython())
    #     debug_to_date = str(self.to_date.date().toPython())
    #     print(debug_from_date, debug_to_date)

    def reload_db_combo(self):
        self.avail_db_combo.clear()
        self.avail_db_combo.addItems(self.available_db_combo())

    def available_db_combo(self):

        db_files = []
        db_list_model = QStringListModel()

        for subdir, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
            for file in files:
                filepath = subdir + os.path.sep + file

                if filepath.endswith(".db"):
                    if filepath not in db_files:
                        db_files.append(file)

        db_list_model.setStringList(db_files)

        return db_list_model.stringList()

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

        multi_go_db = self.avail_db_combo.currentText()
        multi_go_extr = Extractor(multi_go_db)
        multi_go_plt = Plotter()
        multi_go_lists = []
        # converts Qdate object to python date object
        go_from_date = str(self.from_date.date().toPython())
        go_to_date = str(self.to_date.date().toPython())

        multi_go_lists = multi_go_extr.custom_select(go_from_date, go_to_date)

        # graph_object = multi_go_plt.go_scatter(
        #     chart_mode, multi_go_lists[0], multi_go_lists[1], multi_go_db)
        go_data = multi_go_plt.go_scatter(
            chart_mode, multi_go_lists[0], multi_go_lists[1], multi_go_db)
        Window.go_list.append(go_data)
        if Window.unit is None:
            Window.unit = multi_go_lists[2][0]

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

        # trial = Window.go_list[: len(Window.go_list) - 1]
        # print(Window.go_list[0])
        # print(Window.go_list)
        # print(trial)

        if chart_mode == "lines" or chart_mode == "lines+markers" or chart_mode == "markers":
            multi_go_plt.go_plot("Multiple Graphs",
                                 "TIME", Window.unit, Window.go_list)
        elif chart_mode == "Bars":
            multi_go_plt.bar_plot("Multiple Graphs",
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

        custom_db = self.avail_db_combo.currentText()
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
        self.db_dialog_groupbox = QGroupBox("Database Creation and Data Import")

        # Create widgets

        self.db_label = QLabel("Provide a name for the database, e.g. sensor_db.db")
        self.path_label = QLabel("Provide path to search for .xml files")

        self.db_field = QLineEdit("something.db")
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
        # Add button signal to greetings slot

        self.db_field.textChanged.connect(self.db_field_changed)
        self.button.clicked.connect(self.run_script)

    def run_script(self):
        error = "Error parsing files or path"
        db = self.db_field.text()
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
            msg.setText("Database import successful")
            msg.setInformativeText("The database: {0} has been created.".format(db))
            msg.setWindowTitle("Database imported!")
            msg.setDetailedText("The details are as follows:\nDatabase \
            name: {0}\nUnit of sensors: \nPath of .xml "
                                "files: {1}".format(db, path))
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        else:
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Database import failed!")
            msg.setInformativeText("Creation of the database: {0} failed!".format(db))
            msg.setWindowTitle("Database import failed!")
            msg.setDetailedText("ERROR:\n {0}".format(error))
            msg.setStandardButtons(QMessageBox.Retry | QMessageBox.Abort)

        retval = msg.exec_()
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

        # Constantly update text when changed
        self.db_update_field.textChanged.connect(self.db_update_field_changed)
        self.db_clear_field.textChanged.connect(self.db_clear_field_changed)
        self.update_button.clicked.connect(self.update_script)
        self.clear_button.clicked.connect(self.clear_table_script)

    def update_script(self):
        db = self.db_update_field.text()
        database_interaction = DatabaseInteraction(db)
        path = self.path_field.text()
        xml_importer = XMLImporter(database_interaction.name, path)
        xml_importer.import_xml()

    def ready_plots(self):
        # Create Groupbox
        self.ready_plt_groupbox = QGroupBox("Ready-to-use plots")

        # Create Widgets
        self.choose_db_label = QLabel(
            "Provide the database that contains the data you wish to plot")
        self.choose_db_field = QLineEdit("sensor_data.db")
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
        # self.chart_field.currentIndexChanged.connect(self.localeChanged)
        # self.localeChanged(self.chart_field.currentIndex())

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
        db = self.db_clear_field.text()
        clear_table = DatabaseInteraction(db)
        clear_table.clear_table()

    def set_db_entry_button_script(self):

        self.db = DatabaseInteraction(self.avail_db_combo.currentText())
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
    # def set_db_entry_button_script(self):
    #
    #     self.db = DatabaseInteraction(self.db_entry_field.text())
    #     extr = Extractor(self.db.name)
    # # Create datetime objects of the first and last strings of date
    #     self.datetime_first = datetime.strptime(extr.select_first_row()[
    #         0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
    #     self.datetime_last = datetime.strptime(extr.select_last_row()[
    #         0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
    #     self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
    #     self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
    #     self.calendar.setMinimumDate(self.first_row)
    #     self.calendar.setMaximumDate(self.last_row)
    #
    #     self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
    #     self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
    #     self.calendar.setMinimumDate(self.first_row)
    #     self.calendar.setMaximumDate(self.last_row)

    def ready_plot_script(self):
        db = self.choose_db_field.text()
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
