import random

from PySide6.QtWidgets import QApplication, QMainWindow
from ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.startCycleButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.stopCycleButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))



def main():
    app = QApplication()
    window = MainWindow()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()