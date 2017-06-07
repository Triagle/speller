from PyQt5.QtWidgets import QMainWindow, QApplication
import speller
import correction_dialog
import sys


class UIManager:
    """ Manage UI state. """
    def __init__(self):
        """ Setup UI objects. """
        self.application = QApplication(sys.argv)
        self.main_window = QMainWindow()
        self.main_window_state = speller.Ui_MainWindow(self.main_window)

    def run(self):
        """ Run UIManager. """
        self.main_window.show()
