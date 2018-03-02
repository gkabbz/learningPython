import pandas as pd
import numpy as np

#Comments will match up with pandasTrainingNotes for easy reference
#1 Defining an index
s = pd.Series(np.random.randint(1,100,5), index = ('a','b', 'c', 'd', 'e'))
print(s)

# 2 if you don't define an index, one is created automatically
series = pd.Series(np.random.randint(0,100,10),index=None)
print(series)
# to see index
print(series.index)

# 3 Data stored in a dict, panda automatically converts key into index
d = {'a':0, 'b':1, 'c':2}
dictSeries = pd.Series(d)
print(dictSeries)

# 4 A series acts like a dict, you can set values by using the index as a key
print(series[9])
#will return value of the 9th item in the series
series[9]=200 # will change it's value into from the random value generated above to 200

