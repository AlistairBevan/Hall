from PyQt5.QtCore import QObject, pyqtSignal
from typing import List

class HallWorker(QObject):

    finished = pyqtSignal()
    dataPoint = pyqtSignal(float)
    line = pyqtSignal(list)


    def __init__(self,voltmeter: Resource = None, currentSource: Resource = None,
        scanner:Resource = None, intgrlTime: int = 0, rangeCtrl: str = '',
        current: float = 0, dwell: float = 0, vLim: float = 0, numPoints: int = 1,
        field: int = 0,
        fieldDelay: float = 0) -> None:
        '''Constructor for the class; stores the relevant information for the thread
        to use'''
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        self.scanner = scanner
        self.intgrlTime = intgrlTime
        self.rangeCtrl = rangeCtrl
        self.current = current
        self.dwell = dwell
        self.vLim = vLim
        self.numPoints = numPoints
        self.field = field
        self.fieldDelay = fieldDelay


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
