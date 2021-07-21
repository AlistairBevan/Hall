import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal
from miscellaneous import available_name

class Fitter(QObject):

    done = pyqtSignal(dict)

    def fit(self,lines):
        p = []
        for line in lines:
            transposeLine = line.T
            x = transposeLine[0]
            y = transposeLine[1]

            p.append(np.polyfit(x,y,1))
        return p

    def calculateResults(self, lines: List, thickness: float):
        results = {}
        #convert thickness
        thickness = thickness * 0.0001
        #get the 8 resistances by fitting the lines
        R1,R2,R3,R4,R5,R6,R7,R8 = self.fit(lines)

        #choose the larger of the ratios of R1/R2 see pg.10 of Hall Effect Measurement Handbook
        if R1 < R2:
            q1 = R2/R1
        else:
            q1 = R1/R2

        results['q1'] = q1
        #choose the larger of the ratios of R3/R4 see pg.11 of Hall Effect Measurement Handbook
        if R4 < R3:
            q2 = R4/R3
        else:
            q2 = R3/R4
        results['q2':q2]
        #get the average pg.11
        qAve = np.mean([q1,q2])
        results['qAve'] = qAve

        cf = 0
        ff = 1
        while abs(cf - ff) > 0.001:
            cf = ff
            ff = np.log(2)/(np.log(2*np.cosh((qAve - 1)/(qAve + 1)*np.log(2)/cf)))

        results['ff'] = ff
        #get the sheet resistivity pg.10 and pg.11
        pSheet1 = np.mean([R1,R2])*np.pi/np.log(2)*ff
        pSheet2 = np.mean([R3,R4])*np.pi/np.log(2)*ff
        results['pSheet1'] = pSheet1
        results['pSheet2'] = pSheet2

        pSheet = np.mean([pSheet1,pSheet2])
        results['pSheet' = pSheet]

        #pg.13
        pBulk1 = pSheet1 * thickness
        pBulk2 = pSheet2 * thickness
        results['pBulk1'] = pBulk1
        results['pBulk2'] = pBulk2
        pBulk = np.mean([pBulk1,pBulk2])
        results['pBulk'] = pBulk

        #pg.17
        Rxy1 = np.mean([R5,R6])
        Rxy2 = np.mean([R6,R7])
        results['Rxy1'] = Rxy1
        results['Rxy2'] = Rxy2

        Rxy = np.mean([Rxy1, Rxy2])
        results['Rxy'] = Rxy

        #pg.16?
        rhs1 = Rxy1 * (100000000/B)
        rhs2 = Rxy2 * (100000000/B)

        rhs = np.mean([rhs1,rhs2])

        if Rxy1 < Rxy2:
            hallRatio = Rxy1/Rxy2
        else:
            hallRatio = Rxy2/Rxy1

        rh1 = rhs1 * thickness
        rh2 = rhs2 * thickness

        hallCoef = np.mean([rh1, rh2])
        results['hallCoef'] = hallCoef
        sheetConc = 1/(rhs * 1.6022e-19)
        results['sheetConc'] = sheetConc
        bulkConc = sheetConc/(0.0001 * thickness)
        results['bulkConc'] = bulkConc

        #emit the results to be displayed and saved
        done.emit(results)
        return results

class Writer:

    def writeToFile(filepath: str, results: dict):
        filepath = available_name(filepath)
        f = open(filepath, 'a')
        f.write('Header')
        for key in results.keys():
            f.write(f'{key} + : + {str(results[key])} + \n)
