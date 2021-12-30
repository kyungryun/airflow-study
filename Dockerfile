FROM python:3.8-slim-buster

ARG AIRFLOW_VERSION=2.2.2
ARG AIRFLOW_USER_HOME=/airflow
ARG HOME=/home
ENV AIRFLOW_HOME=${AIRFLOW_USER_HOME}

RUN apt-get update && apt-get install -y gcc \
    g++ \
    vim \
    procps \
    netcat \
    libpq-dev \
    libsasl2-dev \
    ssh

RUN pip install --upgrade pip setuptools wheel
RUN pip install paramiko==1.18.5
RUN pip install numpy
RUN pip install Cython
RUN pip install pendulum
RUN pip install celery
RUN pip install flower
RUN pip install redis
RUN pip install sasl
RUN pip install thrift_sasl
RUN pip install --no-use-pep517 pandas
RUN pip install --no-use-pep517 apache-airflow[hive,druid,slack,postgres,celery,ssh,oracle]==2.1.0
RUN pip install psycopg2
RUN mkdir airflow

COPY ./script/entrypoint.sh /entrypoint.sh

WORKDIR ${AIRFLOW_USER_HOME}


ENTRYPOINT ["bash", "/entrypoint.sh"]
