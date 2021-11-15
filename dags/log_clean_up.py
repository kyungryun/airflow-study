import os
import sys

sys.path.append(os.environ['AIRFLOW_HOME'])

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
import lib.util as util

dag_id = util.dag_id(__file__)

default_args = {
        'owner': 'admin',
        'depends_on_past': 'False',
        'start_date': datetime(2021, 7, 1),
        'provide_context': True
        }

dag = DAG(
        dag_id,
        default_args=default_args,
        catchup=False,
        schedule_interval='40 0 * * *',
        )

bash_command = 'find /경로/ -type f -mtime +30 -name "*.log" -delete'

log_clean_up = BashOperator(
    task_id='log_clean_up',
    bash_command = bash_command,
    dag=dag,
)

log_clean_up
