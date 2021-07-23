import os
import json
class Writer:

    temp: str = ''
    sampleID: str = ''
    thickness: str = ''
    filepath: str = ''

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

    def writeToFile(self, results: dict):
        dir = os.path.dirname(self.filepath)
        if not os.path.isdir(dir) and dir != '':
            os.makedirs(dir)
        filepath = self.available_name(self.filepath)
        results['sampleID'] = self.sampleID
        results['temp'] = self.temp
        results['thickness'] = self.thickness
        with open(self.filepath, 'w') as outfile:
            json.dump(results, outfile, indent = 4)

    #avoid overwriting data
    def available_name(self,filename: str) -> str:
        '''checks if the filename is available and returns the next best name'''
        exists = os.path.exists(filename)

        depth =  0

        while exists:
            dot = filename.find('.')
            if dot == -1:#if there is no dot do this
                if depth == 0:
                    filename = filename + ' (1)'

                else:
                    filename = filename[:-2] + str(depth + 1) + ')'
            else:#If there is a dot do this
                if depth == 0:
                    filename = filename[:dot] + '(' + str(depth + 1) + ')' + filename[dot:] #add the brackets and number before the dot
                else:
                    filename = filename[:dot - 2] + str(depth + 1) + filename[dot - 1:]#replace the number

            exists = os.path.exists(filename)
            depth += 1

        return filename
