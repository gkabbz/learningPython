import pandas as pd

# Open file and store in dataframe

file1 = '/users/gkaberere/downloads/Mozilla_Metric_Fetch_20180810.csv'
file2 = '/users/gkaberere/downloads/Mozilla_Trafficking_Fetch_20180810.csv'

metricsDF = pd.read_csv(file1, sep=',', header=0, index_col=None, usecols=None, skiprows=None, encoding='utf-8')
traffickingDF = pd.read_csv(file2, sep=',', header=0, index_col=None, usecols=None, skiprows=None, encoding='utf-8')

# rename traffickingDF AdName column to Adname to allow join
traffickingDF = traffickingDF.rename(columns={'AdName': 'Adname'})


# Merge dataframes on AdName to pull in campaign
joinedDF = metricsDF.merge(traffickingDF, how='left', on='Adname')

# Select columns wanted
select
