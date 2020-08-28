# Code companion for section_3_coding_your_first_data_pipeline.md

from airflow import DAG

#1. Setting up the DAG Skeleton

# Instantiate a DAG object using with
# with statement makes sure that whatever happens in its scope e.g. exception, the resources will be properly released
# Makes code cleaner as don't have to create a variable for each task
# assign dag_id - has to be unique.
# Set schedule_interval - either cron operations or explicit time
with DAG(dag_id="twitter_dag", schedule_interval="@daily") as dag:
    None

#2. Operators

#2a) Setting a Sensor Operator
from airflow import DAG
# To import File Sensor
from airflow.contrib.sensors.file_sensor import FileSensor
from datetime import datetime

# Try and have these args be universal across the dags. ie. don't have different start dates for different dags
default_args = {
        "start_date": datetime(2020, 1, 1),
        "owner":"airflow"
}
with DAG(dag_id="twitter_dag", schedule_interval="@daily", default_args=default_args) as dag:
        waiting_for_tweets = FileSensor(
            # need to give it a task id
            task_id="waiting_for_tweets",
            # parameter required for FileSensor operator
            fs_conn_id="fs_tweet",
            # parameter required for FileSensor operator
            filepath="data.csv",
            # how often the sensor operator should check the file (seconds)
            poke_interval=5)
        None

#To set the connection in Airflow, go to the UI
#1. Under Admin -> Connections click create
#2. Conn Id = fs_tweet
#3. Conn Type = Select File(path)
#4. Extra = {"path":"/home/vagrant/airflow/dags/data"} - sets the file path to check for the file data.csv from DAG above
#5. Save


#2b) Setting a Python Operator
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
# To import Python Operator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# To avoid having issues finding the python files need to set environment python path variable to search location
# of the python files
import fetching_tweet
import cleaning_tweet

# Try and have these args be universal across the dags. ie. don't have different start dates for different dags
default_args = {
        "start_date": datetime(2020, 1, 1),
        "owner":"airflow"
}
with DAG(dag_id="twitter_dag", schedule_interval="@daily", default_args=default_args) as dag:
        waiting_for_tweets = FileSensor(
            # need to give it a task id
            task_id="waiting_for_tweets",
            # parameter required for FileSensor operator
            fs_conn_id="fs_tweet",
            # parameter required for FileSensor operator
            filepath="data.csv",
            # how often the sensor operator should check the file (seconds)
            poke_interval=5)

        fetching_tweets = PythonOperator(
            task_id = 'fetching_tweets',
            # calling the python function from the python file (change main to function name when needed)
            python_callable= fetching_tweet.main
        )

        cleaning_tweet = PythonOperator(
            task_id = 'cleaning_tweets',
            python_callable = cleaning_tweet.main
        )
        None


#2c) Using Bash Operator and Hive Operator
from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.python_operator import PythonOperator
# To import bash operator
from airflow.operators.bash_operator import BashOperator
# To import hive Operator
from airflow.operators.hive_operator import HiveOperator
from datetime import datetime

# To avoid having issues finding the python files need to set environment python path variable to search location
# of the python files
import fetching_tweet
import cleaning_tweet

# Try and have these args be universal across the dags. ie. don't have different start dates for different dags
default_args = {
        "start_date": datetime(2020, 1, 1),
        "owner":"airflow"
}
with DAG(dag_id="twitter_dag", schedule_interval="@daily", default_args=default_args, catchup=False) as dag:
        waiting_for_tweets = FileSensor(
            # need to give it a task id
            task_id="waiting_for_tweets",
            # parameter required for FileSensor operator
            fs_conn_id="fs_tweet",
            # parameter required for FileSensor operator
            filepath="data.csv",
            # how often the sensor operator should check the file (seconds)
            poke_interval=5)

        fetching_tweets = PythonOperator(
            task_id = 'fetching_tweets',
            # calling the python function from the python file (change main to function name when needed)
            python_callable= fetching_tweet.main
        )

        cleaning_tweet = PythonOperator(
            task_id = 'cleaning_tweets',
            python_callable = cleaning_tweet.main
        )

        storing_tweets = BashOperator(
            task_id="storing_tweets",
            # enter bash command
            bash_command="hadoop fs -put -f /tmp/data_cleaned.csv /tmp/"
        )

        loading_tweets = HiveOperator(
            task_id="loading_tweets",
            hql="LOAD DATA INPATH '/tmp/data_cleaned.csv' INTO TABLE tweets"
        )
        None

# Adding Dependencies
waiting_for_tweets >> fetching_tweets >> cleaning_tweet >> storing_tweets >> loading_tweets


#3. Playing with Backfill and Catchup
