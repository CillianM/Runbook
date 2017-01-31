from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class ImageButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(ImageButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()