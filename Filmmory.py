import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QDate, QTimer
from datetime import date
from Filmmory_UI import  Ui_MainWindow


# For converting datetime.date format to QDate format.
# To display the current date on widgets on startup.
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

        #For saving entered titles only to not allow duplicates.
        self.titles = set()

        #This function includes setting headers and their sizes, since .clear() removes them too.
        self.import_movies()

        self.unknown_start_date.stateChanged.connect(self.unknown_start_date_checked)
        self.unknown_finish_date.stateChanged.connect(self.unknown_finish_date_checked)
        self.status_combo.currentTextChanged.connect(self.status_date_control)

        self.add_button.clicked.connect(self.add_movie)
        self.remove_button.clicked.connect(self.remove_movie)
        self.import_button.clicked.connect(self.import_movies_interactive)
        self.save_button.clicked.connect(self.save_movies_interactive)
        self.sort_button.clicked.connect(self.sorter)


    # Disables Date Widgets based on selected status.
    def status_date_control(self):
        if self.status_combo.currentIndex() == 1:
            self.score_combo.setEnabled(True)
            self.start_date.setEnabled(True)
            self.finish_date.setEnabled(True)
            self.unknown_start_date.setEnabled(True)
            self.unknown_finish_date.setEnabled(True)
        elif self.status_combo.currentIndex() == 0:
            self.score_combo.setEnabled(True)
            self.start_date.setEnabled(True)
            self.finish_date.setEnabled(False)
            self.unknown_finish_date.setEnabled(False)
        else:
            self.score_combo.setEnabled(False)
            self.start_date.setEnabled(False)
            self.finish_date.setEnabled(False)
            self.unknown_start_date.setEnabled(False)
            self.unknown_finish_date.setEnabled(False)


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
        if self.status_combo.currentIndex() == 2:
            return '-'
        elif self.unknown_start_date.isChecked():
            return '?'
        else:
            return '/'.join(str(self.start_date.date())[19:29].split(', ')[::-1])

    def finish_date_value(self):
        if self.status_combo.currentIndex() == 0 or self.status_combo.currentIndex() == 2:
            return '-'
        elif self.unknown_finish_date.isChecked():
            return '?'
        else:
            return '/'.join(str(self.finish_date.date())[19:29].split(', ')[::-1])


    # Returns selected score or "-" if not selected.
    def score_value(self):
        if not self.score_combo.isEnabled() or self.score_combo.currentText() == 'Score':
            return '-'
        else:
            return self.score_combo.currentText()


    # Adds input to the list as a movie.
    # Keeps tabs for duplicates in self.titles.
    def add_movie(self):
        if self.title.text() == '':
            pass
        elif self.title.text().lower() in self.titles:
            self.add_button.setText('Already Present!')
            QTimer.singleShot(1000, lambda: self.add_button.setText('Add'))
        else:
            self.movie_table_model.appendRow([
                QStandardItem(self.title.text()),
                QStandardItem(self.status_combo.currentText()),
                QStandardItem(self.score_value()),
                QStandardItem(self.start_date_value()),
                QStandardItem(self.finish_date_value())])
            self.titles.add(self.title.text().lower())
            self.title.clear()


    # Finds selected row indexes and removes them decreasingly
    # If not selected, removes last entry.
    # Keeps tabs for duplicates in self.titles
    def remove_movie(self):
        selections = self.movie_table_view.selectionModel().selectedRows()
        if not selections:
            last_row = self.movie_table_model.rowCount() - 1
            self.titles.discard(self.movie_table_model.item(last_row, 0).text().lower())
            self.movie_table_model.removeRow(last_row)
        else:
            selection_indexes = reversed(sorted(index.row() for index in selections))
            for each in selection_indexes:
                self.titles.discard(self.movie_table_model.item(each, 0).text().lower())
                self.movie_table_model.removeRow(each)


    # Imports movies by turning lines into list(), separating by " | ".
    # This function includes setting headers and their sizes, since .clear() deletes them too.
    # Keeps tabs for duplicates in self.titles.
    def import_movies(self):
        self.movie_table_model.clear()
        self.movie_table_model.setHorizontalHeaderLabels(['Title', 'Status', 'Score', 'Start Date', 'Finish Date'])
        self.movie_table_view.setColumnWidth(0, 320)
        with open('filmmory_save1.txt', encoding='UTF-8') as filmmory_save1:
            for line in filmmory_save1:
                tags = line.strip('\n').split(' | ')
                self.titles = set()
                self.titles.add(tags[0].lower())
                single_movie = Movie(tags)
                self.movie_table_model.appendRow([
                    QStandardItem(single_movie.title),
                    QStandardItem(single_movie.status),
                    QStandardItem(single_movie.score),
                    QStandardItem(single_movie.start_date),
                    QStandardItem(single_movie.finish_date),])

    # Changes button text briefly.
    def import_movies_interactive(self):
        try:
            self.import_button.setText('Importing...')
            self.import_movies()
            QTimer.singleShot(1000, lambda: self.import_button.setText('Done!'))
        except FileNotFoundError:
            QTimer.singleShot(1000, lambda: self.import_button.setText('No Savefile Found!'))
        except:
            self.movie_table_model.clear()
            QTimer.singleShot(1000, lambda: self.import_button.setText('Savefile Damaged!'))
        finally:
            QTimer.singleShot(2000, lambda: self.import_button.setText('Import'))


    # Saves the list into a .txt file, separating tags with a " | ".
    def save_movies(self):
        with open('filmmory_save1.txt', 'w', encoding='UTF-8') as filmmory_save1:
            for row in range(int(self.movie_table_model.rowCount())):
                for column in range(int(self.movie_table_model.columnCount())):
                    index = self.movie_table_model.index(row, column)
                    content = self.movie_table_model.itemFromIndex(index).text()
                    if column != int(self.movie_table_model.columnCount()) - 1:
                        filmmory_save1.write(content+' | ')
                    else:
                        filmmory_save1.write(content+'\n')

    # Changes button text briefly.
    def save_movies_interactive(self):
        self.save_button.setText('Saving...')
        self.save_movies()
        QTimer.singleShot(1000, lambda: self.save_button.setText('Done!'))
        QTimer.singleShot(2000, lambda: self.save_button.setText('Save'))


    # Sorts the savefile and then imports it.
    # Uses both self.save_movies() and self.import_movies().
    def sorter(self):
        list1 = []
        self.save_movies()
        try:
            with open('filmmory_save1.txt',encoding='UTF-8') as filmmory_save1:
                self.sort_button.setText('Sorting...')
                for line in filmmory_save1:
                    list1.append(line)
                list1 = sorted(list1)
            with open('filmmory_save1.txt','w', encoding='UTF-8') as filmmory_save1:
                for each in list1:
                    filmmory_save1.write(each)
            self.import_movies()
            QTimer.singleShot(1000, lambda: self.sort_button.setText('Done!'))
        except FileNotFoundError:
            QTimer.singleShot(1000, lambda: self.sort_button.setText('No Savefile Found!'))
        except:
            self.movie_table_model.clear()
            QTimer.singleShot(1000, lambda: self.sort_button.setText('Savefile Damaged!'))
        finally:
            QTimer.singleShot(2000, lambda: self.sort_button.setText('Sort'))



app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
