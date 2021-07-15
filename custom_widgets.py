from PyQt5.QtWidgets import (QPushButton,QFormLayout,QWidget,
                             QLineEdit,QVBoxLayout,QSizePolicy,
                             QGroupBox,QHBoxLayout,QComboBox,QFrame,
                             QLabel,QSpacerItem)
from PyQt5.QtGui import (QValidator,QDoubleValidator,QIntValidator)
#from PyQt5.qtc import ()
from sys import float_info, maxsize



class MyDoubleValidator(QDoubleValidator):

    '''
    Fix for strange behavior of default QDoubleValidator used in
    CurrentSourceWidget
    http://learnwithhelvin.blogspot.com/2010/01/qdoublevalidator.html
    (needed some tweaking)
    '''

    def __init__(self, bottom: float = float_info.min, \
                 top:float = float_info.max, \
                 decimals:int  = float_info.dig, parent: QWidget = None):

        super(MyDoubleValidator, self).__init__(bottom, top, decimals, parent)

    def validate(self, input_value : str, pos : int) -> tuple:
        state, char, pos = super().validate(input_value, pos)

        if input_value == '' or input_value == '.':
            return QValidator.Intermediate,char, pos

        if state != QValidator.State.Acceptable:
            return QValidator.Invalid,char, pos

        return QValidator.Acceptable,char, pos


class ColoredButton(QPushButton):
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

class MyGroupBox(QGroupBox):
    '''custom groupbox to make the border darker and make
    further style sheet changes easier'''
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
        layout = QFormLayout()

        self.fieldInput = QLineEdit('5000')
        self.fieldInput.setValidator(QIntValidator())
        layout.addRow('Field (Gauss)',self.fieldInput)

        self.delayInput = QLineEdit('10')
        self.delayInput.setValidator(QDoubleValidator())
        layout.addRow('Field Delay (sec)',self.delayInput)
        self.setMaximumSize(350,400)
        self.setLayout(layout)

