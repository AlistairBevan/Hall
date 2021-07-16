import sys
import pyvisa
import time
from custom_widgets import (FieldControllerWidget, CurrentSourceWidget,
                            VoltmeterWidget, SampleInfoWidget, BelowGraphWidget,
                            ResistivityWidget, Column4Widget, ColoredButton,
                            IVColumn1)
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from graphing import View

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow Constructor'''
        super().__init__()
        self.makeUI()
        self.connectButtons()
        self.setupInstruments()
        self.show()

    def setupInstruments(self):
        '''sets up the instruments for use'''
        rm = pyvisa.ResourceManager()
        # voltmeter = rm.open_resource('GPIB0::2::INSTR')
        # scanner = rm.open_resource('GPIB0::7::INSTR')
        # currentSource = rm.open_resource('GPIB0::12::INSTR')


    def makeUI(self):
        '''Constructs the visual components of the UI'''
        self.setWindowTitle('Hall GUI')

        cw = qtw.QTabWidget()#central widget (the outermost widget)
        self.setCentralWidget(cw)
        self.hallWidget = qtw.QWidget()#widget to contain all of the hall tab
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
        #add the buttons
        self.goBtn = ColoredButton('GO')
        self.goBtn.setMinimumSize(400,55)
        self.column1Layout.addWidget(self.goBtn)
        self.abortBtn = ColoredButton('Abort', rgb = (255,0,0))
        self.abortBtn.setMinimumSize(400,55)
        self.column1Layout.addWidget(self.abortBtn)
        #add a spacer on the bottom
        spacer = qtw.QSpacerItem(100,100, hPolicy = qtw.QSizePolicy.Preferred,
                                vPolicy = qtw.QSizePolicy.Expanding)
        self.column1Layout.addItem(spacer)

        #make the second column
        self.column2Layout = qtw.QVBoxLayout()
        self.hallLayout.addLayout(self.column2Layout)

        #add the graph
        self.hall_plot = View()
        self.hall_plot.setSizePolicy(qtw.QSizePolicy.MinimumExpanding,
                                    qtw.QSizePolicy.MinimumExpanding)
        self.column2Layout.addWidget(self.hall_plot)

        #add the stuff below the graph
        self.belowGraph = BelowGraphWidget()
        self.column2Layout.addWidget(self.belowGraph)

        #add the third column
        self.resistivityWidget = ResistivityWidget()
        self.hallLayout.addWidget(self.resistivityWidget)

        #add the fourth column
        self.column4Widget = Column4Widget()
        self.hallLayout.addWidget(self.column4Widget)

        self.hallWidget.setLayout(self.hallLayout)#sets the layout of out Halltab
        self.centralWidget().addTab(self.hallWidget, "Hall-Program")

        #make the IV tab next
        self.IVWidget = qtw.QWidget()
        self.IVLayout = qtw.QHBoxLayout()

        self.IVColumn1 = IVColumn1()
        self.IVLayout.addWidget(self.IVColumn1)

        self.IVColumn2 = qtw.QVBoxLayout()
        self.IVLayout.addLayout(self.IVColumn2)
        self.IV_Plot = View()
        self.IV_Plot.setSizePolicy(qtw.QSizePolicy.MinimumExpanding,
                                    qtw.QSizePolicy.MinimumExpanding)
        self.IVColumn2.addWidget(self.IV_Plot)
        self.IVWidget.setLayout(self.IVLayout)

        self.centralWidget().addTab(self.IVWidget, "IV-Test")
        self.resize(800,600)

    def connectButtons(self):
        '''Connects the buttons to the proper logic'''
        self.goBtn.clicked.connect(self.go)
        self.abortBtn.clicked.connect(self.abort)

    def go(self):
        '''run when you press go, sets up thread and starts it'''
        pass

    def abort(self):
        '''stops the thread'''
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
