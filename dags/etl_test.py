import os
import sys
from functools import partial
sys.path.append(os.environ['AIRFLOW_HOME'])

from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from datetime import datetime
import lib.util as util
from lib.slack import SlackAlert
import random
import pymysql


# 앞단 작업 실패시 뒷단 실행 안되게
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 3, 20),
    'wait_for_downstream': True
}

dag = DAG('etl_dag',
          default_args=default_args,
          schedule_interval='*/2 * * * *',
          catchup=False
          )
conn = pymysql.connect(host='localhost', user='airflow', password='airflow', db='airflow', charset='utf8')


def select_data(**kwargs):
    cursor = conn.cursor()

    select_sql = "select max(random_number) from airflow_test"
    cursor.execute(select_sql)

    now = datetime.now()
    nowDatetime = now.strftime('%Y-%m-%d %H:%M')
    f = open("dir" + str(nowDatetime) + ".txt", 'w')
    for data in cursor.fetchall():
        f.write(str(data[0]))
    f.close()
    conn.commit()
    conn.close()
    return 'CreateFile'


def insert_data(**kwargs):
    cursor = conn.cursor()

    insert_sql = "insert into airflow_test values (%s, now())"
    cursor.execute(insert_sql, random.randint(1, 100))
    conn.commit()
    conn.close()
    return 'Insert Data'


insert_task = PythonOperator(
    task_id='insert_task',
    python_callable=insert_data,
    provide_context=True,
    dag=dag
)
select_task = PythonOperator(
    task_id='select_task',
    python_callable=select_data,
    provide_context=True,
    dag=dag
)

insert_task >> select_task
