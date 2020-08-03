import os
from google.cloud import bigquery

# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'

# Connect client and define project
client = bigquery.Client(project='ga-mozilla-org-prod-001')

# Find dataset metadata
datasetID = 'telemetry'
datasetRef = client.dataset(datasetID)
dataset = client.get_dataset(datasetRef)

datasetDescription = dataset.description
print(datasetDescription)
datasetLabels = dataset.labels
print(datasetLabels)

# List datasets in a project
datasets = list(client.list_datasets())
for dataset in datasets:
    print('\t{}'.format(dataset.dataset_id))

# Creating a dataset
datasetID = 'testDataset' # name of dataset you want to create
datasetRef = client.dataset(datasetID) # create a dataset reference using a chosen dataset ID
dataset = bigquery.Dataset(datasetRef) # Construct a dataset object to send to the API
dataset.location = 'US' # Specify geographic location of dataset
dataset = client.create_dataset(dataset) # sends the dataset to the API for creation. Raises exception if dataset already exists

# TODO: Updating / Managing datasets
# How to update dataset (descriptions, expiration time, access controls, labels)
# See: https://cloud.google.com/bigquery/docs/managing-datasets


# TODO: Learn how to get list of tables in datasets
# You can get specific dataset table metadata by running a query e.g.: 'SELECT * FROM telemetry.__TABLES_SUMMARY__'
# The tables_summary__ table is a read only that has the list of tables and vies in a dataset includes fields such as project_id, dataset_id, table_id, creation_time and type (1 for table 2 for view)

# Create an empty table in a dataset
import os
from google.cloud import bigquery
# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'

# Connect client and define project
client = bigquery.Client(project='ga-mozilla-org-prod-001')
datasetRef = client.dataset('testDataset2') # create a dataset reference using a chosen dataset ID
schema = [
    bigquery.SchemaField('fullName', 'STRING', mode='REQUIRED'),
    bigquery.SchemaField('age', 'INTEGER', mode='REQUIRED')
]# define schema in line

# Create a nested table
from google.cloud import bigquery

data = {"id":"1","first_name":"John","last_name":"Doe","dob":"1968-01-22","addresses":[{"status":"current","address":"123 First Avenue","city":"Seattle","state":"WA","zip":"11111","numberOfYears":"1"},{"status":"previous","address":"456 Main Street","city":"Portland","state":"OR","zip":"22222","numberOfYears":"5"}]}
data2 = {"id":"2","first_name":"Jane","last_name":"Doe","dob":"1980-10-16","addresses":[{"status":"current","address":"789 Any Avenue","city":"New York","state":"NY","zip":"33333","numberOfYears":"2"},{"status":"previous","address":"321 Main Street","city":"Hoboken","state":"NJ","zip":"44444","numberOfYears":"3"}]}


client = bigquery.Client(project='ga-mozilla-org-prod-001')
dataset_ref = client.dataset('leanPlum')

