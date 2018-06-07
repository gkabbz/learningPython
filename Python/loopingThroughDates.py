from datetime import timedelta, datetime

startPeriod = datetime(year=2017, month=1, day=1)
endPeriod = datetime(year=2017, month=12, day=31)

period = endPeriod - startPeriod
if period.days <= 30:
    startPeriodString = startPeriod.strftime("%Y%m%d")
    endPeriodString = endPeriod.strftime("%Y%m%d")
    print(startPeriodString)
    print(endPeriodString)
else:
    dayChunks = timedelta(days=30)
    currentPeriodStart = startPeriod
    currentPeriodEnd = startPeriod + dayChunks
    currentPeriodChunk = endPeriod - currentPeriodEnd

    while currentPeriodEnd <= endPeriod:
        startPeriodString = currentPeriodStart.strftime("%Y%m%d")
        endPeriodString = currentPeriodEnd.strftime("%Y%m%d")
        print(startPeriodString)
        print(endPeriodString)
        print('next loop')
        currentPeriodStart = currentPeriodEnd + timedelta(days=1)
        currentPeriodEnd = currentPeriodStart + dayChunks
        if currentPeriodStart > endPeriod:
            break
        else:
            if currentPeriodEnd > endPeriod:
                currentPeriodEnd = endPeriod