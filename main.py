import sys
from PyQt5 import QtWidgets
from ui import manager


def main():
    """ Main program entry function"""
    ui = manager.UIManager()
    sys.exit(ui.run())

main()
