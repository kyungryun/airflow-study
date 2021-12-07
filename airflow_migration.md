# Airflow 1.10.2 버전 업그레이드 (작성중...)


Airflow 1.10.x 버전의 EOL : 21/06/17


## Airflow 2.X.X (Stable 2.2.0) 2버전에서 달라진 점

DAG Serialization & Fast-Follow 를 도입해서 DAG 파싱 속도를 개선 함

- 반복적인 DAG 파싱 작업을 줄이고 Task Scheduling 과정이 개선 ([astronomer 블로그](https://www.notion.so/Airflow-3624c737c33c4f71a87e26486ca400b7) 에 따르면 10배 이상의 성능 개선이 있었다고 함)
    - 현재도 Task간 lag 가 수초씩 나고 있음, 배치가 늘어난다면 더 체감이 될 것 같음
- Scheduler HA를 지원해서 Scale Out이 가능하도록 지원해줌

Web 서버 사용성 개선

- Dag Serialization을 통해 meta 에서 JSON 형태로 DAG을 읽어와 Web UI에서 더 빠르게 DAG 정보를 불러올 수 있음
    - 현재 Dag 생성 후 웹 UI에 반영이 오래걸리는 문제를 해결할 수 있음
- Auto Refresh 기능이 추가
- UI 변경

Sensor

- Smart Sensor 추가로 효율적인 sensing 작업이 가능
    - 기존 Task당 프로세스를 사용하는 것 보다 효율적으로 sensing 작업이 가능


- PythonSensor 공식 지원

1.10.12 버전에서도 DAG Serialization 제공 (현재는 옵션이 꺼져있음)

Airflow 2 부터는 DAG Serialization 이 기본 제공

현재 운영중인 Airflow는 LocalExecutor로 동작하고 있기 때문에 CeleryExecutor 또는 KubernetesExecutor 을 고려해봄 (kubernetes는 힘들어 보이긴 하는데..)