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


class ColoredButton(qtw.QPushButton):
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

class MyGroupBox(qtw.QGroupBox):
    '''custom groupbox to make the border darker and further style sheet changes
    easier'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setStyleSheet("""QGroupBox {
          border: 1px solid black;
          margin-top: 4px;
        }

        QGroupBox:title{
          top: -8px;
          left: 10px;
          padding-top: 2px;
        }""")

class FieldControllerWidget(MyGroupBox):
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
        self.setMaximumSize(350,400)
        self.setLayout(layout)

class CurrentSourceWidget(MyGroupBox):
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


        self.vLimitInput = qtw.QLineEdit()
        self.vLimitInput.setValidator(qtg.QDoubleValidator())
        layout.addRow('V-Limit', self.vLimitInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class VoltmeterWidget(MyGroupBox):
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

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class SampleInfoWidget(MyGroupBox):
    '''Widget for sample inforamtion inputs'''
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

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class ResistivityWidget(qtw.QFrame):
    '''widget to display the results, located on the right side'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(qtw.QFrame.Box)
        self.setFrameShadow(qtw.QFrame.Plain)
        self.setLineWidth(1)
        layout = qtw.QVBoxLayout()


        layout = qtw.QVBoxLayout()
        self.R1Lbl = qtw.QLabel('R1 (Ohm)')
        layout.addWidget(self.R1Lbl)

        self.R1Display = qtw.QLineEdit()
        self.R1Display.setReadOnly(True)
        layout.addWidget(self.R1Display)

        self.R2Lbl = qtw.QLabel('R2 (Ohm)')
        layout.addWidget(self.R2Lbl)

        self.R2Display = qtw.QLineEdit()
        self.R2Display.setReadOnly(True)
        layout.addWidget(self.R2Display)

        self.Rxy1Lbl = qtw.QLabel('Rxy1 (Ohm)')
        layout.addWidget(self.Rxy1Lbl)

        self.Rxy1Display = qtw.QLineEdit()
        self.Rxy1Display.setReadOnly(True)
        layout.addWidget(self.Rxy1Display)

        self.Rxy2Lbl = qtw.QLabel('Rxy2 (Ohm)')
        layout.addWidget(self.Rxy2Lbl)

        self.Rxy2Display = qtw.QLineEdit()
        self.Rxy2Display.setReadOnly(True)
        layout.addWidget(self.Rxy2Display)

        self.Ratio1Lbl = qtw.QLabel('Ratio1')
        layout.addWidget(self.Ratio1Lbl)

        self.Ratio1Display = qtw.QLineEdit()
        self.Ratio1Display.setReadOnly(True)
        layout.addWidget(self.Ratio1Display)

        self.Ratio2Lbl = qtw.QLabel('Ratio2')
        layout.addWidget(self.Ratio2Lbl)

        self.Ratio2Display = qtw.QLineEdit()
        self.Ratio2Display.setReadOnly(True)
        layout.addWidget(self.Ratio2Display)

        self.FfactorLbl = qtw.QLabel('Ffactor')
        layout.addWidget(self.FfactorLbl)

        self.FfactorDisplay = qtw.QLineEdit()
        self.FfactorDisplay.setReadOnly(True)
        layout.addWidget(self.FfactorDisplay)

        self.HallRatioLbl = qtw.QLabel('HallRatio')
        layout.addWidget(self.HallRatioLbl)

        self.HallRatioDisplay = qtw.QLineEdit()
        self.HallRatioDisplay.setReadOnly(True)
        layout.addWidget(self.HallRatioDisplay)

        spacer = qtw.QSpacerItem(100,100, hPolicy = qtw.QSizePolicy.Preferred,
                                vPolicy = qtw.QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setMaximumSize(200,1000)


class Column4Widget(qtw.QFrame):
    '''widget to display the results, located on the right side'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(qtw.QFrame.Box)
        self.setFrameShadow(qtw.QFrame.Plain)
        self.setLineWidth(1)
        layout = qtw.QVBoxLayout()


        layout = qtw.QVBoxLayout()
        self.AvgSheetResLbl = qtw.QLabel('Avg Sheet Res (Ohm)')
        layout.addWidget(self.AvgSheetResLbl)

        self.AvgSheetResDisplay = qtw.QLineEdit()
        self.AvgSheetResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgSheetResDisplay)

        self.AvgTransResLbl = qtw.QLabel('Avg Trans Res (Ohm)')
        layout.addWidget(self.AvgTransResLbl)

        self.AvgTransResDisplay = qtw.QLineEdit()
        self.AvgTransResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgTransResDisplay)

        self.AvgResLbl = qtw.QLabel('Avg Res (Ohm-cm)')
        layout.addWidget(self.AvgResLbl)

        self.AvgResDisplay = qtw.QLineEdit()
        self.AvgResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgResDisplay)

        self.SheetConcLbl = qtw.QLabel('Sheet Conc (cm-2)')
        layout.addWidget(self.SheetConcLbl)

        self.SheetConcDisplay = qtw.QLineEdit()
        self.SheetConcDisplay.setReadOnly(True)
        layout.addWidget(self.SheetConcDisplay)

        self.BulkConcLbl = qtw.QLabel('Bulk Conc (cm-3)')
        layout.addWidget(self.BulkConcLbl)

        self.BulkConcDisplay = qtw.QLineEdit()
        self.BulkConcDisplay.setReadOnly(True)
        layout.addWidget(self.BulkConcDisplay)

        self.HallCoefLbl = qtw.QLabel('Hall Coef (cm3/C)')
        layout.addWidget(self.HallCoefLbl)

        self.HallCoefDisplay = qtw.QLineEdit()
        self.HallCoefDisplay.setReadOnly(True)
        layout.addWidget(self.HallCoefDisplay)

        self.HallMobilityLbl = qtw.QLabel('Hall Mobility (cm2/Vs)')
        layout.addWidget(self.HallMobilityLbl)

        self.HallMobilityDisplay = qtw.QLineEdit()
        self.HallMobilityDisplay.setReadOnly(True)
        layout.addWidget(self.HallMobilityDisplay)

        spacer = qtw.QSpacerItem(100,100, hPolicy = qtw.QSizePolicy.Preferred,
                                vPolicy = qtw.QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setMaximumSize(200,1000)


class BelowGraphWidget(qtw.QWidget):
    '''widget placed below the graph has buttons and a few other widgets'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = qtw.QVBoxLayout()

        subLayout1 = qtw.QHBoxLayout()
        self.goBtn = ColoredButton('GO')
        self.goBtn.setMinimumSize(400,55)
        subLayout1.addWidget(self.goBtn)

        self.abortBtn = ColoredButton('Abort', rgb = (255,0,0))
        self.abortBtn.setMinimumSize(400,55)
        subLayout1.addWidget(self.abortBtn)


        subLayout2 = qtw.QFormLayout()
        self.pathInput = qtw.QLineEdit("C/Users/lw5968/Documents/Hall Data/test")
        subLayout2.addRow('Output file path',self.pathInput)

        self.rSquareDisplay = qtw.QLineEdit()
        self.rSquareDisplay.setReadOnly(True)
        subLayout2.addRow('R-Square Value',self.rSquareDisplay)

        layout.addLayout(subLayout2)
        layout.addLayout(subLayout1)
        self.setLayout(layout)
