from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QCloseEvent, QIcon
from PyQt5.QtCore import QDate
from datetime import date
from Qt_Designer_UI import Ui_MainWindow
from movie import Movie

# For converting datetime.date format to QDate format.
# To display the current date on widgets on startup.
today = str(date.today()).split('-')
current_day = int(today[2])
current_month = int(today[1])
current_year = int(today[0])
today = QDate(current_year, current_month, current_day)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, db):
        super().__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('window_icon.png'))

        self.db = db

        self.start_date.setDate(today)
        self.finish_date.setDate(today)
        self.release_year_spin.setValue(current_year)

        self.movie_table_model = QStandardItemModel()
        self.movie_table_view.setModel(self.movie_table_model)

        self.import_movies()

        self.unknown_start_date.stateChanged.connect(self.unknown_start_date_checked)
        self.unknown_finish_date.stateChanged.connect(self.unknown_finish_date_checked)
        self.status_combo.currentIndexChanged.connect(self.disable_control)
        self.type_combo.currentIndexChanged.connect(self.disable_control)

        self.title.textChanged.connect(self.matching)
        self.add_button.clicked.connect(self.add_movie)
        self.remove_button.clicked.connect(self.remove_movie)
        self.edit_button.clicked.connect(self.edit_movie)
        self.clear_button.clicked.connect(self.wipedown)

        self.actionAll.toggled.connect(self.toggled_all)
        self.actionCompleted.toggled.connect(self.toggled_completed)
        self.actionWatching.toggled.connect(self.toggled_watching)
        self.actionPlan_to_Watch.toggled.connect(self.toggled_plan_to_watch)


    def disable_control(self):
        if self.type_combo.currentIndex() == 0:
            self.runtime_spin.setEnabled(True)
            self.ep_count_label.setEnabled(False)
            self.ep_count_spin.setEnabled(False)
            if self.status_combo.currentIndex() == 0:
                self.score_combo.setEnabled(True)
                self.start_date.setEnabled(False)
                self.finish_date.setEnabled(True)
                self.unknown_start_date.setEnabled(False)
                self.unknown_finish_date.setEnabled(True)
            else:
                self.score_combo.setEnabled(False)
                self.start_date.setEnabled(False)
                self.finish_date.setEnabled(False)
                self.unknown_start_date.setEnabled(False)
                self.unknown_finish_date.setEnabled(False)
        else:
            self.runtime_spin.setEnabled(False)
            self.ep_count_label.setEnabled(True)
            self.ep_count_spin.setEnabled(True)
            if self.status_combo.currentIndex() == 0:
                self.score_combo.setEnabled(True)
                self.start_date.setEnabled(True)
                self.finish_date.setEnabled(True)
                self.unknown_start_date.setEnabled(True)
                self.unknown_finish_date.setEnabled(True)
            elif self.status_combo.currentIndex() == 1:
                self.score_combo.setEnabled(False)
                self.start_date.setEnabled(True)
                self.finish_date.setEnabled(False)
                self.unknown_start_date.setEnabled(True)
                self.unknown_finish_date.setEnabled(False)
            else:
                self.score_combo.setEnabled(False)
                self.start_date.setEnabled(False)
                self.finish_date.setEnabled(False)
                self.unknown_start_date.setEnabled(False)
                self.unknown_finish_date.setEnabled(False)

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
        if not self.start_date.isEnabled():
            if self.type_combo.currentIndex() == 1:
                return ''
            return None
        else:
            return self.start_date.text()

    def finish_date_value(self):
        if not self.finish_date.isEnabled():
            if self.type_combo.currentIndex() == 1:
                return ''
            return None
        else:
            return self.finish_date.text()

    def date_unified(self):
        if self.type_combo.currentIndex() == 0:
            return self.finish_date_value()
        else:
            if not self.start_date.isEnabled() and not self.finish_date.isEnabled():
                return None
            return f'{self.start_date_value()} ~ {self.finish_date_value()}'

    def score_value(self):
        if not self.score_combo.isEnabled() or self.score_combo.currentText() == 'Score':
            return None
        else:
            return self.score_combo.currentText()

    def runtime_ep_count_value(self):
        if self.type_combo.currentIndex() == 0:
            return self.runtime_spin.text()
        else:
            return self.ep_count_spin.text()

    def add_movie(self):
        if len(self.title.text().strip()) == 0:
            pass
        else:
            movie = Movie(None, self.title.text(), self.type_combo.currentText(), self.status_combo.currentText(),
                          self.score_value(), self.runtime_ep_count_value(), self.release_year_spin.text(),
                          self.date_unified())
            self.db.insert_movie(movie)
            self.title.clear()

    def remove_movie(self):
        selection = self.movie_table_view.selectionModel().selectedRows()
        selection_indexes = [index.row() for index in selection]
        for each in selection_indexes:
            id = self.movie_table_model.item(each, 0).text()
            self.db.delete_movie(id)
        self.matching()

    # noinspection PyUnboundLocalVariable,PyGlobalUndefined
    def edit_movie(self):
        selection = self.movie_table_view.selectionModel().selectedRows()
        if len(selection) == 1 and self.edit_button.text() == 'Edit':
            self.add_button.setEnabled(False)
            self.remove_button.setEnabled(False)
            self.clear_button.setEnabled(False)
            selection = selection[0].row()
            global update_id
            update_id = self.movie_table_model.item(selection, 0).text()
            self.bring_forth()
            self.edit_button.setText('Save Changes')
        elif self.edit_button.text() == 'Save Changes' and len(self.title.text().strip()) != 0:
            self.add_button.setEnabled(True)
            self.remove_button.setEnabled(True)
            self.clear_button.setEnabled(True)
            movie = Movie(update_id, self.title.text(), self.type_combo.currentText(), self.status_combo.currentText(),
                          self.score_value(), self.runtime_ep_count_value(), self.release_year_spin.text(),
                          self.date_unified())
            self.db.update_movie(movie)
            self.edit_button.setText('Edit')
            self.title.clear()
            self.matching()

    def bring_forth(self):
        selection = self.movie_table_view.selectionModel().selectedRows()[0].row()
        title = self.movie_table_model.item(selection, 1).text()
        type = self.movie_table_model.item(selection, 2).text()
        status = self.movie_table_model.item(selection, 3).text()
        score = self.movie_table_model.item(selection, 4).text()
        release_year = self.movie_table_model.item(selection, 6).text()
        self.title.setText(title)
        self.type_combo.setCurrentText(type)
        self.status_combo.setCurrentText(status)
        self.score_combo.setCurrentText(score)
        self.release_year_spin.setValue(int(release_year))


    def wipedown(self):
        self.db.clear()
        self.matching()

    def import_movies(self):
        movies = self.filter()
        self.builder(movies)

    def matching(self):
        title = self.title.text()
        movies = self.db.db_matching(title)
        self.builder(movies)

    def builder(self, movies):
        self.movie_table_model.clear()
        self.movie_table_model.setHorizontalHeaderLabels(['ID', 'Title', 'Type', 'Status', 'Score', 'Runtime/Episodes','Release Year', 'Start/Finish Date'])
        self.movie_table_view.setColumnWidth(1, 320)
        self.movie_table_view.setColumnWidth(5, 110)
        self.movie_table_view.setColumnWidth(7, 140)
        for each in movies:
            movie = Movie(*each)
            self.movie_table_model.appendRow([
                QStandardItem(str(movie.id)),
                QStandardItem(movie.title),
                QStandardItem(movie.type),
                QStandardItem(movie.status),
                QStandardItem(movie.score),
                QStandardItem(movie.runtime_ep_count),
                QStandardItem(movie.release_year),
                QStandardItem(movie.date_unified)])
        self.movie_table_view.hideColumn(0)

    def filter(self):
        if self.actionAll.isChecked():
            return self.db.fetch_all_movies()
        elif self.actionCompleted.isChecked():
            return self.db.fetch_completed_movies()
        elif self.actionWatching.isChecked():
            return self.db.fetch_watching_movies()
        elif self.actionPlan_to_Watch.isChecked():
            return self.db.fetch_plan_to_watch_movies()
        else:
            return []

    def toggled_all(self):
        if self.actionAll.isChecked():
            self.actionCompleted.setChecked(False)
            self.actionWatching.setChecked(False)
            self.actionPlan_to_Watch.setChecked(False)
            self.import_movies()
        elif self.no_action_checked():
            self.import_movies()

    def toggled_completed(self):
        if self.actionCompleted.isChecked():
            self.actionAll.setChecked(False)
            self.actionWatching.setChecked(False)
            self.actionPlan_to_Watch.setChecked(False)
            self.import_movies()
        elif self.no_action_checked():
            self.import_movies()


    def toggled_watching(self):
        if self.actionWatching.isChecked():
            self.actionAll.setChecked(False)
            self.actionCompleted.setChecked(False)
            self.actionPlan_to_Watch.setChecked(False)
            self.import_movies()
        elif self.no_action_checked():
            self.import_movies()

    def toggled_plan_to_watch(self):
        if self.actionPlan_to_Watch.isChecked():
            self.actionAll.setChecked(False)
            self.actionCompleted.setChecked(False)
            self.actionWatching.setChecked(False)
            self.import_movies()
        elif self.no_action_checked():
            self.import_movies()

    def no_action_checked(self):
        if not self.actionAll.isChecked() and not self.actionWatching.isChecked() and not self.actionCompleted.isChecked() and not self.actionPlan_to_Watch.isChecked():
            return True
        else:
            return False

    def closeEvent(self, event: QCloseEvent):
        self.db.conn.close()
        event.accept()
