from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from sys import float_info, maxsize

class MyDoubleValidator(qtg.QDoubleValidator):

    '''
    Fix for strange behavior of default QDoubleValidator used in
    CurrentSourceWidget
    http://learnwithhelvin.blogspot.com/2010/01/qdoublevalidator.html
    (needed some tweaking)
    '''

    def __init__(self, bottom = float_info.min, \
                 top = float_info.max, \
                 decimals = float_info.dig, parent = None):

        super(MyDoubleValidator, self).__init__(bottom, top, decimals, parent)

    def validate(self, input_value : str, pos : int):
        state, char, pos = super().validate(input_value, pos)

        if input_value == '' or input_value == '.':
            return qtg.QValidator.Intermediate,char, pos

        if state != qtg.QValidator.State.Acceptable:
            return qtg.QValidator.Invalid,char, pos

        return qtg.QValidator.Acceptable,char, pos


class StandardButton(qtw.QPushButton):
    '''the default button to be used in the program
    (makes it easy to change the color of all buttons and so on)'''
    def __init__(self, *args, rgb: tuple = (64, 137, 255), **kwargs):
        super().__init__(*args, **kwargs)
        color = 'rgb' + str(rgb)
        self.setStyleSheet("""
        QPushButton{
        background-color: """ + color + """;\n
        font: 18px;
        min-width: 2em;
        padding: 6px;
        }""")

class FieldControllerWidget(qtw.QGroupBox):
    '''Widget for displaying the fieldController controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QFormLayout()

        self.fieldInput = qtw.QLineEdit()
        self.fieldInput.setValidator(qtg.QIntValidator())
        layout.addRow('Field (Gauss)',self.fieldInput)

        self.delayInput = qtw.QLineEdit()
        self.delayInput.setValidator(qtg.QDoubleValidator())
        layout.addRow('Field Delay (sec)',self.delayInput)
        self.setLayout(layout)

class CurrentSourceWidget(qtw.QGroupBox):
    '''Widget for displaying the current controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QFormLayout()

        self.currentInput = qtw.QLineEdit()
        self.currentInput.setValidator(qtg.QDoubleValidator())
        layout.addRow('Current (A)',self.currentInput)

        self.dwellInput = qtw.QLineEdit()
        self.dwellInput.setValidator(MyDoubleValidator(0,999.9))
        layout.addRow('Dwell Time (ms) 3ms to 999.9ms',self.dwellInput)
        self.setLayout(layout)

        self.vLimitInput = qtw.QLineEdit()
        self.vLimitInput.setValidator(qtg.QDoubleValidator())
        layout.addRow('V-Limit', self.vLimitInput)

class VoltmeterWidget(qtw.QGroupBox):
    '''Widget for displaying the voltmeter controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QFormLayout()

        self.integratingInput = qtw.QLineEdit()
        self.integratingInput.setValidator(qtg.QIntValidator())
        layout.addRow('Field (Gauss)',self.integratingInput)

        self.RangeInput = qtw.QLineEdit()
        self.RangeInput.setValidator(qtg.QDoubleValidator())
        layout.addRow('Field Delay (sec)',self.RangeInput)
        self.setLayout(layout)

class SampleInfoWidget(qtw.QGroupBox):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QFormLayout()

        self.SampleIDInput = qtw.QLineEdit()
        layout.addRow('Sample ID',self.SampleIDInput)

        self.TempInput = qtw.QLineEdit()
        self.TempInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Temp',self.TempInput)
        self.setLayout(layout)

        self.thicknessInput = qtw.QLineEdit()
        self.thicknessInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Thickness (um)', self.thicknessInput)

        self.dataPointsInput = qtw.QLineEdit()
        #this is the max value the validator will take
        self.dataPointsInput.setValidator(qtg.QIntValidator(0,2147483647))
        layout.addRow('Field Delay (sec)',self.dataPointsInput)
        self.setLayout(layout)
