##Working With Airflow

Getting started
1. Initiate the database

    `airflow initdb`

2. Start the scheduler

    `airflow scheduler`

    To start it in background / redirect the output to quiet the process stream in the terminal
    
    `airflow scheduler &> /dev/null &`
3. Start the webserver
    
    `airflow webserver`
   
   To quiet it do same thing as with the scheduler
   
   `airflow webserver &> /dev/null &`

Once the webserver is up, go to `localhost:8080` in the browser to see the web UI
You can change the port in the config file under `web_server_port = 8080`

To kill the webserver running

- Find the PID currently running `lsof -i tcp:8080`
- Kill the PID `kill <PID>`

The main airflow directory can be found under the home drive. It contains the airflow-webserver.pid, airflow.db, unittests.cfg, and airflow.cfg. It also contains a folder for logs. 

Not present is the dags folder. So we need to create a folder for the dags
`mkdir dags` while in the airflow folder.

#### Airflow Config File

The airflow configuration file is where we can modify many parameters so that airflow fits with my environment. Here you can make modifications to things like:

- location of the dags folder to a different folder
- change the save location of logs
- set the logs to save to cloud storage or to a bucket

#####Setting logs to store in google cloud storage
[Documentation notes](https://airflow.apache.org/docs/stable/howto/write-logs.html#writing-logs-to-google-cloud-storage)

1. Once webserver has been started, go the UI. In top go to Admin -> connections
2. Click create
3. Give a Connection ID (remember it as it will be entered into the config file as well)
4. Select Google Cloud Platform from the Conn Type dropdown
5. Enter the project Id
6. Enter the keyfile path for the service account json or copy the contents of the keyfile json into Keyfile JSON
7. Enter the scopes `https://www.googleapis.com/auth/cloud-platform`
8. Enter desired number of retries and save
9. Edit airflow config file
`vim airflow.cfg`
10. Set `remote_logging = True`
11. Set `remote_base_log_folder = gs://bucket-name/path/to/logs` and save changes
12. Reinitiate the db `airflow initdb`
13. Restart the scheduler and the webserver

You then need to give airflow permissions to be able to write to the gcp storage bucket

`export AIRFLOW_CONN_GOOGLE_CLOUD_DEFAULT='google-cloud-platform://?extra__google_cloud_platform__key_path=/path/to/service/account/file/service_account.json&extra__google_cloud_platform__scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform&extra__google_cloud_platform__project=airflow&extra__google_cloud_platform__num_retries=5'
`

####Overview of the UI
- Dag must be turned on for it to run. Even if you trigger it manually and it isn't turned on the DAG will not run

#### Airflow CLI Useful Commands
`airflow initdb` - when metadata is changed or when initializing

`airflow resetdb` - to rebuild metadata airbase. You'll lose everything so be careful

`airflow upgradedb` - upgrades to latest version of database

`airflow webserver` - Starts a webserver instance. Options include `-p` to set port

`airflow scheduler` - Starts a scheduler instance. Options `-d` - to specify id of dag to run `-sd` to specify directory to look for dags

`airflow worker` - Starts a celery worker node

#### Playing with Dags using CLI
`airflow list_dags` - Shows list of all dags airflow is aware of

`airflow trigger_dag dag_name e.g example_python_operator` - Trigger a dag

`airflow trigger_dag example_branch_operator -e 2020-01-01` - Triggers the dag with a specific start data and it will run multiple times. Concept known as catchup and backfilling. You can also specify a date in the future. Date time is stored internally using UTC. 

`airflow list_dags_runs example_python_operator` - Gives a history of the dag runs

`airflow list_tasks example_python_operator` - Gives lists of task in the dag

`airflow test example_python_operator print_the_context (from task list) 2019-01-01 (execution date in the past)` - Useful for checking the behaviour of a dag

##### What is a DAG?
DAG stands for a directed acyclic graph. A dag is a finite directed graph that doesn't have any loops. 

- In airflow a dag represents a collection of tasks to schedule as well as their dependencies
- Node = task
- Edge = Dependency between N tasks

Between each task there's a dependency (an edge)

###### Important Properties
- `dag_id` - unique identifier of your DAG
- `description` - the description of your DAG
- `start_date` - indicates from which date your DAG should start
- `schedule_interval` - defines how often your DAG runs from the start_date
- `default_args` - a dictionary containing parameters that will be applied to all operators and to your tasks
- `catchup` - to perform scheduler catchup (True by default) Set it as true if you want to run a backfill. 

###### Operator
We create tasks using an operator. 
An operator determines what actually gets done. It can stand on its own.
- Always defines a single task
- Idempotent - always the same result regardless of how many times it is run
- Retry automatically if specified - in case of failure
- A task is created by instantiating an operator class
- An operator defines the nature of this task and how it should be executed
- When an operator is instantiated, this task becomes a node in your DAG

Always a good practice to divide your tasks where each operator only has one thing to do so that it is easier to spot where the problem is. Also since airflow defines each operator as one task, if it fails you have to rerun multiple processes in the situation where you have multiple tasks happing in one operator. ie. if download and processing is combined and the operator fails due to processing. Then you'll have to do the download task again.

There are a lot of operators from python operators to email operators to bash operators. 

All operators inherit from BaseOperator
There are actually 3 types of operators
- **Action Operators** - These perform an action (BashOperator, PythonOperator, EmailOperator)
- **Transfer Operators** - Move data from one system to another (PrestotoMysqlOperator, sftpOperator)
- **Sensor Operators** - Waiting for something to happen (FileSensor etc.)

**Transfer Operators**
- Move data from one system to another
- Data will be pulled out from the source, staged on the machine where the executor is running, and then transferred to the target system
- Don't use these operators if you are dealing with a large amount of data as you will get an out of memory exception

**Sensor Operators**
- Sensor operators inherit of BaseSensorOperator (BaseOperator being the superclass of BaseSensorOperator)
- Monitoring external processes
- Long running task
- Has a poke method that is called repeatedly until it returns True




  
