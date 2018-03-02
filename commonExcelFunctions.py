import pandas as pd
import numpy

# 1 Column Totals and Subtotals
# 2 Functions on columns - adding, subtracting, calculating %s, calculating % change etc.
# 3 Sumifs
# 4 Countifs
# 5 Vlookup
# 6 Formatting dates
# 7 Formatting numbers
# 8 Combining multiple excel files into one
# 9 Slicing one excel file into multiple
# 10 Concatenate - combining two columns together

# Closing a file
# use python to join the telemetry attribution data sets that i downloaded from redash as part of attribution project

# Reading a file with Pandas
# Key items to include when opening a file File location, delimiter, header, names (if no header), usecols (if you only want a specific no of columns),
df = pd.read_csv('samplePandasDataSet.csv', delimiter='\t', header=0)
print(df)

dfTable = pd.read_table('samplePandasDataSet.csv')
