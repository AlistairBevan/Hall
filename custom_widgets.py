from PyQt5.QtWidgets import (QPushButton,QFormLayout,QWidget,
                             QLineEdit,QVBoxLayout,QSizePolicy,
                             QGroupBox,QHBoxLayout,QComboBox,QFrame,
                             QLabel,QSpacerItem, QStatusBar)
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

        super().__init__(bottom, top, decimals, parent)

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

        self.currentInput = QLineEdit('1e-6')
        self.currentInput.setValidator(QDoubleValidator())
        layout.addRow('Current (A)',self.currentInput)

        self.dwellInput = QLineEdit('1')
        self.dwellInput.setValidator(MyDoubleValidator(0,999.9))
        layout.addRow('Dwell Time (s) 3ms to 999.9s',self.dwellInput)

        self.vLimitInput = QLineEdit('10')
        self.vLimitInput.setValidator(QDoubleValidator())
        layout.addRow('V-Limit', self.vLimitInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class VoltmeterWidget(MyGroupBox):
    '''Widget for displaying the voltmeter controls'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.integratingInput = QComboBox()
        self.integratingInput.addItem('~2s')
        self.integratingInput.addItem('~5s')
        self.integratingInput.addItem('~10s')
        self.integratingInput.addItem('~20s')
        self.integratingInput.setCurrentIndex(1)
        layout.addRow('Integrating Time',self.integratingInput)

        self.RangeInput = QComboBox()
        self.RangeInput.addItem('Enable Auto-Range')
        self.RangeInput.addItem('3mV Range')
        self.RangeInput.addItem('30mV Range')
        self.RangeInput.addItem('300mV Range')
        self.RangeInput.addItem('3V Range')
        self.RangeInput.addItem('30V Range')
        self.RangeInput.addItem('Disable Auto-Range')
        layout.addRow('Range Control',self.RangeInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class SampleInfoWidget(MyGroupBox):
    '''Widget for sample inforamtion inputs'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        layout = QFormLayout()

        self.sampleIDInput = QLineEdit()
        layout.addRow('Sample ID',self.sampleIDInput)

        self.tempInput = QLineEdit('293')
        self.tempInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Temp',self.tempInput)
        self.setLayout(layout)

        self.thicknessInput = QLineEdit('1')
        self.thicknessInput.setValidator(MyDoubleValidator(0))
        layout.addRow('Thickness (um)', self.thicknessInput)

        self.dataPointsInput = QLineEdit('10')
        #this is the max value the validator will take
        self.dataPointsInput.setValidator(QIntValidator(0,2147483647))
        layout.addRow('# of data points',self.dataPointsInput)

        self.setMaximumSize(350,400)
        self.setLayout(layout)

class Inputs(QWidget):
    '''column1 of the Hall tab'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #make the first column
        layout = QVBoxLayout()
        #UI section for sample information
        self.sampleInfoWidget = SampleInfoWidget('Sample Information')
        layout.addWidget(self.sampleInfoWidget)
        #UI section for fieldController
        self.fieldControllerWidget = FieldControllerWidget('Field Controller B-H 15')
        layout.addWidget(self.fieldControllerWidget)
        #UI section for Voltmeter
        self.voltmeterWidget = VoltmeterWidget('Voltmeter controls - Keithley 182')
        layout.addWidget(self.voltmeterWidget)
        #UI section for current
        self.currentWidget = CurrentSourceWidget('Current Source - Keithley 220')
        layout.addWidget(self.currentWidget)
        #add the buttons
        self.goBtn = ColoredButton('GO')
        self.goBtn.setMinimumSize(400,55)
        layout.addWidget(self.goBtn)
        self.abortBtn = ColoredButton('Abort', rgb = (255,0,0))
        self.abortBtn.setEnabled(False)
        self.abortBtn.setMinimumSize(400,55)
        layout.addWidget(self.abortBtn)
        #add a spacer on the bottom
        spacer = QSpacerItem(100,100, hPolicy = QSizePolicy.Preferred,
                                vPolicy = QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Expanding)
        self.setLayout(layout)

    def textDict(self) -> dict:
        '''return a dictionary of the displayed text'''
        dict = {'temp': self.sampleInfoWidget.tempInput.text(),
                'sampleID': self.sampleInfoWidget.sampleIDInput.text(),
                'thickness': float(self.sampleInfoWidget.thicknessInput.text()),
                'dataPoints': int(self.sampleInfoWidget.dataPointsInput.text()),
                'field': float(self.fieldControllerWidget.fieldInput.text()),
                'fieldDelay': float(self.fieldControllerWidget.delayInput.text()),
                'current': float(self.currentWidget.currentInput.text()),
                'dwell': float(self.currentWidget.dwellInput.text()),
                'vLim': float(self.currentWidget.vLimitInput.text()),
                'intgrtTime': self.voltmeterWidget.integratingInput.currentText(),
                'rangeCtrl': self.voltmeterWidget.RangeInput.currentText()}
        return dict


class FitResults1(QFrame):
    '''widget to display the results, located on the right side'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.Box)
        self.setFrameShadow(QFrame.Plain)
        self.setLineWidth(1)
        layout = QVBoxLayout()


        layout = QVBoxLayout()
        self.SheetRes1Lbl = QLabel('Sheet Res 1 (Ohm)')
        layout.addWidget(self.SheetRes1Lbl)

        self.SheetRes1Display = QLineEdit()
        self.SheetRes1Display.setReadOnly(True)
        layout.addWidget(self.SheetRes1Display)

        self.SheetRes2Lbl = QLabel('Sheet Res 2 (Ohm)')
        layout.addWidget(self.SheetRes2Lbl)

        self.SheetRes2Display = QLineEdit()
        self.SheetRes2Display.setReadOnly(True)
        layout.addWidget(self.SheetRes2Display)

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

        self.q1Lbl = QLabel('q1')
        layout.addWidget(self.q1Lbl)

        self.q1Display = QLineEdit()
        self.q1Display.setReadOnly(True)
        layout.addWidget(self.q1Display)

        self.q2Lbl = QLabel('q2')
        layout.addWidget(self.q2Lbl)

        self.q2Display = QLineEdit()
        self.q2Display.setReadOnly(True)
        layout.addWidget(self.q2Display)

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
        self.setMinimumSize(120,500)
        self.setMaximumSize(300,1000)


class FitResults2(QFrame):
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
    '''widget placed below the graph'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        layout = QVBoxLayout()

        self.pathLbl = QLabel('Output File Path')
        layout.addWidget(self.pathLbl)
        self.pathInput = QLineEdit('C:/Users/lw5968/Documents/Hall Data/test.txt')
        layout.addWidget(self.pathInput)

        self.rSqrLbl = QLabel('R-Square Value')
        layout.addWidget(self.rSqrLbl)

        self.rContainer = QFrame()
        self.rContainer.setFrameShape(QFrame.Box)
        self.rContainer.setFrameShadow(QFrame.Plain)
        self.rContainer.setLineWidth(1)

        frameLayout = QHBoxLayout()
        self.box1 = QLineEdit()
        self.box1.setReadOnly(True)
        frameLayout.addWidget(self.box1)
        self.box2 = QLineEdit()
        self.box2.setReadOnly(True)
        frameLayout.addWidget(self.box2)
        self.box3 = QLineEdit()
        self.box3.setReadOnly(True)
        frameLayout.addWidget(self.box3)
        self.box4 = QLineEdit()
        self.box4.setReadOnly(True)
        frameLayout.addWidget(self.box4)
        self.box5 = QLineEdit()
        self.box5.setReadOnly(True)
        frameLayout.addWidget(self.box5)
        self.box6 = QLineEdit()
        self.box6.setReadOnly(True)
        frameLayout.addWidget(self.box6)
        self.box7 = QLineEdit()
        self.box7.setReadOnly(True)
        frameLayout.addWidget(self.box7)
        self.box8 = QLineEdit()
        self.box8.setReadOnly(True)
        frameLayout.addWidget(self.box8)

        self.rContainer.setLayout(frameLayout)
        layout.addWidget(self.rContainer)
        self.setLayout(layout)

    def textDict(self) -> dict:
        '''returns a dictionary of all the text in this widget for ease of access later'''
        dict = {'box1': self.box1.text(), 'box2': self.box2.text(),
                'box3': self.box3.text(), 'box4': self.box4.text(),
                'box5': self.box5.text(), 'box6': self.box6.text(),
                'box7': self.box7.text(), 'box8': self.box8.text(),
                'path': self.pathInput.text()}
        return dict

class IVColumn1(QWidget):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        layout = QVBoxLayout()

        self.currentLbl = QLabel('Current (A)')
        layout.addWidget(self.currentLbl)
        self.currentInput = QLineEdit('1e-6')
        layout.addWidget(self.currentInput)

        self.integratingLbl = QLabel('Voltmeter Integrating Time (s)')
        layout.addWidget(self.integratingLbl)
        self.integratingInput = QComboBox()
        self.integratingInput.addItem('~2s')
        self.integratingInput.addItem('~5s')
        self.integratingInput.addItem('~10s')
        self.integratingInput.addItem('~20s')
        self.integratingInput.setCurrentIndex(1)
        layout.addWidget(self.integratingInput)

        self.voltLimitLbl = QLabel('Voltage Limit (V)')
        layout.addWidget(self.voltLimitLbl)
        self.voltLimitInput = QLineEdit('10')
        layout.addWidget(self.voltLimitInput)

        self.resistanceLbl = QLabel('Resistance (ohms)')
        layout.addWidget(self.resistanceLbl)
        self.resistanceDisplay = QLineEdit('0')
        layout.addWidget(self.resistanceDisplay)

        self.switchLbl = QLabel('Switch Number')
        layout.addWidget(self.switchLbl)
        self.switches = QComboBox()
        for i in range(6):
            self.switches.addItem(str(i + 1))

        layout.addWidget(self.switches)
        self.goBtn = ColoredButton('Go')
        self.goBtn.setMinimumSize(400,55)
        layout.addWidget(self.goBtn)

        self.abortBtn = ColoredButton('Abort', rgb = (255,0,0))
        self.abortBtn.setEnabled(False)
        self.abortBtn.setMinimumSize(400,55)
        layout.addWidget(self.abortBtn)

        spacer = QSpacerItem(100,100, hPolicy = QSizePolicy.Preferred,
                                vPolicy = QSizePolicy.Expanding)
        layout.addItem(spacer)
        self.setLayout(layout)
        self.setMaximumSize(200,1000)

    def textDict(self) -> dict:
        dict = {'current': float(self.currentInput.text()),
                'switchNumber': self.switches.currentText(),
                'intgrtTime': self.integratingInput.currentText(),
                'voltLim': float(self.voltLimitInput.text())}
        return dict

class status(QStatusBar):
    '''status bar at the bottom of the application to display useful information'''
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.setStyleSheet('QStatusBar::item {border: None;}')
        self.switchLbl = QLabel('switch: n/a')
        self.fieldLbl = QLabel('field: Off')
        self.stateLbl = QLabel("state: Idle")
        spacer = QWidget()
        spacer.setFixedWidth(50)
        spacer2 = QWidget()
        spacer2.setFixedWidth(50)
        self.addPermanentWidget(self.stateLbl)
        self.addPermanentWidget(spacer)
        self.addPermanentWidget(self.fieldLbl)
        self.addPermanentWidget(spacer2)
        self.addPermanentWidget(self.switchLbl)
