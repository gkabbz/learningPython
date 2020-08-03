from google.cloud import bigquery
from datetime import datetime, date, timedelta
import os
import logging

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/gkaberere/Google Drive/Github/marketing-analytics/AppEngine-moz-mktg-prod-001/moz-mktg-prod-001-app-engine-GAMozillaProdAccess.json'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s: %(message)s')


def delete_bq_table(delete_table, table_date):
    logging.info(f'''Starting copy operation for {table_date}''')

    client = bigquery.Client(project='ga-mozilla-org-prod-001')
    dataset_id = 'desktop'

    table_suffix = datetime.strftime(table_date, "%Y%m%d")

    delete_table_ref = client.dataset(dataset_id).table(f'''{delete_table}_{table_suffix}''')

    client.delete_table(delete_table_ref)
    logging.info(f'''Table {delete_table_ref} deleted''')
    return()


if __name__ == '__main__':
    table_date = date(2019, 5, 20)
    end_date = date(2019, 7, 14)
    delete_table = 'desktop_corp_metrics'

    while table_date <= end_date:
        delete_bq_table(delete_table, table_date)
        table_date = table_date + timedelta(1)
        logging.info(f'''starting next loop''')

    logging.info(f'''Job completed''')


