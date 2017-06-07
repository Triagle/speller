import sys
from PyQt5 import QtWidgets
from ui import manager


def main():
    """ Main program entry function"""
    app = QtWidgets.QApplication(sys.argv)
    ui = manager.UIManager()
    ui.run()
    app.exec()

main()
