from PyQt5.QtWidgets import QWidget

class DrawerWidget(QWidget):
    """ A slide out drawer widget. """
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(-self.width, 0, self.width, self.height)

    def show(self):
