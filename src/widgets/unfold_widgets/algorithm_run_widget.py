from PyQt5.QtWidgets import QVBoxLayout, QMessageBox

from widgets import UnfoldWidget


class AlgorithmRunWidget(UnfoldWidget):
    def __init__(self, parent, engine):
        super().__init__(parent, engine, 'algorithm_run_widget', 'ALGORITHM RUN')

        self.button.disconnect()
        self.button.clicked.connect(self.load_widget)

        # layout
        self.layout = QVBoxLayout(self.frame)

    def load_widget(self):
        if self.engine.state.steps_visualization is None:
            error = QMessageBox()
            error.setIcon(QMessageBox.Critical)
            if self.engine.state.imported_data is None:
                error.setText('No dataset was selected')
            else:
                error.setText('Steps visualization is disabled')
            error.setWindowTitle("Error")
            error.exec_()
            return

        self.clear_layout()
        self.layout.addWidget(self.engine.state.steps_visualization)
        self.layout.update()

        self.parent().unfold(self)

    def clear_layout(self, layout=None):
        if layout is None:
            layout = self.layout
        for i in reversed(range(layout.count())):
            child = layout.itemAt(i)
            if child.widget():
                child.widget().setParent(None)
            elif child.layout():
                self.clear_layout(child.layout())
            else:
                layout.removeItem(child)
