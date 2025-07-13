"""
This file contains user interface code for the data_exctractor project.
"""
import sys
import typing
from PyQt5 import QtCore

from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow


class MainWindow(QMainWindow):
    """
    Application Interface
    """

    def __init__(self, parent: QWidget | None = ...,
                 flags: WindowFlags | WindowType = ...) -> None:
        super().__init__(parent, flags)


def start_app():
    """
    Open the application interface.
    """
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    start_app()
