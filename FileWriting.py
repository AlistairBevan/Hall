import os
from datetime import datetime

class Writer:
    """class for writing the results to a file, its setter functions are
    connected to the inputs in the GUI so they will update in real time"""
    temp: str = ''
    sampleID: str = ''
    thickness: str = ''
    filepath: str = ''
    rSqrd: list = []#emitted to when fitted

    def __init__(self,sampleID,temp,thickness,filepath):
        self.temp = temp
        self.sampleID = sampleID
        self.thickness = thickness
        self.filepath = filepath

    #write setter methods to be connected to signals
    def setTemp(self, temp: str):
        self.temp = temp

    def setThickness(self, thickness: str):
        self.thickness = thickness

    def setFilepath(self, filepath: str):
        self.filepath = filepath

    def setSampleID(self, sampleID: str):
        self.sampleID = sampleID

    def setRSqrd(self, rSqrd: list):
        self.rSqrd = rSqrd

    def writeToFile(self, results: dict):
        """writes the results to a file connected to the result signal of the fitter"""
        dir = os.path.dirname(self.filepath)
        if not os.path.isdir(dir) and dir != '':
            os.makedirs(dir)
        self.filepath = self.available_name(self.filepath)
        with open(self.filepath, 'w') as outfile:
            outfile.write(f"Sample ID:\t\t{self.sampleID}\n\n")
            dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            outfile.write(f"Date Time:\t\t{dt_string}\n\n")
            outfile.write(f"Sample Temperature:\t\t{self.temp}\n")
            outfile.write(f"Sample Current (Amps):\t\t{results['current']}\n")
            outfile.write(f"Magnetic Field (Gauss):\t\t{results['field']}\n")
            outfile.write(f"Epi Thickness (microns):\t\t{self.thickness}\n\n")
            outfile.write('SW\tB\tSlope (Ohm)\tR-Sq\n\n')
            B = 0
            for i in range(1,9):
                if i == 5:
                    B = 5000
                if i == 7:
                    B = -5000
                outfile.write(f"{str(i)}\t{-B}\t{results['sw'+str(i)+' R']:.5e}\t{self.rSqrd[i - 1]:.5f}\n")

            outfile.write('\n\n\n')
            outfile.write(f"Sheet Res1:\t\t{results['sheetRes1']:.5e} ohm\n")
            outfile.write(f"Sheet Res2:\t\t{results['sheetRes2']:.5e} ohm\n")
            outfile.write(f"Rxy1:\t\t{results['Rxy1']:.5e} ohm\n")
            outfile.write(f"Rxy2:\t\t{results['Rxy2']:.5e} ohm\n")
            outfile.write(f"q1:\t\t{results['q1']:.4f}\n")
            outfile.write(f"q2:\t\t{results['q2']:.4f}\n")
            outfile.write(f"Hall Ratio:\t\t{results['hallRatio']:.5e}\n")
            outfile.write(f"Ffactor:\t\t{results['ff']:.4f}\n")
            outfile.write('\n\n\n')
            outfile.write(f"Ave Trans Res:\t{results['AvgTransRes']:.5e}\tohm\n")
            outfile.write(f"Ave Sheet Res:\t{results['sheetRes']:.5e}\tohm\n")
            outfile.write(f"Ave Res:\t{results['pBulk']:.5e}\tohm-cm\n")
            outfile.write(f"Sheet Conc:\t{results['sheetConc']:.5e}\tcm-2\n")
            outfile.write(f"Bulk Conc:\t{results['bulkConc']:.5e}\tcm-3\n")
            outfile.write(f"Hall Coef:\t{results['hallCoef']:.5e}\tcm3 / C\n")
            outfile.write(f"Hall Mobility:\t{results['hallMob']:.5e}\tcm2")

    #avoid overwriting data
    def available_name(self,filename: str) -> str:
        """checks if the filename is available and returns the next best name if its not"""
        exists = os.path.exists(filename)

        depth =  0

        while exists:
            dot = filename.find('.')
            if dot == -1:#if there is no dot do this
                if depth == 0:
                    filename = filename + ' (1)'

                else:
                    filename = filename[:filename.rfind('(')+1] + str(depth + 1) + ')'
                    print(filename)
            else:#If there is a dot do this
                if depth == 0:
                    filename = filename[:dot] + '(' + str(depth + 1) + ')' + filename[dot:] #add the brackets and number before the dot
                else:
                    filename = filename[:filename.rfind('(')+1] + str(depth + 1) + filename[filename.rfind(')'):]#replace the number

            exists = os.path.exists(filename)
            depth += 1

        return filename


if __name__ == '__main__':
    writer = Writer('','','','')
    filename = 'test'
    for i in range(13):
        new_filename = writer.available_name(filename)
        f = open(new_filename, 'w')
        f.write('hello')
        f.close()
