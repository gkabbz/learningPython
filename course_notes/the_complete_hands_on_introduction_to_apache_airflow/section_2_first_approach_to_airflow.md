#What is Airflow

- It is a powerful orchestrator
- Way to programmatically author, schedule and monitor data pipelines

#####Core Components
1. Web Server - Allows you to have a UI to monitor the pipelines and add connections
2. Scheduler - In charge of scheduling tasks based on dependencies
3. Metadata Database - Where all data related to the jobs are stored
4. Executor - Defines how tasks should be executed
5. Worker - Subprocess executing the task received by the executor

#####Key Concepts
1. DAG - A graph object representing your data pipeline
2. Operator - Describe a single task in your data pipeline
3. Task - An instance of an operator
4. TaskInstance - Represents a specific run of a task = DAG + TASK + POINT IN TIME
5. Workflow - Combination of all above

Airflow is not a data streaming solution. Primarily built to perform batch jobs.

# How Airflow Works
1. The scheduler reads the DAG folder
2. Your DAG is run by a process to create a DagRun based on the scheduling parameters of your DAG
3. A TaskInstance is instantiated for each Task that needs to be executed and flagged to "Scheduler" in the metadata 
database
4. The scheduler gets all TaskInstances flagged "Scheduled" from the metadata database, changes the state to "Queued" 
and sends them to the executors to be executed
5. Executors pull out Tasks from the queue (depending on your execution setup), change the state from "Queued" to 
"Running" and Workers start executing the TaskInstances
6. When a Task is finished, the Executor changes the state of that task to its final state (success, failed, etc) in 
the database and the DAGRun is updated by the Scheduler with the state "Success" or "Failed". Of course, the web server 
periodically fetch data from the metadatabase to update the UI

#Installing Airflow
1. Since airflow is Python based, it's installed using pip
    `pip install apache-airflow`
2. To install optional airflow packages you can specify them during install
    `pip install apache-airflow[gcp, celery, crypto, mysql, rabbitmq, redis]`
3. To specify a specific version of airflow 
    `pip install "apache-airflow[gcp, celery, crypto, mysql, rabbitmq, redis]"==1.10.10`
4. To specify a requirements file
    `pip install "apache-airflow[gcp, celery, crypto, mysql, rabbitmq, redis]"==1.10.11 --constraint requirements-python3.7.txt`

####Understanding the Airflow Setup
1. To initialize the metadata database
`airflow initdb`
2. If you ls you'll see a folder called airflow. The contents of the folder are:
- airflow.cfg - Configuration file of airflow. Set ports, path of dag folder
- airflow.db - Corresponds to the sqllite db when using default airflow configuration. All metadata stored here.
- logs - log events 
- unittests.cfg - used for unit testing dags
3. Create a folder called DAGs
- First check where the dags folder is set in the config file. `grep dags_folder airflow.cfg` (Need to be in airflow folder)
- Create folder in that path.
- Alternatively you could create a folder elsewhere and change the path in the config file

####UI Walkthrough
Views
Graph View - Visualize tasks and dependencies of dags. 
Tree View - Gives true represenation of dag that spans across time. Each column corresponds to a dag run and each square correspends to a specific run.
Dialog box - Has lots of options. Can see the log effects of the corresponding task. 
Gantt Chart - Can see bottlenecks and where the bulk of time is spent for a specific dag run

####Command Line Walkthrough
`airflow initdb` - used to setup the sql db that airflow uses

`airflow resetdb` - used to rebuild metadata db to get a fresh new db. You'll lose everything including variables, connections etc

`airflow webserver` - to start webserver and get access to UI

`airflow scheduler` - to start the scheduler

`airflow worker` - starts a celery worker to process commands in a distributed manner

`airflow list_dags` - to see list of dags

`airflow list_tasks $[DAG_NAME]` - see list of tasks in a dag

`airflow list_tasks $[DAG_NAME] --tree` - see the dependencies of tasks in a given dag

`airflow test $[DAG_NAME] $[task_name] $[execution_date_in_past]` - Run a given task without checking for dependencies and storing states in the metadata database. useful for unit testing tasks.


