# ------- Features General

# top percentage of sharpest edges that are used for feature curve generation (DFS)
# or directly registered as features (NON-DFS)
featureCountPercentage = 0.05

# ------- Features DFS

# Max length of DFS result when extending features
max_string_length: int = 5

# minimum feature length
min_feature_length: int = 15

# Decides when to stop expanding a feature curve, the lower the earlier it stops
tao = 16

# ------- Features NON-DFS


# All edges that have an sod bigger than this value are additionally registered as features
minSharpness: int = 20

# ------- Charts

# Controls when charts are merged as a reason of having close origins
epsilonFactor = 1 / 3.5

# The minimum distance to a feature a face must have in order to
def getSeedMinFeatureDistance(faceCount: int):
    if faceCount > 10000:
        return 2
    if faceCount > 5000:
        return 1
    return 0


# Charts cannot expand beyond an edge that has a sod value greater than this
sodExpansionLimit = 10
