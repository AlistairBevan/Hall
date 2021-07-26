import sys
import pyvisa
import time
import numpy as np
from custom_widgets import (Inputs,FitResults1, FitResults2, BelowGraphWidget,
                            ColoredButton,IVColumn1,status)
from workers.IV import IVWorker
from workers.Hall import HallWorker
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from datetime import datetime
from graphing import View
from fitting import Fitter
from FileWriting import Writer

class MainWindow(qtw.QMainWindow):

    def __init__(self):
        '''MainWindow Constructor'''
        super().__init__()
        self.makeUI()
        self.fitter = Fitter()
        self.writer = Writer(self.hallInputs.sampleInfoWidget.sampleIDInput.text(),
            self.hallInputs.sampleInfoWidget.tempInput.text(),
            self.hallInputs.sampleInfoWidget.thicknessInput.text(),
            self.belowGraph.pathInput.text())
        self.connectSignals()
        self.setupInstruments()
        self.show()

    def setupInstruments(self):
        '''sets up the instruments for use'''
        rm = pyvisa.ResourceManager()
        self.voltmeter = rm.open_resource('GPIB0::2::INSTR')
        #in ms change the timeout time to be longer for the longer integrating times
        self.voltmeter.timeout = 25000
        self.scanner = rm.open_resource('GPIB0::7::INSTR')
        self.currentSource = rm.open_resource('GPIB0::12::INSTR')
        self.fieldController = rm.open_resource('GPIB0::3::INSTR')


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
        self.hall_Plot = View()
        self.hall_Plot.setSizePolicy(qtw.QSizePolicy.MinimumExpanding,
                                    qtw.QSizePolicy.MinimumExpanding)
        self.column2Layout.addWidget(self.hall_Plot)

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
        status_bar = status()
        self.setStatusBar(status_bar)
        self.centralWidget().addTab(self.IVWidget, "IV-Test")
        self.resize(800,600)

    def connectSignals(self):
        '''Connects the buttons to the proper logic as well as other functions
        essentially chaining things together'''
        self.hallInputs.goBtn.clicked.connect(self.hallGo)
        self.hallInputs.goBtn.clicked.connect(lambda:
            self.statusBar().stateLbl.setText('state: Running'))

        self.hallInputs.abortBtn.clicked.connect(self.hallAbort)

        self.IVColumn1.goBtn.clicked.connect(self.IVGo)
        self.IVColumn1.goBtn.clicked.connect(lambda:
            self.statusBar().stateLbl.setText('state: Running'))

        self.IVColumn1.abortBtn.clicked.connect(self.IVAbort)

        self.fitter.resultSgnl.connect(self.writer.writeToFile)#writes the results after fitting
        self.fitter.resultSgnl.connect(self.showResults)#displays the results
        self.fitter.rSqrdSgnl.connect(self.showRSqrd)#displays the rsqrd on the UI
        self.fitter.rSqrdSgnl.connect(self.writer.setRSqrd)#gives the righter the r squared values when done

        self.hallInputs.sampleInfoWidget.sampleIDInput.textChanged.connect(self.writer.setSampleID)
        self.hallInputs.sampleInfoWidget.tempInput.textEdited.connect(self.writer.setTemp)
        self.hallInputs.sampleInfoWidget.thicknessInput.textChanged.connect(self.writer.setThickness)

        self.belowGraph.pathInput.textChanged.connect(self.writer.setFilepath)

    #enabling and disabling the proper buttons to prevent crashing
    def disableGo(self):
        '''disables the go buttons and enables the abort buttons'''
        self.IVColumn1.goBtn.setEnabled(False)
        self.hallInputs.goBtn.setEnabled(False)
        self.IVColumn1.abortBtn.setEnabled(True)
        self.hallInputs.abortBtn.setEnabled(True)

    def enableGo(self):
        '''enables the go buttons and disables the abort buttons'''
        self.IVColumn1.goBtn.setEnabled(True)
        self.hallInputs.goBtn.setEnabled(True)
        self.IVColumn1.abortBtn.setEnabled(False)
        self.hallInputs.abortBtn.setEnabled(False)

    def hallGo(self):
        '''run when you press go, sets up thread and starts it'''
        self.disableGo()
        #collect the inputs as a dictionary from the input widget
        inputs = self.hallInputs.textDict()
        current = inputs['current']
        filepath = self.belowGraph.pathInput.text()
        #clear and set the limits of the plot
        self.hall_Plot.cla()
        self.hall_Plot.set_xlim(-current*1.05, current*1.05)
        self.hallThread = qtc.QThread()
        self.hallWorker = HallWorker(voltmeter = self.voltmeter, currentSource = self.currentSource,
                            scanner = self.scanner, fieldController = self.fieldController,
                            current = current, vLim = inputs['vLim'],
                            dataPoints = inputs['dataPoints'], field = inputs['field'],
                            fieldDelay = inputs['fieldDelay'], intgrtTime = inputs['intgrtTime'],
                            rangeCtrl = inputs['rangeCtrl'], thickness = inputs['thickness'])
        #prepares the threading
        self.hallWorker.moveToThread(self.hallThread)
        self.hallThread.started.connect(self.hallWorker.takeHallMeasurment)
        self.hallThread.finished.connect(self.hallThread.deleteLater)
        self.hallWorker.connectSignals(finishedSlots = [self.hallThread.quit,
            self.hallWorker.deleteLater,self.enableGo, lambda: self.statusBar().stateLbl.setText('state: Idle')],
            dataPointSlots = [self.hall_Plot.refresh_stats],
            dataSlots = [self.fitter.calculateResults],
            fieldSlots = [lambda state: self.statusBar().fieldLbl.setText('field: ' + state)],
            switchSlots = [lambda switchNumber: self.statusBar().switchLbl.setText('switch: ' + switchNumber)])
        self.hallThread.start()

    def hallAbort(self):
        '''stops the hall thread'''
        self.hallWorker.abort = True

    def IVGo(self):
        '''run when you press go, sets up thread and starts it'''
        self.disableGo()
        inputs = self.IVColumn1.textDict()
        current = float(inputs['current'])
        self.IV_Plot.cla()
        self.IV_Plot.set_xlim(-current*1.05, current*1.05)
        self.IVThread = qtc.QThread()
        self.IVWorker = IVWorker(voltmeter = self.voltmeter,
                                 scanner = self.scanner,
                                 currentSource = self.currentSource,)
        self.IVWorker.setInputs(**inputs)
        self.IVWorker.moveToThread(self.IVThread)
        self.IVThread.started.connect(self.IVWorker.takeIVMeasurement)
        self.IVThread.finished.connect(self.IVThread.deleteLater)
        self.IVWorker.connectSignals(finishedSlots = [self.IVThread.quit,self.IVWorker.deleteLater,
            self.enableGo, lambda: self.statusBar().stateLbl.setText('state: Idle'),
            lambda: self.statusBar().switchLbl.setText('switch: n/a')],
            dataPointSlots = [self.IV_Plot.refresh_stats])

        self.statusBar().switchLbl.setText('switch: ' + self.IVColumn1.switches.currentText())
        self.IVThread.start()

    def showRSqrd(self, rSqrds):
        self.belowGraph.box1.setText(f"{rSqrds[0]:.6f}")
        self.belowGraph.box2.setText(f"{rSqrds[1]:.6f}")
        self.belowGraph.box3.setText(f"{rSqrds[2]:.6f}")
        self.belowGraph.box4.setText(f"{rSqrds[3]:.6f}")
        self.belowGraph.box5.setText(f"{rSqrds[4]:.6f}")
        self.belowGraph.box6.setText(f"{rSqrds[5]:.6f}")
        self.belowGraph.box7.setText(f"{rSqrds[6]:.6f}")
        self.belowGraph.box8.setText(f"{rSqrds[7]:.6f}")


    def showResults(self,results):
        #these should be looked over carefully
        self.fitResults1.SheetRes1Display.setText(f"{results['sheetRes1']:.4e}")
        self.fitResults1.SheetRes2Display.setText(f"{results['sheetRes2']:.4e}")
        self.fitResults1.Rxy1Display.setText(f"{results['Rxy1']:.4e}")
        self.fitResults1.Rxy2Display.setText(f"{results['Rxy2']:.4e}")
        self.fitResults1.q1Display.setText(f"{results['q1']:.4e}")
        self.fitResults1.q2Display.setText(f"{results['q2']:.4e}")
        self.fitResults1.FfactorDisplay.setText(f"{results['ff']:.4e}")
        self.fitResults1.HallRatioDisplay.setText(f"{results['hallRatio']:.4e}")
        self.fitResults2.AvgSheetResDisplay.setText(f"{results['sheetRes']:.4e}")
        self.fitResults2.AvgTransResDisplay.setText(f"{results['AvgTransRes']:.4e}")
        self.fitResults2.AvgResDisplay.setText(f"{results['pBulk']:.4e}")
        self.fitResults2.SheetConcDisplay.setText(f"{results['sheetConc']:.4e}")
        self.fitResults2.BulkConcDisplay.setText(f"{results['bulkConc']:.4e}")
        self.fitResults2.HallCoefDisplay.setText(f"{results['hallCoef']:.4e}")
        self.fitResults2.HallMobilityDisplay.setText(f"{results['hallMob']:.4e}")

    def IVAbort(self):
        '''stops the IV thread'''
        self.IVWorker.abort = True

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    app.setStyle('Windows')
    mw = MainWindow()
    sys.exit(app.exec())
