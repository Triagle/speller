from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from ui import speller
from ui import correction_dialog
from db import words
import sqlite3
import sys

DATABASE_LOCATION = 'db/data.db'


class UIManager:
    """ Manage UI state. """
    def get_editor_words(self):
        text_editor_text = self.main_window_state.textEdit.toPlainText()
        return text_editor_text.split(' ')

    def get_unrecognized_words(self, candidates):
        text_editor_words = self.get_text_editor_words()
        cursor = self.conn.cursor()
        return [word for word in text_editor_words
                if not words.word_exists(cursor, word)]

    def get_words(self):
        cursor = self.conn.cursor()
        return words.get_word_list(cursor)

    def show_dialog(self):
        """ Show corrections dialog """
        dialog = QDialog(self.main_window)
        self.corrections_dialog.setupUi(dialog)
        dialog.exec()

    def connect_slots(self):
        """ Connect UI slots for various ui objects"""
        self.main_window_state.actionCorrections.triggered.connect(self.show_dialog)

    def load_db(self):
        cursor = self.conn.cursor()
        self.classifier =

    def __init__(self):
        """ Setup UI objects. """
        self.application = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.corrections_dialog = correction_dialog.Ui_Form()
        self.main_window_state = speller.Ui_MainWindow()
        self.main_window_state.setupUi(self.main_window)
        self.connect_slots()

    def run(self):
        """ Run UIManager. """
        with sqlite3.connect(DATABASE_LOCATION) as conn:
            self.conn = conn
            self.main_window.show()
            res = self.application.exec_()
        return res
