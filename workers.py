from PyQt5.QtCore import QObject, pyqtSignal
from pyvisa import Resource
import numpy as np
from typing import List
from miscellaneous import available_name
import time

class HallWorker(QObject):
    '''worker for taking a measurement the takeHallMeasurement method of this
    class will be executed by a seperate thread in order to keep the UI
    responsive'''
    finished = pyqtSignal()
    dataPoint = pyqtSignal(list)
    line = pyqtSignal(list)

    def __init__(self,voltmeter: Resource = None, currentSource: Resource = None,
        scanner:Resource = None, intgrlTime: int = 0, rangeCtrl: str = '',
        current: float = 0, dwell: float = 0, vLim: float = 0, sampleID: str = '',
        temp: float = 0, thickness: float = 0, numPoints: int = 1, field: int = 0,
        fieldDelay: float = 0, filepath: str = '') -> None:
        '''Constructor for the class; stores the relevant information for the thread
        to use, since arguments cannot be passed when using moveToThread (might be
        possible with lambda but I think this way is better)'''
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        self.scanner = scanner
        self.intgrlTime = intgrlTime
        self.rangeCtrl = rangeCtrl
        self.current = current
        self.dwell = dwell
        self.vLim = vLim
        self.sampleID = sampleID
        self.temp = temp
        self.thickness = thickness
        self.numPoints = numPoints
        self.field = field
        self.fieldDelay = fieldDelay
        self.filepath = available_name(filepath)


    def ready(self, finishedSlots: List = [], dataPointSlots: List = [],
              lineSlots: List = []) -> None:
        '''connect all the signals and slots, takes lists of the slots desired to be
        connected, one list for each different signal this class has'''
        #connect the signals to desired slots
        for finishedSlot in finishedSlots:
            self.finished.connect(finishedSlot)

        for dataPointSlot in dataPointSlots:
            self.dataPoint.connect(dataPointSlot)

        for LineSlot in lineSlots:
            self.line.connect(lineSlot)


    def takeHallMeasurment(self) -> None:
        '''method for executing a measurement routine'''
        pass



class IVWorker(QObject):

    finished = pyqtSignal()
    dataPoint = pyqtSignal(list)
    abort = False
    switchDict: dict = {'1': ':clos (@1!1!1,1!2!2,1!3!3,1!4!4)',
                        '2': ':clos (@1!1!2,1!2!3,1!3!4,1!4!1)',
                        '3': ':clos (@1!1!3,1!2!4,1!3!1,1!4!2)',
                        '4': ':clos (@1!1!4,1!2!1,1!3!2,1!4!3)',
                        '5': ':clos (@1!1!1,1!2!4,1!3!2,1!4!3)',
                        '6': ':clos (@1!1!4,1!2!2,1!3!3,1!4!1)',}

    def __init__(self, voltmeter: Resource = None, currentSource: Resource = None,
            scanner: Resource = None):
        super().__init__()
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        self.scanner = scanner
        self.currentValues = np.array([])
        self.switch = ''

    def setInputs(self, switchNumber: str = '', intgrtTime: int = 5, current: float = 0,
                    voltLim: float = 10) -> None:
        '''sets the user inputs to the correct values'''
        self.currentValues = np.linspace(-current, current, 11)
        self.switch = self.switchDict[switchNumber]
        self.intgrtTime = intgrtTime
        self.voltLim = voltLim

    def connectSignals(self, finishedSlots: List = [], dataPointSlots: List = []) -> None:
        '''connect all the signals and slots, takes lists of the slots desired to be
        connected, one list for each different signal this class has'''
        #connect the signals to desired slots
        for finishedSlot in finishedSlots:
            self.finished.connect(finishedSlot)

        for dataPointSlot in dataPointSlots:
            self.dataPoint.connect(dataPointSlot)

    def takeIVMeasurement(self) -> None:
        '''takes 11 evenly spaced current and voltage measurements across the
        -current to current range and plots them on the IV_Plot'''
        self.clearDevices()
        #configuring the voltmeter based on the labview
        self.voltmeter.write('G0B1I0N1W0Z0R0S0P1O0T5')
        self.scanner.write(self.switch)#set the selected switch
        self.currentSource.write('F1XL1 B1')

        for current in self.currentValues:

            if self.abort:
                self.currentSource.write('I0.000E+0X')
                self.finished.emit()
                return

            currentCmdString = f'I{current:.4e}X'
            self.currentSource.write(currentCmdString)
            self.voltmeter.write('X')
            voltage = float(self.voltmeter.read())
            print(voltage)
            self.dataPoint.emit([current, voltage])

        self.currentSource.write('I0.000E+0X')
        self.clearDevices()
        self.finished.emit()

    def clearDevices(self) -> None:
        self.currentSource.clear()
        self.currentSource.write('K0X')
        self.scanner.write(':open all')
        self.scanner.clear()



    def stop(self) -> None:
        self.currentSource.write('I0.000E+0X')
