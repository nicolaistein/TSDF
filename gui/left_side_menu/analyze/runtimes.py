import scipy.interpolate

lscm = [(60,1), (120,2), (178,3), (225,4), (335,8), (499,12),
        (734,23), (1800,82), (2500,133), (4400,308)]

arap = [(60,1), (178,4), (225,5), (499,12),
        (734,20), (1800,69), (2500,106), (4400,203)]

#average per cone
bffBasic = [(50,0.16), (152,0.48), (355,1.41), (461,3.08), (616,9)]

#average per cone
bffComplex = [  (60,1.97), (120,6.6), (178,12.04), (225,16.95),
                (335,39.28), (499,65.07), (734,108.9)]

def computeTime(dataPoints, triangleCount:int):
    print("computeTime")
    print(dataPoints)
    x, y = zip(dataPoints)
    y_interpolation = scipy.interpolate.interp1d(x, y)
    return y_interpolation(triangleCount)

def lscmTime(triangleCount:int):
    return computeTime(lscm, triangleCount)
    
def arapTime(triangleCount:int):
    return computeTime(arap, triangleCount)
    
def bffTime(triangleCount:int, basic:bool):
    return computeTime(bffBasic if basic else bffComplex, triangleCount)
