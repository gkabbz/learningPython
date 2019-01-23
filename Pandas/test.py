import pandas as pd
import numpy as np

# Open Files and store in dataframes

historic = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/jun2018.csv'

combinedDF = pd.read_csv(historic, sep=',', header=0, index_col=None, usecols=None, skiprows=None, encoding='utf-8')

# Remove rows without dimensions
combinedDF = combinedDF.loc[combinedDF['submission_date_s3'].notnull()]

# Change Nulls to 0
combinedDF['DAU'].fillna(0, inplace=True)
combinedDF['activeDAU'].fillna(0, inplace=True)
combinedDF['totalURI'].fillna(0, inplace=True)
combinedDF['searches'].fillna(0, inplace=True)
combinedDF['installs'].fillna(0, inplace=True)

# Convert floats to integer and submissionDate to string
combinedDF['submission_date_s3'] = combinedDF.submission_date_s3.astype(int)
combinedDF['submission_date_s3'] = combinedDF.submission_date_s3.astype(str)
combinedDF['DAU'] = combinedDF.DAU.astype(int)
combinedDF['activeDAU'] = combinedDF.activeDAU.astype(int)
combinedDF['totalURI'] = combinedDF.totalURI.astype(int)
combinedDF['searches'] = combinedDF.searches.astype(int)
combinedDF['installs'] = combinedDF.installs.astype(int)


# Clean up attribution fields
# Duplicate columns to preserve original telemetry columns

combinedDF['sourceCleaned'] = combinedDF['source']
combinedDF['mediumCleaned'] = combinedDF['medium']
combinedDF['campaignCleaned'] = combinedDF['campaign']
combinedDF['contentCleaned'] = combinedDF['content']

def mediumCleanup(x):
    # Cleanup direct traffic to equal (none)
    if x[(x.source == 'www.mozilla.org') & (x.medium == '%2528none%2529')]:
        return('(none)')
    #if x['source'] == 'www.mozilla.org' and x['medium'] == '%2528none%2529':
     #   return '(none)'
     # Cleanup organic traffic medium to organic
    #elif 'www.google' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'organic'
    #elif 'bing.com' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'organic'
    #elif 'yandex' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'organic'
    #elif 'search.yahoo' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'organic'
    #elif 'search.seznam' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'organic'
    #else:
    #    return x['medium']


#def sourceCleanup(x):
    # Cleanup direct traffic to equal (none)
    #if x['source'] == 'www.mozilla.org' and x['medium'] == '%2528none%2529':
    #    return '(direct)'
     # Cleanup organic traffic medium to organic
    #elif 'www.google' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'google'
    #elif 'bing.com' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'bing'
    #elif 'yandex' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'yandex'
    #elif 'search.yahoo' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'yahoo'
    #elif 'search.seznam' in x['source'] and x['medium'] == 'referral' and x['campaign'] == '%2528not%2Bset%2529':
    #    return 'seznam'
    #else:
    #   return x['source']


print('cleaning mediums')
combinedDF['mediumCleaned'] = combinedDF.apply(mediumCleanup, axis=1)
print('cleaning sources')
#combinedDF['sourceCleaned'] = combinedDF.apply(sourceCleanup, axis=1)

# Clean direct traffic
# combinedDF.loc[np.where(combinedDF['source'] == 'www.mozilla.org' & combinedDF['medium'] == '%2528none%2529', 'sourceCleaned'] = '(none)'
# combinedDF.loc[combinedDF['source'] == 'www.mozilla.org' & combinedDF['medium'] == '%2528none%2529', 'mediumCleaned'] = '(direct)'



# combinedDF['mediumCleaned'] = np.where(combinedDF['medium'] == '%2528direct%2529', '(direct)',
#                                       np.where(combinedDF['medium'] == ''),, combinedDF['medium'])
# testCleanup = combinedDF[combinedDF['medium'] == '%2528direct%2529']

# Write transformed file and save
print('start writing file')
transformedFile = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/test2.csv'
with open(transformedFile, 'w') as file:
    columnNames = (
    'submissionDate', 'source', 'medium', 'campaign', 'content', 'country', 'DAU', 'activeDAU', 'totalURI', 'searches',
    'installs', 'funnelOrigin', 'mediumCleaned')
    combinedDF.to_csv(file, index=False, header=True, encoding='utf-8')
print('transformed file completed')
