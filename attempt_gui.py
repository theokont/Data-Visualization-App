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


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()

        self.createCalendarBox()
        self.setup_database_dialog()

        layout = QGridLayout()
        layout.addWidget(self.db_dialog_groupbox, 0, 0)
        layout.addWidget(self.previewGroupBox, 0, 1)
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

        self.mode_label = QLabel("&Mode")
        self.custom_mode = QComboBox()
        self.custom_mode.addItem("Lines")
        self.custom_mode.addItem("Lines and Markers")
        self.custom_mode.addItem("Scatter")
        self.custom_mode.addItem("Bars")
        self.mode_label.setBuddy(self.custom_mode)

        # Attempt for better visuals
        self.h_mode_layout = QHBoxLayout()
        self.h_mode_layout.addWidget(self.mode_label)
        self.h_mode_layout.addWidget(self.custom_mode)

        self.from_to_dates_layout = QHBoxLayout()
        self.from_date = QDateEdit()
        self.from_date.setDisplayFormat('MMM d yyyy')
        self.from_date.setDate(self.calendar.selectedDate())
        self.from_date_label = QLabel("From")

        self.from_to_dates_layout.addWidget(self.from_date_label)
        self.from_to_dates_layout.addWidget(self.from_date)

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
        self.unit_label = QLabel("Provide the unit of the measurements")
        self.db_label = QLabel("Provide a name for the database, e.g. sensor_db.db")
        self.path_label = QLabel("Provide path to search for .xml files")

        self.unit_field = QLineEdit("unit")
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
        unit = self.unit_field.text()
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
        pass


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())

    #
    # class CalendarWindow(QWidget):
    #     def __init__(self):
    #         super(CalendarWindow, self).__init__()
    #
    #         self.createCalendarBox()
    #         self.createQdialog()
    #
    #         layout = QGridLayout()
    #         layout.addWidget(self.previewGroupBox, 0, 0)
    #         layout.addWidget(self.previewDialog, 0, 1)
    #
    #         self.setLayout(layout)
    #         self.previewLayout.setRowMinimumHeight(0,
    #                                                self.calendar.sizeHint().height())
    #         self.previewLayout.setColumnMinimumWidth(0,
    #                                                  self.calendar.sizeHint().width())
    #
    #         self.setWindowTitle("Calendar Widget")
    #
    #     def createCalendarBox(self):
    #         extr = Extractor("sensor_data.db")
    #         # Create datetime objects of the first and last strings of date
    #         self.datetime_first = datetime.strptime(extr.select_first_row()[
    #             0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
    #         self.datetime_last = datetime.strptime(extr.select_last_row()[
    #             0][0], "%Y-%m-%dT%H:%M:%S.%fZ")
    #
    #         self.previewGroupBox = QGroupBox("Preview")
    #
    #         self.calendar = QCalendarWidget()
    #         self.first_row = QDate.fromString(str(self.datetime_first.date()), "yyyy-MM-dd")
    #         self.last_row = QDate.fromString(str(self.datetime_last.date()), "yyyy-MM-dd")
    #         print(self.first_row)
    #         self.calendar.setMinimumDate(self.first_row)
    #         self.calendar.setMaximumDate(self.last_row)
    #         self.calendar.setGridVisible(True)
    #         # self.calendar.currentPageChanged.connect(self.reformatCalendarPage)
    #         self.previewLayout = QGridLayout()
    #         self.previewLayout.addWidget(self.calendar, 0, 0, Qt.AlignCenter)
    #         self.previewGroupBox.setLayout(self.previewLayout)
    #
    #     def createQdialog(self):
    #         # Create widgets
    #         self.unit_label = QLabel("Provide the unit of the measurements")
    #         self.db_label = QLabel("Provide a name for the database, e.g. sensor-xkl-12")
    #         self.path_label = QLabel("Provide path to search for .xml files")
    #
    #         self.unit_field = QLineEdit("unit")
    #         self.db_field = QLineEdit("db")
    #         self.path_field = QLineEdit(str(os.path.dirname(os.path.realpath(__file__))))
    #         self.button = QPushButton("Get started")
    #
    #         # Create layout and add widgets
    #         self.previewDialog = QVBoxLayout()
    #         self.previewDialog.addWidget(self.unit_label)
    #         self.previewDialog.addWidget(self.unit_field)
    #         self.previewDialog.addWidget(self.db_label)
    #         self.previewDialog.addWidget(self.db_field)
    #         self.previewDialog.addWidget(self.path_label)
    #         self.previewDialog.addWidget(self.path_field)
    #         self.previewDialog.addWidget(self.button)
    #         self.previewCalendarLayout = QGridLayout()
    #         self.previewCalendarLayout.addWidget(self.previewDialog, 0, 0)
    #         self.previewDialog.setLayout(self.previewCalendarLayout)
    #
    #
    # class UIWindow(QWidget):
    #     def __init__(self, parent=None):
    #         super(UIWindow, self).__init__(parent)
    #         # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
    #         self.ToolsBTN = QPushButton('text', self)
    #         self.ToolsBTN.move(50, 350)
    #
    #
    # class UIToolTab(QWidget):
    #     def __init__(self, parent=None):
    #         super(UIToolTab, self).__init__(parent)
    #         self.CPSBTN = QPushButton("text2", self)
    #         self.CPSBTN.move(100, 350)
    #
    #
    # class MainWindow(QMainWindow):
    #     def __init__(self, parent=None):
    #         super(MainWindow, self).__init__(parent)
    #         self.setGeometry(50, 50, 400, 450)
    #         self.setFixedSize(400, 450)
    #         self.startCalendarWidget()
    #
    #     def startUIToolTab(self):
    #         self.ToolTab = UIToolTab(self)
    #         self.setWindowTitle("UIToolTab")
    #         self.setCentralWidget(self.ToolTab)
    #         self.ToolTab.CPSBTN.clicked.connect(self.startCalendarWidget)
    #         self.show()
    #
    #     def startUIWindow(self):
    #         self.Window = UIWindow(self)
    #         self.setWindowTitle("UIWindow")
    #         self.setCentralWidget(self.Window)
    #         self.Window.ToolsBTN.clicked.connect(self.startUIToolTab)
    #         self.show()
    #
    #     def startCalendarWidget(self):
    #         self.cal = CalendarWindow()
    #         self.cal.show()
    #
    #
    # if __name__ == '__main__':
    #     app = QApplication(sys.argv)
    #     w = MainWindow()
    #     sys.exit(app.exec_())
