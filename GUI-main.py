import sys
import pyvisa
import time
from custom_widgets import (StandardButton,
                            FieldControllerWidget,
                            CurrentSourceWidget,
                            VoltmeterWidget,
                            SampleInfoWidget)
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow Constructor'''
        super().__init__()
        self.makeUI()
        self.show()

    def setupInstruments(self):
        rm = pyvisa.ResourceManager()

    def makeUI(self):
        '''Constructs the visual components of the UI'''
        self.setWindowTitle('Hall GUI')

        cw = qtw.QTabWidget()#central widget (the outermost widget)
        self.setCentralWidget(cw)
        self.hallWidget = qtw.QWidget()#central widget to contain all the hall UI
        self.hallLayout = qtw.QHBoxLayout()#layout for the hall tab

        #make the first column
        self.column1Layout = qtw.QVBoxLayout()
        self.hallLayout.addLayout(self.column1Layout)

        #UI section for sample information
        self.sampleInfoWidget = SampleInfoWidget('Sample Information')
        self.column1Layout.addWidget(self.sampleInfoWidget)
        #UI section for fieldController
        self.fieldControllerWidget = FieldControllerWidget('Field Controller B-H 15')
        self.column1Layout.addWidget(self.fieldControllerWidget)
        #UI section for Voltmeter
        self.voltmeterWidget = VoltmeterWidget('Voltmeter controls - Keithley 182')
        self.column1Layout.addWidget(self.voltmeterWidget)
        #UI section for current
        self.currentWidget = CurrentSourceWidget('Current Source - Keithley 220')
        self.column1Layout.addWidget(self.currentWidget)

        #make the second column
        self.column2Layout = qtw.QVBoxLayout()
        self.hallLayout.addLayout(self.column2Layout)

        spacer = qtw.QWidget()
        spacer.setSizePolicy(qtw.QSizePolicy.Expanding,qtw.QSizePolicy.Expanding)
        self.column2Layout.addWidget(spacer)

        self.goBtn = StandardButton('GO')
        self.goBtn.setMinimumSize(200,55)
        self.column2Layout.addWidget(self.goBtn)

        self.abortBtn = StandardButton('Abort', rgb = (255,0,0))
        self.abortBtn.setMinimumSize(200,55)
        self.column2Layout.addWidget(self.abortBtn)

        self.hallWidget.setLayout(self.hallLayout)
        self.centralWidget().addTab(self.hallWidget, "Hall")


        self.resize(600,600)

    def connectButtons(self):
        '''Connects the buttons to the proper logic'''
        self.magnetButton.clicked.connect(flipMagnet)

    def flipMagnet(self):
        '''logic for turning the magnet on and off'''
        if isOn:
            self.fieldController.write_ascii_values('SO4')
            time.sleep(0.2)
            self.fieldController.write_ascii_values('SO0')
            time.sleep(2)
            self.fieldController.write_ascii_values('CF', data)

        else:
            self.fieldController.write_ascii_values('ST')

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
