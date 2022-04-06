def formatTime(seconds: float):
    mins = int(seconds // 60)
    secs = round(seconds % 60, 2)

    val = str(int(round(secs, 0))) + "s"

    if mins > 0:
        val = str(mins) + "m " + val
    elif secs < 10:
        val = str(secs) + "s"

    return val
