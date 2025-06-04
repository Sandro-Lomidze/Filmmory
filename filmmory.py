import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, QTimer
from untitled import Ui_MainWindow
from datetime import date


#For converting datetime.date format to QDate format.
#To display the current date on widgets on startup.
today = str(date.today()).split('-')
current_day = int(today[2])
current_month = int(today[1])
current_year = int(today[0])
today = QDate(current_year, current_month, current_day)

class Movie:
    def __init__(self, tags):
        if not isinstance(tags, list):
            raise TypeError('Argument must be a list')
        self.title = tags[0]
        self.status = tags[1]
        self.score = tags[2]
        self.start_date = tags[3]
        self.finish_date = tags[4]



class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.start_date.setDate(today)
        self.finish_date.setDate(today)

        self.movie_table_model = QStandardItemModel()
        self.movie_table_view.setModel(self.movie_table_model)

        self.titles = set()
        #This function includes setting headers and their sizes, since .clear() them too.
        self.import_movies()


        self.unknown_start_date.stateChanged.connect(self.unknown_start_date_checked)
        self.unknown_finish_date.stateChanged.connect(self.unknown_finish_date_checked)

        self.add_button.clicked.connect(self.add_movie)
        self.remove_button.clicked.connect(self.remove_movie)
        self.import_button.clicked.connect(self.import_movies)
        self.save_button.clicked.connect(self.save_movies)


    # To disable QDate widgets when checking boxes.
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


    # To return date values based on boxes checked.
    # Last line changes PyQt5.QtCore.QDate(2025, 6, 2) -> "2/6/2025".
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


    # Retruns selected score or "-" if not selected.
    def score_value(self):
        if self.score_combo.currentText() == 'Score':
            return '-'
        else:
            return self.score_combo.currentText()


    # Adds input to the list as a movie.
    # Keeps tabs for duplicates in self.titles
    def add_movie(self):
        if self.title.text() == '':
            pass
        elif self.title.text() in self.titles:
            self.add_button.setText('Entry Already Present!')
            QTimer.singleShot(1000, lambda: self.add_button.setText('Add'))
        else:
            self.movie_table_model.appendRow([
                QStandardItem(self.title.text()),
                QStandardItem(self.status_combo.currentText()),
                QStandardItem(self.score_value()),
                QStandardItem(self.start_date_value()),
                QStandardItem(self.finish_date_value())
            ])
            self.titles.add(self.title.text())
            self.title.clear()



    # Finds selected row indexes and removes them decreasingly
    # If not selected, removes last entry.
    # Keeps tabs for duplicates in self.titles
    def remove_movie(self):
        selections = self.movie_table_view.selectionModel().selectedRows()
        if not selections:
            last_row = self.movie_table_model.rowCount() - 1
            self.titles.discard(self.movie_table_model.item(last_row, 0).text())
            self.movie_table_model.removeRow(last_row)
        else:
            selection_indexes = reversed(sorted(index.row() for index in selections))
            for each in selection_indexes:
                self.titles.discard(self.movie_table_model.item(each, 0).text())
                self.movie_table_model.removeRow(each)


    # Imports movies by turning lines into list(), separating by " | ".
    # Changes button text briefly.
    # This function includes setting headers and their sizes, since .clear() deletes them too.
    # Keeps tabs for duplicates in self.titles
    def import_movies(self):
        self.movie_table_model.clear()
        self.movie_table_model.setHorizontalHeaderLabels(['Title', 'Status', 'Score', 'Start Date', 'Finish Date'])
        self.movie_table_view.setColumnWidth(0, 320)
        self.import_button.setText('Importing...')
        try:
            save1 = open('filmmory_save1.txt', encoding='UTF-8')
            for line in save1:
                tags = line.strip('\n').split(' | ')
                self.titles.add(tags[0])
                single_movie = Movie(tags)
                self.movie_table_model.appendRow([
                    QStandardItem(single_movie.title),
                    QStandardItem(single_movie.status),
                    QStandardItem(single_movie.score),
                    QStandardItem(single_movie.start_date),
                    QStandardItem(single_movie.finish_date),
                ])
            QTimer.singleShot(1000, lambda: self.import_button.setText('Done'))
        except FileNotFoundError:
            QTimer.singleShot(1000, lambda: self.import_button.setText('No Savefile Found!'))
        except:
            self.movie_table_model.clear()
            QTimer.singleShot(1000, lambda: self.import_button.setText('Savefile Damaged!'))
        finally:
            QTimer.singleShot(2000, lambda: self.import_button.setText('Import'))

    # Saves the list into a .txt file, separating tags with a " | ".
    # Changes button text briefly.
    def save_movies(self):
        self.save_button.setText('Saving...')
        save1 = open('filmmory_save1.txt', 'w', encoding='UTF-8')
        for row in range(int(self.movie_table_model.rowCount())):
            for column in range(int(self.movie_table_model.columnCount())):
                index = self.movie_table_model.index(row, column)
                content = self.movie_table_model.itemFromIndex(index).text()
                if column != int(self.movie_table_model.columnCount()) - 1:
                    save1.write(content+' | ')
                else:
                    save1.write(content+'\n')
        QTimer.singleShot(1000, lambda: self.save_button.setText('Done!'))
        QTimer.singleShot(2000, lambda: self.save_button.setText('Save'))



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
