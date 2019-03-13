# Using the public dataset on names by year to populate a table in development
# Code reads from the development table to find the max date then pulls the next years data each time it's run
# This is to allow proper testing of app once deployed

import os
from google.cloud import bigquery

# Set environment variable to authenticate using service account
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Python/Github Personal/gkPersonalGCPLocalServiceAccount.json'

def ingestNextYear():
    client = bigquery.Client()
    datasetID = 'Development'
    tableName = 'usNamesBQPublicData'

    jobConfig = bigquery.QueryJobConfig()
    jobConfig.write_disposition = 'WRITE_APPEND'
    # Set the destination table
    tableRef = client.dataset(datasetID).table(tableName)
    jobConfig.destination = tableRef
    sql = """
    SELECT
    *
    FROM
    `bigquery-public-data.usa_names.usa_1910_2013`
    WHERE
    year = (SELECT max(year) FROM `development-184611.Development.usNamesBQPublicData`)+1
    """
    # TODO: Store new data appended to development table
    # Start the query, passing in the extra configuration
    query_job = client.query(
    sql,
    job_config=jobConfig)

    query_job.result()
    print('Query result loaded to table {}'.format(tableRef.path))

if __name__ == '__main__':
    ingestNextYear()