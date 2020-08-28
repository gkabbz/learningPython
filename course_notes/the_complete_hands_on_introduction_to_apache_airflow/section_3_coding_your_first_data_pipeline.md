#### What is a DAG?
- A DAG is a finite directed graph that doesn't have any cycles (loops).
    - A cycle is a series of vertices that connect back to each other making a loop
- In apache airflow a DAG _represents a collection of tasks to run, organized in a way that represents their dependencies and relationships_
    - It's job is to make sure that tasks happen at the right time in the right order with the right handling of any unexpected issues
    - It ultimately defines our workflow
- Each Node is a task
- Each edge is a dependency

#####Important Properties
- DAGs are defined in Python files placed into Airflow's DAG_FOLDER (usually ~/airflow/dags)
- dag_id serves as a unique identifier of your DAG
- description - the description of your dag
- start_date - tells when your DAG should starts. Dag is triggered after the scheduled start_date
- schedule_interval - defines how often your DAG runs
- depend_on_past - run the next DAGRun if the previous one completed successfully
- default_args - a dictionary of variables to be used as constructor keyword parameter when initializing operators

#####DAG Skeleton
The basic skeleton of a dag includes:
1. Importing the DAG class 
2. Naming the dag as a `dag_id`
3. Scheduling the dag using `schedule_interval`

See: section_3_twitter_dag.py for example: part 1

#####Operators
1. Definition of a single task
2. Should be idempotent
    - Meaning your operator should product the same result regardless of how many times it is run
3. Retry automatically - in case of a failure
4. A Task is created by instantiating an Operator class
5. An Operator defines the nature of this Task and how it should be executed
6. When an operator is instantiated, this task becomes a node in your DAG

Apache airflow provides many operators:
1. BashOperator - Executes a bash command
2. PythonOperator - Calls an arbitrary python function
3. EmailOperator - Sends an email
4. MySQLOperator, SqliteOperator, PostgresOperator - Executes a sql command
5. You can also create your own operators

#####Types of Operators:
- All operators inherit from BaseOperator
- There are actually three types of operators:
    1. Action Operators - That perform an action (BashOperator, PythonOperator, EmailOperator)
    2. Transfer Operators - That move data from one system to another (PrestoToMySqlOperator, sftpOperator)
    3. Sensor Operators - waiting for data to arrive at a defined location
     
#####Transfer Operators
- Operators that move data from one system to another
- Data will be pulled out from the source, staged on the machine where the executor is running and the transferred
to the target systm
- Don't use these operators if you are dealing with a large amount of data to avoid getting memory errors

#####Sensor Operators
- Sensor operators inherit of BaseSensorOperator (BaseOperator being the superclass of BaseSensorOperator)
- They are useful for monitoring external processes like waiting for files ot be uploaded in HDFS or a partition 
appearing in Hive
- They are basically long running task
- The Sensor Operator has a poke method called repeatedly until it returns True (it is the method used for monitoring
the external process)

#####Organize Your Tasks
######How to make dependencies in Airflow?
There are two ways of describing dependencies between operators in Apache Airflow:
1. By using the traditional operator relationships with:
    - `set_upstream()`
    - `set_downstream()`
    e.g. t1.set_downstream(t2); t2.set_downstream(t3)
    t3.set_upstream(t2); t2.set_upstream(t1)
2. From Apache Airflow 1.8 you can use Python bitshift operators
    - `<< (= set_upstream)`
    - `>> (= set_downstream)`
    e.g. t1 >> t2 >> t3
    t4 << t3 << t2
    
#####How the Scheduler Works
- The scheduler's role is to monitor all tasks and DAGs to ensure that everything is executed based on the start_date
and the schedule_interval parameters. There is also an execution_date which is the latest time your DAG has been
executed (last(date)+schedule_interval)
- The scheduler periodically scans the DAG folder (airflow/dags) to inspect tasks and verifies if they can be triggered
or not

######DagRun
- A DAG consists of Tasks and needs those tasks to run
- When the scheduler parses a DAG, it automatically creates a DAGRun which is an instantiation of a DAG in time
according to the start_date and the schedule_interval
- When a DagRun is running all tasks inside it will be executed

######Key Parameters
When you instantiate a DAGRun there are some key parameters to note:
1. start_date = The first date for which you want to have data produced by the DAG in your database (can be set in the 
past)
2. end_date = The date at which your DAG should stop running (usually set to None)
3. retries = The maximum number of retries before the task fails
4. retry_delay = the delay between retries
5. schedule_interval = the interval at which the scheduler will trigger your DAG

|Preset	    |Meaning   	|Cron   	|
|---	    |---	|---	|
|None       |Don't schedule. Manually triggered   	        |   	|
|@once	    |Schedule once and only once   	                |   	|
|@hourly   	|Run once an hour at the beginning of the hour  | 0****  	|
|@daily   	|Run once a day at midnight   	                | 00***  	|
|@weekly   	|Run once a week at midnight on a Sunday morning| 00**0  	|
|@monthly   |Run once a month at midnight of the first day of the month   	| 001**   	|
|@yearly   	|Run once a year at midnight of January 1   	| 0011*  	|

######Important Note
- The scheduler runs your job one schedule interval after the start_date at the end of the period.
i.e. if start date = 2018-01-01 then it will be triggered after 2018-01-01 T 23:59.
It will not be triggered on midnight of 2018-01-01 T 00:00. The DAGRun for 2018-01-01 will be ran after the schedule interval has elapsed.

#####Backfill and Catchup
To avoid having the scheduler backfill your data you have to set `catchup=False`. Otherwise the scheduler will run the tasks for each schedule interval since the start_date. 