from datetime import timedelta, datetime
from os import path


def yesterday():
    now = datetime.now()
    return datetime(now.year, now.month, now.day) - timedelta(days=1)


def dag_id(file):
    if file is None:
        raise ValueError("file parameter must be passed")
    if "/dags/" in file:
        dag_id = file.split("/dags/")[1].replace("/", "_").replace(".py", "")
    else:
        dag_id = file.replace("/", "_").replace(".py", "")

    return dag_id
