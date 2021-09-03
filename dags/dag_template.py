import os
import sys
from functools import partial
sys.path.append(os.environ['AIRFLOW_HOME'])

import cx_Oracle
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.sql_sensor import SqlSensor
from datetime import datetime


dsn_tns = cx_Oracle.makedsn(, , )

default_args = {
        'owner': '',
        'depends_on_past': False,
        'start_date': datetime(2021, 7, 1),
        'provide_context': True
        }

dag = DAG(
        '',
        default_args=default_args,
        catchup=False,
        schedule_interval='* * * * *', # cron
        )

base_dt = "{{ dag.timezone.convert(execution_date).strftime('%Y%m%d%H%M%S')}}"

# 5분마다 체크
wait_interval = 60 * 5
# 1시간 동안 기다리면 에러 발생
wait_timeout = 60*60

# PythonOperator 에서 호출할 함수 작성
def python_operator(base_dt, **kwargs):
    conn = cx_Oracle.connect(user=, password=, dsn=dsn_tns, encoding='utf-8')
    sql = ''' 
        쿼리 작성
    '''
    cur = conn.cursor()
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

"""
SqlSensor 템플릿
sql 쿼리를 넣으면 wait_interval 주기 마다 쿼리를 실행시켜 결과가 있으면 다음 태스크 실행
wait_timeout 동안 결과가 없다면 에러 출력
"""    
sql_sensor_template = SqlSensor(
    task_id = 'sql_sensor_template',
    conn_id=,
    sql="""
    """,
    poke_interval=wait_interval,
    timeout=wait_timeout,
    dag=dag
)

"""
PythonOperator 템플릿
python_callable 에 작성한 파이썬 함수명을 추가함
파라미터를 넘길땐 op_kwargs 에 key : value 형태로 추가하여 넘겨줄 수 있음
"""
python_operator_template = PythonOperator(
    task_id='python_operator_template',
    python_callable=python_operator,
    op_kwargs={'base_dt': base_dt,},
    provide_context=True,
    dag=dag,
)


sql_sensor_template >> python_operator_template
