from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QPaintEvent, QPixmap
from PyQt5.QtWidgets import QWidget


class QImage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.p = QPixmap()

    def setPixmap(self, p: QPixmap):
        self.p = p
        self.update()

    def paintEvent(self, event: QPaintEvent) -> None:
        if not self.p.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.SmoothPixmapTransform)
            _, _, w_widget, h_widget = self.rect().getRect()
            x, y, w, h = self.p.rect().getRect()
            if w > w_widget or h > h_widget:
                alfa = min(w_widget / w, h_widget / h)
                w = int(alfa * w)
                h = int(alfa * h)
            x = int(0.5 * (w_widget - w))
            painter.drawPixmap(QRect(x, y, w, h), self.p)
