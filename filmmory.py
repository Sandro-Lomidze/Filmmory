import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtCore
from untitled import Ui_MainWindow
from datetime import date


today = str(date.today()).split('-')
this_day = int(today[2])
this_month = int(today[1])
this_year = int(today[0])
today = QtCore.QDate(this_year, this_month, this_day)



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_date.setDate(today)
        self.finish_date.setDate(today)

        self.movie_table_model = QStandardItemModel()
        self.movie_table_model.setHorizontalHeaderLabels(['Title', 'Status', 'Score', 'Date Started', 'Date Finished'])
        self.movie_table_model.appendRow([QStandardItem('I am the bone of my sword.'), QStandardItem('Plan to Watch')])
        self.movie_table_view.setModel(self.movie_table_model)
        self.movie_table_view.setColumnWidth(0, 320)


        self.unknown_start_date.stateChanged.connect(self.unknown_start_date_checked)
        self.unknown_finish_date.stateChanged.connect(self.unknown_finish_date_checked)

        self.add_button.clicked.connect(self.add_movie)


    def unknown_start_date_checked(self):
        if self.unknown_start_date.isChecked():
            self.start_date.setEnabled(False)
        else:
            self.start_date.setEnabled(True)

    def unknown_finish_date_checked(self):
        if self.unknown_finish_date.isChecked():
            self.finish_date.setEnabled(False)
        else:
            self.finish_date.setEnabled(True)

    def start_date_value(self):
        if self.unknown_start_date.isChecked():
            return '?'
        else:
            return '/'.join(str(self.start_date.date())[19:29].split(', ')[::-1])

    def finish_date_value(self):
        if self.unknown_finish_date.isChecked():
            return '?'
        else:
            return '/'.join(str(self.finish_date.date())[19:29].split(', ')[::-1])

    def score_value(self):
        if self.score_combo.currentText() == 'Score':
            return '-'
        else:
            return self.score_combo.currentText()


    def add_movie(self):
        if self.title.text() != '':
            self.movie_table_model.appendRow([
                QStandardItem(self.title.text()),
                QStandardItem(self.status_combo.currentText()),
                QStandardItem(self.score_value()),
                QStandardItem(self.start_date_value()),
                QStandardItem(self.finish_date_value())
            ])



app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())
