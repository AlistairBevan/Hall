from PyQt5.QtCore import QObject, pyqtSignal
from pyvisa import Resource
import numpy as np
from typing import List
import time

class HallWorker(QObject):
    '''worker for taking a measurement the takeHallMeasurement method of this
    class will be executed by a seperate thread in order to keep the UI
    responsive'''
    finished = pyqtSignal()
    dataPoint = pyqtSignal(list)
    lineData = pyqtSignal(dict)
    fieldState = pyqtSignal(str)
    switchSgnl = pyqtSignal(str)
    abort = False
    switchDict: dict = {'1': ':clos (@1!1!1,1!2!2,1!3!3,1!4!4)',
                        '2': ':clos (@1!1!2,1!2!3,1!3!4,1!4!1)',
                        '3': ':clos (@1!1!3,1!2!4,1!3!1,1!4!2)',
                        '4': ':clos (@1!1!4,1!2!1,1!3!2,1!4!3)',
                        '5': ':clos (@1!1!1,1!2!4,1!3!2,1!4!3)',
                        '6': ':clos (@1!1!4,1!2!2,1!3!3,1!4!1)',}

    intgrtTimeDict: dict = {'~2s': 'S1P1', '~5s': 'S0P1', '~10s': 'S0P2', '~20s': 'S2P1'}
    rangeDict: dict = {'Enable Auto-Range': 'R0', '3mV Range': 'R1', '30mV Range': 'R2',
        '300mV Range': 'R3', '3V Range': 'R4', '30V Range': 'R5', 'Disable Auto-Range': 'R8'}

    def __init__(self,voltmeter: Resource = None, currentSource: Resource = None,
        scanner: Resource = None, fieldController: Resource = None, intgrtTime: str = '~5s',
        rangeCtrl: str = '', current: float = 0, vLim: float = 0,
        dataPoints: int = 1, field: int = 0, fieldDelay: float = 0, thickness: float = 0) -> None:
        '''Constructor for the class; stores the relevant information for the thread
        to use since arguments cannot be passed when using moveToThread (might be
        possible with lambda but I think this way is better)'''
        super().__init__()
        self.voltmeter = voltmeter
        self.currentSource = currentSource
        voltLimCmd = f"V{vLim:.4e}X"
        self.currentSource.write(voltLimCmd)
        self.scanner = scanner
        self.fieldController = fieldController
        self.intgrtTimeCmd = self.intgrtTimeDict[intgrtTime]
        self.rangeCtrlCmd = self.rangeDict[rangeCtrl]
        self.current = current
        self.vLim = vLim
        self.dataPoints = dataPoints
        self.field = field
        self.fieldDelay = fieldDelay
        self.currentValues = np.linspace(-current, current, dataPoints)
        self.thickness = thickness


    def connectSignals(self, finishedSlots: List = [], dataPointSlots: List = [],
              dataSlots: List = [], fieldSlots: List = [], switchSlots: List = []) -> None:
        '''connect all the signals and slots, takes lists of the slots desired to be
        connected, one list for each different signal this class has'''
        #connect the signals to desired slots
        for finishedSlot in finishedSlots:
            self.finished.connect(finishedSlot)

        for dataPointSlot in dataPointSlots:
            self.dataPoint.connect(dataPointSlot)

        for dataSlot in dataSlots:
            self.lineData.connect(dataSlot)

        for fieldSlot in fieldSlots:
            self.fieldState.connect(fieldSlot)

        for switchSlot in switchSlots:
            self.switchSgnl.connect(switchSlot)

    def powerOnField(self) -> None:
        '''starts up the field Controller (copied from labview)'''
        self.fieldController.write('MO0')
        self.fieldController.write('SO1')
        time.sleep(0.2)
        self.fieldController.write('SO0')
        self.fieldController.write('CF0')

    def reverseField(self) -> None:
        '''reverses the field direction'''
        self.fieldController.write(f'CF0')
        time.sleep(self.fieldDelay)
        #reverse the field
        self.fieldController.write('SO4')
        time.sleep(0.2)
        self.fieldController.write('SO0')
        time.sleep(2*self.fieldDelay)#takes a while for it to reverse



    def takeHallMeasurment(self) -> None:
        '''method for executing a measurement routine'''
        self.voltmeter.write(f'G0B1I0N1W0Z0{self.rangeCtrlCmd}{self.intgrtTimeCmd}O0T5')
        self.currentSource.write('F1XL1 B1')
        self.powerOnField()
        self.resetDevices()
        data = {}
        lines = []

        for i in range(1,9):
            self.switchSgnl.emit(str(i))#notify the gui what switch is selected

            if i < 7:
                switchCmd = self.switchDict[str(i)]
            else:#repeats 5 and 6
                switchCmd = self.switchDict[str(i - 2)]
            self.scanner.write(switchCmd)
            if i == 5:
                #turn on the field when we get to the fifth switch
                self.fieldState.emit('On')#update the GUI field: display
                self.fieldController.write(f'CF{self.field}')
                time.sleep(self.fieldDelay)

            if i == 7:
                #reverse the field when we get to the seventh switch
                self.reverseField()
                #ramp back up to the desired field
                self.fieldState.emit('On - Reversed')#update GUI field: display
                self.fieldController.write(f'CF{self.field}')
                time.sleep(self.fieldDelay)

            singleLine = []
            #iterate throught the current values measuring voltage
            for current in self.currentValues:
                if self.abort:#check for an abort call
                    self.resetDevices()
                    self.finished.emit()
                    return

                currentCmdString = f'I{current:.4e}X'
                self.currentSource.write(currentCmdString)
                time.sleep(0.2)
                self.voltmeter.write('X')#takes the measurement
                voltage = float(self.voltmeter.read_raw())#reads the measurement
                self.dataPoint.emit([current, voltage])
                singleLine.append([current, voltage])
            self.scanner.write(':open all')
            lines.append(np.array(singleLine))



        #when were done we need to reverse the field back again
        self.reverseField()
        self.resetDevices()
        time.sleep(2*self.fieldDelay)
        data['lines'] = lines
        data['field'] = self.field
        data['current'] = self.current
        data['thickness'] = self.thickness
        self.finished.emit()
        self.lineData.emit(data)
        print('done')


    def resetDevices(self):
        self.currentSource.write('K0X')
        self.currentSource.write('I0.000E+0X')
        self.scanner.write(':open all')
        self.switchSgnl.emit('n/a')
        self.fieldController.write('CF0')
        self.fieldState.emit('Off')
