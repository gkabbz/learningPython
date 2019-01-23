import pandas as pd
from google.cloud import bigquery
import os

# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'

# Connect client and define project
client = bigquery.Client(project='ga-mozilla-org-prod-001')

# Set Query
query = '''
SELECT * 
FROM `ga-mozilla-org-prod-001.telemetry.corpMetrics` 
WHERE submission_date_s3 = '20181201' 
LIMIT 50
'''

# Run Query and view results
queryJob = client.query(query)
data = list(queryJob.result())
for row in data:
    print(row)

# Pass results to pandas
df = queryJob.to_dataframe()
df.head(3)
df.info()

