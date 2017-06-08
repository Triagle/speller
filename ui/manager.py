from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from ui import speller
from ui import correction_dialog
import sys


class UIManager:
    """ Manage UI state. """
    def show_dialog(self):
        """ Show corrections dialog """
        dialog = QDialog(self.main_window)
        self.corrections_dialog.setupUi(dialog)
        dialog.exec()

    def connect_slots(self):
        """ Connect UI slots for various ui objects"""
        self.main_window_state.actionCorrections.triggered.connect(self.show_dialog)

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
        self.main_window.show()
        return self.application.exec_()
