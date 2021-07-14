import sys
import pyvisa
from custom_widgets import stadardButton
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow Constructor'''
        super().__init__()
        self.makeUI()
        self.show()

    def makeUI(self):
        '''Constructs the visual components of the UI'''
        self.setWindowTitle('Hall GUI')
        centralWidget = qtw.QWidget()
        outerLayout = qtw.QVBoxLayout()
        self.magnetButton = standardButton("Flip Magnet Switch")
        self.magnetButton.setSizePolicy(qtw.QSizePolicy.MinimumExpanding,
                                        qtw.QSizePolicy.MinimumExpanding)
        outerLayout.addWidget(self.magnetButton)
        centralWidget.setLayout(outerLayout)
        self.setCentralWidget(centralWidget)
        self.resize(600,600)

    def connectButtons(self):
        '''Connects the buttons to the proper logic'''
        self.magnetButton.clicked.connect(flipMagnet)

    def flipMagnet(self):
        '''logic for turning the magnet on and off'''
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
