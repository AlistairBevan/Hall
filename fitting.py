import numpy as np
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QObject, pyqtSignal
from typing import List

class Fitter(QObject):

    resultSgnl= pyqtSignal(dict)
    rSqrdSgnl = pyqtSignal(list)

    def fit(self,lines):
        slopes = []
        rSqrds = []

        for line in lines:
            transposeLine = line.T
            x = transposeLine[0]
            y = transposeLine[1]
            slope = np.polyfit(x,y,1)[0]
            mean_y = np.mean(y)
            TSS = np.sum((y - mean_y)**2)
            RSS = np.sum((y - slope*x)**2)
            rSqrds.append(1 - RSS/TSS)
            slopes.append(slope)

        self.rSqrdSgnl.emit(rSqrds)
        return slopes

    def fitfunc(f,q):
        return (q-1)/(q+1) - f * np.arccosh(np.exp(np.log(2)/f)/2)/np.log(2)

    def calculateResults(self, data):
        results = {}
        #convert thickness
        thickness = data['thickness'] * 0.0001
        results['thickness'] = data['thickness']
        results['field'] = data['field']
        results['current'] = data['current']
        B = data['field']
        lines = data['lines']
        #get the 8 resistances by fitting the lines
        R1,R2,R3,R4,R5,R6,R7,R8 = self.fit(lines)
        results['sw1 R'] = R1
        results['sw2 R'] = R2
        results['sw3 R'] = R3
        results['sw4 R'] = R4
        results['sw5 R'] = R5
        results['sw6 R'] = R6
        results['sw7 R'] = R7
        results['sw8 R'] = R8
        #choose the larger of the ratios of R1/R2 see pg.10 of Hall Effect Measurement Handbook
        if R1 < R2:
            q1 = R2/R1
        else:
            q1 = R1/R2

        results['q1'] = q1
        #choose the larger of the ratios of R3/R4 see pg.11 of Hall Effect Measurement Handbook
        if R4 < R3:
            q2 = R3/R4
        else:
            q2 = R4/R3

        results['q2'] = q2
        #get the average pg.11
        qAve = np.mean([abs(q1),abs(q2)])
        results['qAve'] = qAve

        cf = 0
        ff = 1
        while(abs(cf - ff) > 0.001):
            cf = ff
            ff = np.log(2)/(np.log(2*np.cosh((qAve - 1)/(qAve + 1)*np.log(2)/cf)))


        results['ff'] = ff
        #get the sheet resistivity pg.10 and pg.11
        SheetRes1 = np.mean([R1,R2])*np.pi/np.log(2)*ff
        SheetRes2 = np.mean([R3,R4])*np.pi/np.log(2)*ff
        results['sheetRes1'] = SheetRes1
        results['sheetRes2'] = SheetRes2

        SheetRes = np.mean([SheetRes1,SheetRes2])
        results['sheetRes'] = SheetRes

        #pg.13
        pBulk1 = SheetRes1 * thickness
        pBulk2 = SheetRes2 * thickness
        results['pBulk1'] = pBulk1
        results['pBulk2'] = pBulk2
        pBulk = np.mean([pBulk1,pBulk2])
        results['pBulk'] = pBulk

        #pg.17
        Rxy1 = np.mean([-R5,R7])
        Rxy2 = np.mean([-R6,R8])
        results['Rxy1'] = Rxy1
        results['Rxy2'] = Rxy2

        Rxy = np.mean([Rxy1, Rxy2])
        results['AvgTransRes'] = Rxy

        #pg.16?
        rhs1 = Rxy1 * (100000000/B)
        rhs2 = Rxy2 * (100000000/B)
        results['rhs1'] = rhs1
        results['rhs2'] = rhs2
        rhs = np.mean([rhs1,rhs2])
        results['rhs'] = rhs

        if Rxy1 < Rxy2:
            hallRatio = Rxy2/Rxy1
        else:
            hallRatio = Rxy1/Rxy2
        results['hallRatio'] = hallRatio
        rh1 = rhs1 * thickness
        rh2 = rhs2 * thickness
        results['rh1'] = rh1
        results['rh2'] = rh2

        hallCoef = np.mean([rh1, rh2])
        results['hallCoef'] = hallCoef
        sheetConc = 1/(rhs * 1.6022e-19)
        results['sheetConc'] = sheetConc
        bulkConc = sheetConc/(thickness)
        results['bulkConc'] = bulkConc
        hallMobility = abs(hallCoef/pBulk)
        results['hallMob'] = hallMobility
        #emit the results to be displayed and written to file
        self.resultSgnl.emit(results)
