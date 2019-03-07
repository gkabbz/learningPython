import json

variables = {
    "metadata_url": "https://s3-us-west-2.amazonaws.com/snippets-prod-us-west/metadata/za7to7mi9cu9sy5ko1zy/",
    "bucket": "snippets-data-transfer",
    "project": "ga-mozilla-org-prod-001",
    "gcs_file_name": "gs://snippets-data-transfer/metaData"
}

with open('snippetsEnvVariables2.json', 'w') as outfile:
    json.dump(variables, outfile)