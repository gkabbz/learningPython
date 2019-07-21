from google.cloud import bigquery
from datetime import datetime, date, timedelta
import os
import logging

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = ['ENTER_USER_CREDENTIALS']

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')


def copy_table(original_table, destination_table, table_date, end_date):
    logging.info(f'''Starting copy operation for {table_date}''')

    client = bigquery.Client(project=['ENTER_PROJECT_NAME'])
    source_dataset_id = 'desktop'
    destination_dataset_id = 'desktop'

    table_suffix = datetime.strftime(table_date, "%Y%m%d")

    origin_table_ref = client.dataset(source_dataset_id).table(f'''{original_table}_{table_suffix}''')
    destination_table_ref = client.dataset(destination_dataset_id).table(f'''{destination_table}_{table_suffix}''')

    job = client.copy_table(
        origin_table_ref,
        destination_table_ref,
        location="US"
        ,
    )
    job.result()

    assert job.state == "DONE"
    destination_table = client.get_table(destination_table_ref)
    assert destination_table.num_rows > 0

    return()


#TODO: ADD inputs to minimize chance of accidental deletion of a dataset
#TODO: Are you sure this is the project you want to delete?
#TODO: Are you sure this is the dataset you want to delete?
#TODO: Are you sure these are the tables you want to delete?
#TODO: Confirm one more time that these are indeed the tables you want to delete?


if __name__ == '__main__':
    table_date = date(2019, 5, 19)
    end_date = date(2019, 7, 14)
    original_table = 'desktop_corpMetrics_post_profilePerInstallAdj'
    destination_table = 'desktop_corp_metrics'

    while table_date <= end_date:
        copy_table(original_table, destination_table, table_date, end_date)
        table_date = table_date + timedelta(1)
        logging.info(f'''starting next loop''')

    logging.info(f'''Job completed''')


