import logging
import os
import urllib3
import tempfile
from google.cloud.storage import Blob
from google.cloud import storage
import pandas as pd

date = '20190227h'

permanent_dir = '/Users/gkaberere/spark-warehouse/testSnippet/metaData'
permanent_file_name = os.path.join(permanent_dir, f'snippets_metadata_{date}.csv')

temp_dir = tempfile.mkdtemp(prefix='snippet_metadata')
temp_file_name = os.path.join(temp_dir, f'snippets_metadata_{date}.csv')

url = f'''https://s3-us-west-2.amazonaws.com/snippets-prod-us-west/metadata/my3zy7my7ca1pa9si1ta3ke7wu9ni7re4tu8zo8d/snippets_metadata_20190227.csv'''


def download_metadata_file(url):
    with tempfile.TemporaryFile(mode='w') as csvfile:
        csvfile.write('Hello World this shit is hard!/n')
        csvfile.write('Hope this works/n')
        print(csvfile.seek(0))
    return csvfile

download_metadata_file(url)

