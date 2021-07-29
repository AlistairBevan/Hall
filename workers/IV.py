from PyQt5.QtCore import QObject, pyqtSignal
from pyvisa import Resource
import numpy as np
from typing import List
import time

class IVWorker(QObject):

    finished = pyqtSignal()
    dataPoint = pyqtSignal(list)
    lineSgnl = pyqtSignal(list)
    abort = False
    switchDict: dict = {'1': ':clos (@1!1!1,1!2!2,1!3!3,1!4!4)',
                        '2': ':clos (@1!1!2,1!2!3,1!3!4,1!4!1)',
                        '3': ':clos (@1!1!3,1!2!4,1!3!1,1!4!2)',
                        '4': ':clos (@1!1!4,1!2!1,1!3!2,1!4!3)',
                        '5': ':clos (@1!1!1,1!2!4,1!3!2,1!4!3)',
                        '6': ':clos (@1!1!4,1!2!2,1!3!3,1!4!1)',}

    intgrtTimeDict: dict = {'~2s': 'S1P1', '~5s': 'S0P1', '~10s': 'S0P2', '~20s': 'S2P1'}

    def __init__(self, voltmeter: Resource = None, currentSource: Resource = None,
            scanner: Resource = None):
        super().__init__()
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        self.scanner = scanner
        self.currentValues = np.array([])
        self.switchCmd = ''

    def setInputs(self, switchNumber: str = '', intgrtTime: str = '~5s', current: float = 0,
                    voltLim: float = 10) -> None:
        '''sets the user inputs to the correct values'''
        self.currentValues = np.linspace(-current, current, 11)
        self.switchCmd = self.switchDict[switchNumber]
        self.intgrtTimeCmd = self.intgrtTimeDict[intgrtTime]
        voltLimCmd = f"V{voltLim:.4e}X"
        self.currentSource.write(voltLimCmd)

    def connectSignals(self, finishedSlots: List = [], dataPointSlots: List = [],
        lineSlots: List = []) -> None:
        '''connect all the signals and slots, takes lists of the slots desired to be
        connected, one list for each different signal this class has'''
        #connect the signals to desired slots
        for finishedSlot in finishedSlots:
            self.finished.connect(finishedSlot)

        for dataPointSlot in dataPointSlots:
            self.dataPoint.connect(dataPointSlot)

        for lineSlot in lineSlots:
            self.lineSgnl.connect(lineSlot)

    def takeIVMeasurement(self) -> None:
        '''takes 11 evenly spaced current and voltage measurements across the
        -current to current range and plots them on the IV_Plot'''
        self.clearDevices()
        #configuring the voltmeter based on the labview
        self.voltmeter.write(f'G0B1I0N1W0Z0R0{self.intgrtTimeCmd}O0T5')
        self.scanner.write(self.switchCmd)#set the selected switch
        self.currentSource.write('F1XL1 B1')
        line = []
        for current in self.currentValues:

            if self.abort:
                self.clearDevices()
                self.finished.emit()
                return

            currentCmdString = f'I{current:.4e}X'
            self.currentSource.write(currentCmdString)
            time.sleep(0.2)
            self.voltmeter.write('X')
            voltage = float(self.voltmeter.read_raw())
            self.dataPoint.emit([current, voltage])
            line.append([current, voltage])

        self.lineSgnl.emit(line)
        self.clearDevices()
        self.finished.emit()

    def clearDevices(self) -> None:
        self.currentSource.write('K0X')
        self.currentSource.clear()
        self.scanner.clear()
        self.voltmeter.clear()
        self.scanner.write(':open all')
        self.currentSource.write('I0.000E+0X')
