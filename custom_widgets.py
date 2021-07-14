from PyQt5 import QtWidgets as qtw

class blueButton(qtw.QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""
        QPushButton{
        background-color: rgb(64, 137, 255);\n
        font: 18px;
        min-width: 2em;
        padding: 6px;
        }""")
