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
    abort = False
    switchDict: dict = {'1': ':clos (@1!1!1,1!2!2,1!3!3,1!4!4)',
                        '2': ':clos (@1!1!2,1!2!3,1!3!4,1!4!1)',
                        '3': ':clos (@1!1!3,1!2!4,1!3!1,1!4!2)',
                        '4': ':clos (@1!1!4,1!2!1,1!3!2,1!4!3)',
                        '5': ':clos (@1!1!1,1!2!4,1!3!2,1!4!3)',
                        '6': ':clos (@1!1!4,1!2!2,1!3!3,1!4!1)',}

    intgrtTimeDict: dict = {'2': 'S0P1', '5': 'S0P2', '10': 'S2P1', '20': 'S0P3'}

    def __init__(self,voltmeter: Resource = None, currentSource: Resource = None,
        scanner:Resource = None, fieldController = None, intgrtTime: int = 0, rangeCtrl: str = '',
        current: float = 0, dwell: float = 0, vLim: float = 0, sampleID: str = '',
        temp: float = 0, thickness: float = 0, numPoints: int = 1, field: int = 0,
        fieldDelay: float = 0, filepath: str = '') -> None:
        '''Constructor for the class; stores the relevant information for the thread
        to use, since arguments cannot be passed when using moveToThread (might be
        possible with lambda but I think this way is better)'''
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        self.scanner = scanner
        self.fieldController = fieldController
        self.intgrtTimeCmd = intgrtTimeDict['intgrtTime']
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


    def connectSignals(self, finishedSlots: List = [], dataPointSlots: List = [],
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
        self.voltmeter.write(f'G0B1I0N1W0Z0R0{self.intgrtTimeCmd}O0T5')
        self.currentSource.write('F1XL1 B1')

        for i in range(1,5):#do the first four without magnet
            switchCmd = switchDict[str(i)]
            self.scanner.write(switchCmd)
            for current in self.currentValues:

                if self.abort:
                    self.currentSource.write('I0.000E+0X')
                    self.finished.emit()
                    return

                currentCmdString = f'I{current:.4e}X'
                self.currentSource.write(currentCmdString)
                self.voltmeter.write('X')
                voltage = float(self.voltmeter.read())
                self.dataPoint.emit([current, voltage])

        #turn on magnet
        self.fieldController.write(f'CF{self.field}')



    def clearDevices(self):
        self.currentSource.write('K0X')
        self.scanner.write(':open all')
        self.fieldControler.write('CF0')
