import sys
import pyvisa
import time
from custom_widgets import (Inputs,FitResults1, FitResults2, BelowGraphWidget,
                            ColoredButton,IVColumn1)
from workers import IVWorker, HallWorker
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from datetime import datetime
from graphing import View

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow Constructor'''
        super().__init__()
        self.makeUI()
        self.connectButtons()
        self.setupInstruments()

        self.hallWorker = HallWorker(voltmeter = self.voltmeter,
                                     scanner = self.scanner,
                                     currentSource = self.currentSource)
        self.show()

    def setupInstruments(self):
        '''sets up the instruments for use'''
        rm = pyvisa.ResourceManager()
        self.voltmeter = rm.open_resource('GPIB0::2::INSTR')
        self.scanner = rm.open_resource('GPIB0::7::INSTR')
        self.currentSource = rm.open_resource('GPIB0::12::INSTR')


    def makeUI(self):
        '''Constructs the visual components of the UI'''
        self.setWindowTitle('Hall GUI')

        cw = qtw.QTabWidget()#central widget (the outermost widget)
        self.setCentralWidget(cw)
        self.hallWidget = qtw.QWidget()#widget to contain all of the hall tab
        self.hallLayout = qtw.QHBoxLayout()#layout for the hall tab

        #start making the first tab
        #make the first column
        self.hallInputs = Inputs()

        self.hallLayout.addWidget(self.hallInputs)

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
        self.fitResults1 = FitResults1()
        self.hallLayout.addWidget(self.fitResults1)

        #add the fourth column
        self.fitResults2 = FitResults2()
        self.hallLayout.addWidget(self.fitResults2)

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
        self.hallInputs.goBtn.clicked.connect(self.hallGo)
        self.hallInputs.abortBtn.clicked.connect(self.hallAbort)
        self.IVColumn1.goBtn.clicked.connect(self.IVGo)
        self.IVColumn1.abortBtn.clicked.connect(self.IVAbort)

    def hallGo(self):
        '''run when you press go, sets up thread and starts it'''
        pass

    def hallAbort(self):
        '''stops the hall thread'''
        pass

    def IVGo(self):
        '''run when you press go, sets up thread and starts it'''
        inputs = self.IVColumn1.textDict()
        current = float(inputs['current'])
        switch = inputs['switch']
        self.IV_Plot.cla()
        self.IV_Plot.set_xlim(-current*1.05, current*1.05)
        self.IVThread = qtc.QThread()
        self.IVWorker = IVWorker(voltmeter = self.voltmeter,
                                 scanner = self.scanner,
                                 currentSource = self.currentSource,)
        self.IVWorker.moveToThread(self.IVThread)
        self.IVThread.started.connect(self.IVWorker.takeIVMeasurement)
        self.IVThread.finished.connect(self.IVThread.deleteLater)

        self.IVWorker.setInputs(current = current, switchNumber = switch)
        self.IVWorker.connectSignals(finishedSlots = [self.IVThread.quit,self.IVWorker.deleteLater],
            dataPointSlots = [self.IV_Plot.refresh_stats])
        self.IVThread.start()

    def IVAbort(self):
        '''stops the IV thread'''
        pass
if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle('Windows')
    mw = MainWindow()
    sys.exit(app.exec())
