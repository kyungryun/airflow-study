kill -9 `ps -ef|grep airflow|grep -v grep|grep -v tail|awk '{print $2}'`
echo "Airflow Stopped"