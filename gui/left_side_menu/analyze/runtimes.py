import scipy.interpolate


def interpolate(dataPoints):
    dataPoints.append((0, 0))
    x, y = zip(*dataPoints)
    return scipy.interpolate.interp1d(x, y)


lscm = [
    (60, 1),
    (120, 2),
    (178, 3),
    (225, 4),
    (335, 8),
    (499, 12),
    (734, 23),
    (1800, 82),
    (2500, 133),
    (4400, 308),
]
lscmInterpolation = interpolate(lscm)

arap = [
    (60, 1),
    (178, 4),
    (225, 5),
    (499, 12),
    (734, 20),
    (1800, 69),
    (2500, 106),
    (4400, 203),
]
arapInterpolation = interpolate(arap)

# average per cone
bffBasic = [(50, 0.16), (152, 0.48), (355, 1.41), (461, 3.08), (616, 9)]
bffBasicInterpolation = interpolate(bffBasic)

# average per cone
bffComplex = [
    (60, 1.97),
    (120, 6.6),
    (178, 12.04),
    (225, 16.95),
    (335, 39.28),
    (499, 65.07),
    (734, 108.9),
]
bffComplexInterpolation = interpolate(bffComplex)


def computeTime(interpolation, triangleCount: int):
    triangleCount = triangleCount / 1000
    return interpolation(triangleCount)


def lscmTime(triangleCount: int):
    return computeTime(lscmInterpolation, triangleCount)


def arapTime(triangleCount: int):
    return computeTime(arapInterpolation, triangleCount)


def bffTime(triangleCount: int, basic: bool):
    return computeTime(
        bffBasicInterpolation if basic else bffComplexInterpolation, triangleCount
    )
