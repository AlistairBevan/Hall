import sys
import pyvisa
import time
from custom_widgets import (StandardButton,
                            FieldControllerWidget,
                            CurrentSourceWidget,
                            VoltmeterWidget,
                            SampleInfoWidget,
                            BelowGraphWidget,
                            ResultDisplayWidget)
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from graphing import View

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

        #add the graph
        self.IV_plot = View()
        self.IV_plot.setSizePolicy(qtw.QSizePolicy.MinimumExpanding,
                                    qtw.QSizePolicy.MinimumExpanding)
        self.column2Layout.addWidget(self.IV_plot)

        #add the stuff below the graph
        subgraph = BelowGraphWidget()
        self.column2Layout.addWidget(subgraph)


        self.hallWidget.setLayout(self.hallLayout)
        self.centralWidget().addTab(self.hallWidget, "Hall")

        self.column3Layout = qtw.QVBoxLayout()
        placeHolder = ResultDisplayWidget()
        self.column3Layout.addWidget(placeHolder)
        self.hallLayout.addLayout(self.column3Layout)

        self.resize(800,600)

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
