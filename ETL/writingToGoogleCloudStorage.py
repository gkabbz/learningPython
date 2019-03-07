from google.cloud import storage
import os

#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= '/Users/gkaberere/Google Drive/Github/gkLocalAppsServiceAccount.json'
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= '/Users/gkaberere/Google Drive/Github/marketing-analytics/App Engine - moz-mktg-prod-001/moz-mktg-prod-001-app-engine-GAMozillaProdAccess.json'

storage_client = storage.Client()
bucket = storage_client.get_bucket("snippets-data-transfer") #bucket name
blob = bucket.blob('metaData/snippets_metadata_20190227j.csv') # The folder / filename of where you want the file saved in cloud storage
blob.upload_from_filename(filename='/users/gkaberere/spark-warehouse/testSnippet/metaData/snippets_metadata_20190227.csv')

# Get list of buckets
buckets = list(storage_client.list_buckets())
print(buckets)



# TODO: Function to upload to google cloud storage
bucket = 'snippets-data-transfer'
blobname = f'metaData/20190227.csv'
csv_file_location = f'/users/gkaberere/spark-warehouse/testSnippet/metaData/snippets_metadata_20190227.csv'

def upload_to_gcs(csvfile, bucket, blobname):
   client = storage.Client()
   bucket = client.get_bucket(bucket)
   blob = bucket.blob(blobname)
   blob.upload_from_filename(filename=csvfile)
   gcslocation = f'gs://{bucket}/{blobname}'
   logging.info(f'Uploaded {gcslocation} ...')
   return gcslocation

#csvfile = download_metadata_file(url, temp_file_name)
upload_to_gcs(csv_file_location, bucket, blobname)


#TODO: Function to upload to google cloud storage using intermidiary temporary files