schema = [
    bigquery.SchemaField("id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("first_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("last_name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("dob", "DATE", mode="NULLABLE"),
    bigquery.SchemaField(
        "addresses",
        "RECORD",
        mode="REPEATED",
        fields=[
            bigquery.SchemaField("status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("address", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("city", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("state", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("zip", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("numberOfYears", "STRING", mode="NULLABLE"),
        ],
    ),
]
table_ref = dataset_ref.table("test_nested_table")
table = bigquery.Table(table_ref, schema=schema)
table = client.create_table(table)  # API request

print("Created table {}".format(table.full_table_id))


# TODO: How to define schema using a json file
tableName = 'helloTable'
tableRef = datasetRef.table(tableName)
table = bigquery.Table(tableRef, schema=schema)
table = client.create_table(table)

# Create a table from a query result
import os
from google.cloud import bigquery
# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'

client = bigquery.Client()
datasetID = 'testDataset2'
tableName = 'helloWorld9'

jobConfig = bigquery.QueryJobConfig()
# Set the destination table
tableRef = client.dataset(datasetID).table(tableName)
jobConfig.destination = tableRef
sql = """
    SELECT corpus
    FROM `bigquery-public-data.samples.shakespeare`
    GROUP BY corpus;
"""

# Start the query, passing in the extra configuration.
query_job = client.query(
    sql,
    location='US', #Location must match that of the dataset(s) referenced in the query and of the destination table.
    job_config=jobConfig)  # API request - starts the query

query_job.result()  # Waits for the query to finish
print('Query results loaded to table {}'.format(tableRef.path))

# Create a table and loading data from a local file
import os
from google.cloud import bigquery
client = bigquery.Client()
fileName = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181119-20181125Cleaned.csv'
datasetID = 'testDataset2'
tableID = 'helloWorld2'

datasetRef = client.dataset(datasetID) # create a dataset reference using a chosen dataset ID
table_ref = datasetRef.table(tableID) # create a table reference using a chosen table ID
job_config = bigquery.LoadJobConfig() # load job call
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True # auto detect schema
job_config.max_bad_records = 20 # number of bad records allowed before job fails

with open(fileName, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)  # API request

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(job.output_rows, datasetID, tableID))

#
import os
from google.cloud import bigquery
client = bigquery.Client()
fileName = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181119-20181125Cleaned.csv'
datasetID = 'testDataset2'
tableID = 'helloWorld2'

datasetRef = client.dataset(datasetID)  # create a dataset reference using a chosen dataset ID
table_ref = datasetRef.table(tableID)  # create a table reference using a chosen table ID
job_config = bigquery.LoadJobConfig()  # load job call
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.autodetect = True  # auto detect schema
job_config.max_bad_records = 20  # number of bad records allowed before job fails


with open(fileName, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)  # API request

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(job.output_rows, datasetID, tableID))


# Create a date partitioned table from local file
# docs: https://cloud.google.com/bigquery/docs/partitioned-tables
# My preference will be to treat dates as dates as opposed to how we've been storing them as strings
# This will make partitioning by date easier

import os
import pandas as pd
# Transform cleaned file submission_date_s3 to date column
file = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181119-20181125Cleaned.csv'
df = pd.read_csv(file, sep=',', header=0, skiprows=None, encoding='utf-8')
df['submission_date_s3'] = pd.to_datetime(df['submission_date_s3'].astype(str), format='%Y%m%d')
df.to_csv('/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181119-20181125Cleanedv2.csv', index=False, header=True, encoding='utf-8')


from google.cloud import bigquery
client = bigquery.Client()
fileName = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181119-20181125Cleanedv2.csv'
datasetID = 'testDataset2'
tableID = "helloWorldUnpartitioned2"

datasetRef = client.dataset(datasetID) # create a dataset reference using a chosen dataset ID
table_ref = datasetRef.table(tableID) # create a table reference using a chosen table ID
job_config = bigquery.LoadJobConfig() # load job call
job_config.schema = [
    bigquery.SchemaField('submission_date_s3', 'DATE'),
    bigquery.SchemaField('source', 'STRING'),
    bigquery.SchemaField('medium', 'STRING'),
    bigquery.SchemaField('campaign', 'STRING'),
    bigquery.SchemaField('content', 'STRING'),
    bigquery.SchemaField('country', 'STRING'),
    bigquery.SchemaField('DAU', 'INTEGER'),
    bigquery.SchemaField('activeDAU', 'INTEGER'),
    bigquery.SchemaField('totalURI', 'INTEGER'),
    bigquery.SchemaField('searches', 'INTEGER'),
    bigquery.SchemaField('installs', 'INTEGER'),
    bigquery.SchemaField('sourceCleaned', 'STRING'),
    bigquery.SchemaField('mediumCleaned', 'STRING'),
    bigquery.SchemaField('campaignCleaned', 'STRING'),
    bigquery.SchemaField('contentCleaned', 'STRING'),
    bigquery.SchemaField('funnelOrigin', 'STRING'),
    bigquery.SchemaField('countryName', 'STRING')
] # Define schema
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field='submission_date_s3',
    )
job_config.max_bad_records = 20 # number of bad records allowed before job fails

with open(fileName, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)  # API request

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(job.output_rows, datasetID, tableID))

# Check if a table is partitioned - LEGACY - SELECT * FROM [testDataset2.helloWorld8$__PARTITIONS_SUMMARY__]
# Validating if partitioning does improve performance
# Test 1 - using the 20181119-20181125 file, found a query for a specific date in the partitioned data used 7.4 times less data
# Test 2 - using ga data for



#  Append data to a table from a local file
import os
import pandas as pd
# Transform cleaned file submission_date_s3 to date column
file = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181126-20181202Cleaned.csv'
df = pd.read_csv(file, sep=',', header=0, skiprows=None, encoding='utf-8')
df['submission_date_s3'] = pd.to_datetime(df['submission_date_s3'].astype(str), format='%Y%m%d')
df.to_csv('/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181126-20181202Cleanedv2.csv', index=False, header=True, encoding='utf-8')


from google.cloud import bigquery
client = bigquery.Client()
fileName = '/Users/gkaberere/spark-warehouse/weeklyReporting/dimensionedFinal/20181126-20181202Cleanedv2.csv'
datasetID = 'testDataset2'
tableID = "helloWorld8"

