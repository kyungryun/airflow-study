# Airflow 2.2.2 Install

[Airflow 공식 홈페이지](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) 를 참조하여 2.2.2를 설치해 보자 

(Docker 기반 MAC에서 Docker for Desktop 없이 사용하는 방법은 `minikube.md` 파일에 정리해 둠)

docker-compose.yaml 내려 받기

```sh
$ curl -Lf0 'https://airflow.apache.org/docs/apache-airflow/2.2.2/docker-compose.yaml' 
```
위 docker-compose 에는 `Airflow, postgres, redis, celery, flower` 가 있으며 기본적으로 `CeleryExecutor`로 동작함

`./dags ./logs ./plugins` 폴더 생성

docker 기반으로 동작하기 때문에 airflow container의 볼륨으로 마운트하기 위함

마운트를 하면 airflow task의 로그를 컨테이너에 접근해서 확인하지 않고 해당 폴더에서 확인하거나, 새로운 DAG을 컨테이너에 넣어주지 않고 `./dags` 디렉토리에 넣어주기만 하면 됨

airflow의 uid를 호스트 uid와 맞춰주기 위해 아래 스크립트 입력 airflow 에서 마운트될 폴더에 접근을 못 할 수 있음 (chmod 777 을 통해 폴더 권한을 다 열어주면 접근이 가능하지만 보안에 취약)

```sh
# minikube 환경이라면 호스트의 uid가 아닌 minikube의 uid로 설정을 해줘야 함 (왜 그런지는 아직 모르겠음..)
echo -e "AIRFLOW_UID=$(id -u)" > .env
```



다음으로 airflow 공통 환경을 셋팅해 줌

```sh
$ docker-compose up airflow-init
```

초기화가 끝난다면 아래와 같은 메시지가 확인됨

```
airflow-init_1		   | 2.2.2
airflow_airflow-init_1 exited with code 0
```

`docker ps`를 통해 postgres, redis container 두 개가 정상적으로 떠있는지 확인



이제 아래 명령어를 통해 airflow 서비스를 올림

```shell
# -d 옵션을 통해 detached 모드로 실행
$ docker-compose up -d
```

접속 ip는 `$ minikube ip ` 를 통해 ip를 얻음


# Docker 네트워크 대역 설정

`docker-compose` 로 airflow를 구동시키면 ip대역이 172.xx 로 시작하게 되는데 기존 ip와 충돌이 발생할 수 있다.

이런 경우를 방지하기 위해 airflow network를 설정하여 고정 ip로 컨테이너가 동작하게 설정을 해야한다.

```yaml
# docker-compose.yaml 하단에 아래와 같이 네트워크를 추가해 줌 airflow_net의 네트워크 대역은 192.167.49.0 으로 설정하였는데 원하는 대역으로 설정하면 된다.
networks:
    airflow_net:
      ipam:
        driver: default
        config:
          - subnet: 192.167.49.0/16
```

```yaml
# 이후 각 services 마다 구동할 ip를 설정 후 docker-compose up 으로 컨테이너를 실행한다.
networks:
      airflow_net:
        ipv4_address: 192.167.49.x
```