
class Fitter():

    def fit(self,lines):
        p = []
        for line in lines:
            transposeLine = line.T
            x = transposeLine[0]
            y = transposeLine[1]

            p.append(np.polyfit(x,y,1))
        return p
