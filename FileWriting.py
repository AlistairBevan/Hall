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
        filepath = self.available_name(self.filepath)
        f = open(filepath, 'a')
        f.write(f'sampleId: {self.sampleID}\n')
        f.write(f'temp (K): {self.temp}\n')
        f.write(f'thickness (um): {self.thickness}\n')

        for key in results.keys():
            f.write(f'{key}:  {str(results[key])}\n')

    #avoid overwriting data
    def available_name(filename: str) -> str:
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
