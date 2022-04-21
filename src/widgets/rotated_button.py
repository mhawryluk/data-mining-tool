from PyQt5.QtWidgets import QPushButton, QStylePainter, QStyle, QStyleOptionButton


class RotatedButton(QPushButton):
    def __init__(self, parent, orientation="east"):
        super().__init__(parent)
        self.orientation = orientation

    def paintEvent(self, event):
        painter = QStylePainter(self)
        if self.orientation == "east":
            painter.rotate(270)
            painter.translate(-1 * self.height(), 0)
        if self.orientation == "west":
            painter.rotate(90)
            painter.translate(0, -1 * self.width())
        painter.drawControl(QStyle.CE_PushButton, self.get_style_options())

    def minimumSizeHint(self):
        size = super(RotatedButton, self).minimumSizeHint()
        size.transpose()
        return size

    def sizeHint(self):
        size = super(RotatedButton, self).sizeHint()
        size.transpose()
        return size

    def get_style_options(self):
        options = QStyleOptionButton()
        options.initFrom(self)
        size = options.rect.size()
        size.transpose()
        options.rect.setSize(size)
        options.features = QStyleOptionButton.None_

        if self.isFlat():
            options.features |= QStyleOptionButton.Flat
        if self.menu():
            options.features |= QStyleOptionButton.HasMenu
        if self.autoDefault() or self.isDefault():
            options.features |= QStyleOptionButton.AutoDefaultButton
        if self.isDefault():
            options.features |= QStyleOptionButton.DefaultButton
        if self.isDown() or (self.menu() and self.menu().isVisible()):
            options.state |= QStyle.State_Sunken
        if self.isChecked():
            options.state |= QStyle.State_On
        if not self.isFlat() and not self.isDown():
            options.state |= QStyle.State_Raised

        options.text = self.text()
        options.icon = self.icon()
        options.iconSize = self.iconSize()

        return options
