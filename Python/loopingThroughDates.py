from datetime import timedelta, datetime

startPeriod = datetime(year=2017, month=2, day=16)
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

    while currentPeriodEnd <= endPeriod:
        startPeriodString = currentPeriodStart.strftime("%Y%m%d")
        endPeriodString = currentPeriodEnd.strftime("%Y%m%d")
        metrics = "submission_date_s3 >= '{}' AND submission_date_s3 <= '{}'".format(startPeriodString,
                                                                                     endPeriodString)
        print(metrics)
        print('next loop')
        currentPeriodStart = currentPeriodEnd + timedelta(days=1)
        currentPeriodEnd = currentPeriodStart + dayChunks
        if currentPeriodStart > endPeriod:
            break
        else:
            if currentPeriodEnd > endPeriod:
                currentPeriodEnd = endPeriod



