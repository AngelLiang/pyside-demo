import sys
import random

from PySide6 import QtCore, QtWidgets


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text_edit.setText(random.choice(self.hello))


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(600, 400)
    widget.show()

    sys.exit(app.exec())
