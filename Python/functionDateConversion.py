import pandas as pd

#TODO: I want the function to take a string input stored in a dataframe column and convert it to date

def date_time_conv(changeToDateFmt):
    return pd.to_datetime(changeToDateFmt, format="%Y%m%d")

# Applying the function to a variable
date = '20180101'
dateConverted = date_time_conv(date)
print(dateConverted)

# Applying the function to a pandas dataframe
df = pd.read_csv('/Users/gkaberere/Google Drive/Python/Github/learningPython/dateConversionFunction.csv')
df['converted_submission_date_s3'] = df['submission_date_s3'].apply(date_time_conv)
print(df.head())