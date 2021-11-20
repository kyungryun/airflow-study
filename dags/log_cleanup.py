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

# Airflow System log는 logrotate를 이용해서 관리하는 게 더 효율적
dag_clean = BashOperator(
    task_id='dag_clean',
    bash_command = 'find /경로/ -type f -mtime +30 -name "*.log" -delete',
    dag=dag,
)
dir_clean = BashOperator(
    task_id='dir_clean',
    bash_command = 'find /경로/ -type d -empty -delete',
    dag=dag,
)
dag_clean >> dir_clean