datasetRef = client.dataset(datasetID) # create a dataset reference using a chosen dataset ID
table_ref = datasetRef.table(tableID) # create a table reference using a chosen table ID
job_config = bigquery.LoadJobConfig() # load job call
job_config.schema = [
    bigquery.SchemaField('submission_date_s3', 'DATE'),
    bigquery.SchemaField('source', 'STRING'),
    bigquery.SchemaField('medium', 'STRING'),
    bigquery.SchemaField('campaign', 'STRING'),
    bigquery.SchemaField('content', 'STRING'),
    bigquery.SchemaField('country', 'STRING'),
    bigquery.SchemaField('DAU', 'INTEGER'),
    bigquery.SchemaField('activeDAU', 'INTEGER'),
    bigquery.SchemaField('totalURI', 'INTEGER'),
    bigquery.SchemaField('searches', 'INTEGER'),
    bigquery.SchemaField('installs', 'INTEGER'),
    bigquery.SchemaField('sourceCleaned', 'STRING'),
    bigquery.SchemaField('mediumCleaned', 'STRING'),
    bigquery.SchemaField('campaignCleaned', 'STRING'),
    bigquery.SchemaField('contentCleaned', 'STRING'),
    bigquery.SchemaField('funnelOrigin', 'STRING'),
    bigquery.SchemaField('countryName', 'STRING')
] # Define schema
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.write_disposition = 'WRITE_APPEND' #Options are WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY see doc https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs
job_config.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field='submission_date_s3',
    )
job_config.max_bad_records = 20 # number of bad records allowed before job fails

with open(fileName, 'rb') as source_file:
    job = client.load_table_from_file(
        source_file,
        table_ref,
        location='US',  # Must match the destination dataset location.
        job_config=job_config)  # API request

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(job.output_rows, datasetID, tableID))

# Create a table and load data from a query
from google.cloud import bigquery
client = bigquery.Client()
datasetID = 'testDataset2'
tableID = 'helloQueryResult2'

datasetRef = client.dataset(datasetID)
tableRef = datasetRef.table(tableID)
job_config = bigquery.QueryJobConfig() #load job call
#job_config.schema = []
job_config.write_disposition = 'WRITE_APPEND' #Options are WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
job_config.destination = tableRef
sql = """
    SELECT 
    * 
    FROM `ga-mozilla-org-prod-001.telemetry.corpMetrics` 
    WHERE submission_date_s3 = '20181202'
"""

# Start the query, passing in the extra configuration.
query_job = client.query(
    sql,
    # Location must match that of the dataset(s) referenced in the query
    # and of the destination table.
    location='US',
    job_config=job_config)  # API request - starts the query

query_job.result()  # Waits for the query to finish
print('Query results loaded to table {}'.format(tableRef.path))


# Create a table and load data from a file in Google Cloud Storage
import os
from google.cloud import bigquery
# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/marketing-analytics/App Engine - moz-mktg-prod-001/moz-mktg-prod-001-app-engine-GAMozillaProdAccess.json'

client = bigquery.Client()
fileName = 'gs://snippets-data-transfer/daily-tracking-data/snippets_20190102.csv'
datasetID = 'testDataset2'
tableID = "helloWorld12"

datasetRef = client.dataset(datasetID) # create a dataset reference using a chosen dataset ID
table_ref = datasetRef.table(tableID) # create a table reference using a chosen table ID
job_config = bigquery.LoadJobConfig() # load job call
job_config.autodetect = True
job_config.source_format = bigquery.SourceFormat.CSV
job_config.skip_leading_rows = 1
job_config.max_bad_records = 20
job_config.write_disposition = 'WRITE_APPEND' #Options are WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY see doc https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs
#job_config.time_partitioning = bigquery.TimePartitioning(
#    type_=bigquery.TimePartitioningType.DAY,
#    field='submission_date_s3',
#    )
job_config.max_bad_records = 20 # number of bad records allowed before job fails

job = client.load_table_from_uri(
    fileName,
    table_ref,
    location='US',  # Must match the destination dataset location.
    job_config=job_config)  # API request

assert job.job_type == 'load'

job.result()  # Waits for table load to complete.

print('Loaded {} rows into {}:{}.'.format(job.output_rows, datasetID, tableID))


# Create a table and load data and append to tables with suffixes
import os
from google.cloud import bigquery
# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'
client = bigquery.Client()
datasetID = 'testDataset2'
tableName = 'helloQueryResult4'
suffix = '20181203'
tableID = f'{tableName.lower()}_{suffix}'

datasetRef = client.dataset(datasetID)
tableRef = datasetRef.table(tableID)
job_config = bigquery.QueryJobConfig() #load job call
#job_config.schema = []
job_config.write_disposition = 'WRITE_APPEND' #Options are WRITE_TRUNCATE, WRITE_APPEND, WRITE_EMPTY
job_config.destination = tableRef
sql = """
    SELECT 
    * 
    FROM `ga-mozilla-org-prod-001.telemetry.corpMetrics` 
    WHERE submission_date_s3 = '20181203'
"""

# Start the query, passing in the extra configuration.
query_job = client.query(
    sql,
    # Location must match that of the dataset(s) referenced in the query
    # and of the destination table.
    location='US',
    job_config=job_config)  # API request - starts the query

query_job.result()  # Waits for the query to finish
print('Query results loaded to table {}'.format(tableRef.path))



