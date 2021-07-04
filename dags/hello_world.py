 




from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator


def print_hello():
    return 'Hello world!'


dag = DAG('hello_world',
          description='Simple tutorial DAG',
          schedule_interval='0/1 * * * *',
          start_date=datetime(2021, 2, 1),
          catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries=3, dag=dag)

date_operator = BashOperator(task_id='date_task', bash_command='date', dag=dag)

hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

dummy_operator >> date_operator >> hello_operator
