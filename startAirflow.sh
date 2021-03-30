# airflow 프로세스 종료
kill -9 `ps -ef|grep airflow|grep -v grep|grep -v tail|awk '{print $2}'`

# scheduler 실행 Log파일은 logs/scheduler 저장
nohup airflow scheduler > $AIRFLOW_HOME/logs/scheduler/airflow-scheduler.log 2>&1 &
echo "Airflopw Scheduler Start!!!"
# webserver 실행 Log파일은 logs/webserver 저장
nohup airflow webserver -p 8080 > $AIRFLOW_HOME/logs/webserver/airflow-webserver.log 2>&1 &
echo "Airflopw Webserver Start!!!"