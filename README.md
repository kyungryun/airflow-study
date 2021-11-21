



### Conda env 환경에서 테스트

환경 생성 및 에어플로우 설치

```bash
1. conda create -n airflow_ex python=3.8
2. conda activate airflow_ex or source activate airflow_ex
3. conda install -y -c conda-forge airflow
# conda-forge 를 이용할 경우 airflow 2.0.1 버전이 설치됨
# 2.0 이상 버전 설치를 추천 (이전 버전 서포트 중지 예정)
# 이전 버전 설치를 하려면 pip 를 이용해서 설치 
pip install apache-airflow==1.10.12 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-1.10.12/constraints-3.8.txt"
```

에어플로우 설정

```bash
# airflow 버전 확인
airflow version

# mysql or mariadb 사용시 관련 패키지 설치
pip3 install 'apache-airflow[mysql]'

# brew를 통해 설치한 mariadb 서버 실행
brew services start mariadb

# db 초기화
airflow db init # 2버전 이상
airflow initdb # 2버전 이하

# Global variable explicit_defaults_for_timestamp needs to be on (1) for mysql 에러 발생시
mysql 설정 변경

# sql 쿼리를 통해 변경
SET GLOBAL explicit_defaults_for_timestame = 1 or ON (mariadb)
# Variable 'explicit_defaults_for_timestamp' is a read only variable 해당 에러가 난다면

# my.cnf 파일 수정 // brew를 통해 설치했을 경우 /etc/bin/ 아래에 파일이 있음 파일을 열고
# [mysqld] 아래 내용 추가 후 db 재시작
explicit_defaults_for_timestamp = 1 or ON (mariadb)

# airflow db init 시 아래와 같은 에러가 뜨는 경우 (mariadb 에서 발생하는듯)
Specified key was too long; max key length is 3072 bytes

# my.cnf 파일의 [mysqld] 아래에 옵션 추가
innodb_file_format = barracuda
innodb_large_prefix = on


```

Log 설정
- find delete 를 통해 dag 로그 삭제
- logrotate 를 통해 Airflow 시스템 로그 삭제

Todo
- docker compose 로 설정해보기
```
$git clone https://github.com/puckel/docker-airflow
$cd docker-airflow

$docker pull puckel/docker-airflow

$docker-compose -f docker-compose-LocalExecutor.yml up -d
$docker ps
```
- git sync sidecar 테스트
- airflow 2.0 테스트
- smart sensor 테스트
- custom sensor 개발 해보기
- loop 사용방법? , operator in function
- flower redis 이용한 병렬 워커 테스트
