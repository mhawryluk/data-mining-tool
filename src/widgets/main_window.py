from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QDesktopWidget
from widgets import MainWidget


class MainWindow(QMainWindow):

    def __init__(self, engines):
        super().__init__()
        self.setWindowTitle('Data Mining Tool')
        self.setGeometry(0, 0, 1200, 600)

        # position the window in the middle of the screen
        rect = self.frameGeometry()
        rect.moveCenter(QDesktopWidget().availableGeometry().center())
        self.move(rect.topLeft())

        self.generalLayout = QHBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # with open('static/css/styles.css') as stylesheet:
        #     self.setStyleSheet(stylesheet.read())

        self.setStyleSheet("""
                UnfoldWidget > QFrame {
                    background-color: white;
                }
                
                UnfoldWidget QGroupBox:title, UnfoldWidget QTabBar::tab{
                    padding: 5px;
                    border-radius: 5px;
                    margin-bottom: 5px;
                    margin-right: 5px;
                }
                
                QScrollArea { background: transparent; }
                QScrollArea QWidget { background: transparent; }
                
                #import_widget > QPushButton, #import_widget QGroupBox:title {
                    background-color: #054a91;
                    color: white;
                    border: none;
                }
                
                #preprocessing_widget > QPushButton, #preprocessing_widget QGroupBox:title {
                    background-color: #3e7cb1;
                    color: white;
                    border: none;
                }
                
                #algorithm_setup_widget > QPushButton, #algorithm_setup_widget QGroupBox:title{
                    background-color: #81a4cd;
                    color: white;
                    border: none;
                }
                
                #algorithm_run_widget > QPushButton, #algorithm_run_widget QGroupBox:title{
                    background-color: #dbe4ee;
                    color: black;
                    border: none;
                }
                
                #results_widget > QPushButton, #results_widget QGroupBox:title, #results_widget QTabBar::tab:selected {
                    background-color: #f17300;
                    color: white;
                    border: none;
                }
                
                #results_widget QTabWidget QTabWidget QGroupBox QGroupBox {
                    border-radius: 10px;
}     
        """)

        self.generalLayout.addWidget(MainWidget(engines))

        self.show()