class CurrentSourceWidget(MyGroupBox):
    '''Widget for displaying the current controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.currentInput = QLineEdit()
        self.currentInput.setValidator(QDoubleValidator())
        layout.addRow('Current (A)',self.currentInput)

        self.dwellInput = QLineEdit()
        self.dwellInput.setValidator(MyDoubleValidator(0,999.9))
        layout.addRow('Dwell Time (ms) 3ms to 999.9ms',self.dwellInput)

        self.vLimitInput = QLineEdit()
        self.vLimitInput.setValidator(QDoubleValidator())
        layout.addRow('V-Limit', self.vLimitInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class VoltmeterWidget(MyGroupBox):
    '''Widget for displaying the voltmeter controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.integratingInput = QLineEdit()
        self.integratingInput.setValidator(QIntValidator())
        layout.addRow('Integrating Time',self.integratingInput)

        self.RangeInput = QLineEdit()
        self.RangeInput.setValidator(QDoubleValidator())
        layout.addRow('Range Control',self.RangeInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class SampleInfoWidget(MyGroupBox):
    '''Widget for sample inforamtion inputs'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.SampleIDInput = QLineEdit()
        layout.addRow('Sample ID',self.SampleIDInput)

        self.TempInput = QLineEdit()
        self.TempInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Temp',self.TempInput)
        self.setLayout(layout)

        self.thicknessInput = QLineEdit()
        self.thicknessInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Thickness (um)', self.thicknessInput)

        self.dataPointsInput = QLineEdit()
        #this is the max value the validator will take
        self.dataPointsInput.setValidator(QIntValidator(0,2147483647))
        layout.addRow('Field Delay (sec)',self.dataPointsInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class ResistivityWidget(QFrame):
    '''widget to display the results, located on the right side'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        layout = QVBoxLayout()


        layout = QVBoxLayout()
        self.R1Lbl = QLabel('R1 (Ohm)')
        layout.addWidget(self.R1Lbl)

        self.R1Display = QLineEdit()
        self.R1Display.setReadOnly(True)
        layout.addWidget(self.R1Display)

        self.R2Lbl = QLabel('R2 (Ohm)')
        layout.addWidget(self.R2Lbl)

        self.R2Display = QLineEdit()
        self.R2Display.setReadOnly(True)
        layout.addWidget(self.R2Display)

        self.Rxy1Lbl = QLabel('Rxy1 (Ohm)')
        layout.addWidget(self.Rxy1Lbl)

        self.Rxy1Display = QLineEdit()
        self.Rxy1Display.setReadOnly(True)
        layout.addWidget(self.Rxy1Display)

        self.Rxy2Lbl = QLabel('Rxy2 (Ohm)')
        layout.addWidget(self.Rxy2Lbl)

        self.Rxy2Display = QLineEdit()
        self.Rxy2Display.setReadOnly(True)
        layout.addWidget(self.Rxy2Display)

        self.Ratio1Lbl = QLabel('Ratio1')
        layout.addWidget(self.Ratio1Lbl)

        self.Ratio1Display = QLineEdit()
        self.Ratio1Display.setReadOnly(True)
        layout.addWidget(self.Ratio1Display)

        self.Ratio2Lbl = QLabel('Ratio2')
        layout.addWidget(self.Ratio2Lbl)

        self.Ratio2Display = QLineEdit()
        self.Ratio2Display.setReadOnly(True)
        layout.addWidget(self.Ratio2Display)

        self.FfactorLbl = QLabel('Ffactor')
        layout.addWidget(self.FfactorLbl)

        self.FfactorDisplay = QLineEdit()
        self.FfactorDisplay.setReadOnly(True)
        layout.addWidget(self.FfactorDisplay)

        self.HallRatioLbl = QLabel('HallRatio')
        layout.addWidget(self.HallRatioLbl)

        self.HallRatioDisplay = QLineEdit()
        self.HallRatioDisplay.setReadOnly(True)
        layout.addWidget(self.HallRatioDisplay)

        spacer = QSpacerItem(100,100, hPolicy = QSizePolicy.Preferred,
                                vPolicy = QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setMaximumSize(200,1000)


class Column4Widget(QFrame):
    '''widget to display the results, located on the right side'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        layout = QVBoxLayout()


        layout = QVBoxLayout()
        self.AvgSheetResLbl = QLabel('Avg Sheet Res (Ohm)')
        layout.addWidget(self.AvgSheetResLbl)

        self.AvgSheetResDisplay = QLineEdit()
        self.AvgSheetResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgSheetResDisplay)

        self.AvgTransResLbl = QLabel('Avg Trans Res (Ohm)')
        layout.addWidget(self.AvgTransResLbl)

        self.AvgTransResDisplay = QLineEdit()
        self.AvgTransResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgTransResDisplay)

        self.AvgResLbl = QLabel('Avg Res (Ohm-cm)')
        layout.addWidget(self.AvgResLbl)

        self.AvgResDisplay = QLineEdit()
        self.AvgResDisplay.setReadOnly(True)
        layout.addWidget(self.AvgResDisplay)

        self.SheetConcLbl = QLabel('Sheet Conc (cm-2)')
        layout.addWidget(self.SheetConcLbl)

        self.SheetConcDisplay = QLineEdit()
        self.SheetConcDisplay.setReadOnly(True)
        layout.addWidget(self.SheetConcDisplay)

        self.BulkConcLbl = QLabel('Bulk Conc (cm-3)')
        layout.addWidget(self.BulkConcLbl)

        self.BulkConcDisplay = QLineEdit()
        self.BulkConcDisplay.setReadOnly(True)
        layout.addWidget(self.BulkConcDisplay)

        self.HallCoefLbl = QLabel('Hall Coef (cm3/C)')
        layout.addWidget(self.HallCoefLbl)

        self.HallCoefDisplay = QLineEdit()
        self.HallCoefDisplay.setReadOnly(True)
        layout.addWidget(self.HallCoefDisplay)

        self.HallMobilityLbl = QLabel('Hall Mobility (cm2/Vs)')
        layout.addWidget(self.HallMobilityLbl)

        self.HallMobilityDisplay = QLineEdit()
        self.HallMobilityDisplay.setReadOnly(True)
        layout.addWidget(self.HallMobilityDisplay)

        spacer = QSpacerItem(100,100, hPolicy = QSizePolicy.Preferred,
                                vPolicy = QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setMaximumSize(200,1000)


class BelowGraphWidget(QWidget):
    '''widget placed below the graph has buttons and a few other widgets'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()

        subLayout1 = QHBoxLayout()
        self.goBtn = ColoredButton('GO')
        self.goBtn.setMinimumSize(400,55)
        subLayout1.addWidget(self.goBtn)

        self.abortBtn = ColoredButton('Abort', rgb = (255,0,0))
        self.abortBtn.setMinimumSize(400,55)
        subLayout1.addWidget(self.abortBtn)


        subLayout2 = QFormLayout()
        self.pathInput = QLineEdit("C/Users/lw5968/Documents/Hall Data/test")
        subLayout2.addRow('Output file path',self.pathInput)

        self.rSquareDisplay = QLineEdit()
        self.rSquareDisplay.setReadOnly(True)
        subLayout2.addRow('R-Square Value',self.rSquareDisplay)

        layout.addLayout(subLayout2)
        layout.addLayout(subLayout1)
        self.setLayout(layout)
