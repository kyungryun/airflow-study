## minikube 설치하기

Virtualbox 설치

`docker-cli` , `docker-compose`, `minikube`, `docker-credential-helper`, `helm(airflow helm chart 를 사용하기 위함)`  를 설치

(Docker desktop은 편리하게 설치가 가능하나 유료화 이슈가 있음)

```sh
$ brew install docker
$ brew install docker-compose
$ brew install minikube
$ brew install docker-credential-helper
$ brew install helm
$ minikube start --driver=virtualbox
```

`minikube` 클러스터를 생성함, 드라이버 기본값이 `docker` 이기 때문에 `virtualbox` 옵션을 명시해서 설치

```sh
$ minikube start --driver=virtualbox
😄  Darwin 11.6 의 minikube v1.24.0
✨  기존 프로필에 기반하여 virtualbox 드라이버를 사용하는 중
👍  minikube 클러스터의 minikube 컨트롤 플레인 노드를 시작하는 중
🤷  virtualbox "minikube" VM is missing, will recreate.
🔥  virtualbox VM (CPUs=2, Memory=4000MB, Disk=20000MB) 를 생성하는 중 ...
🐳  쿠버네티스 v1.22.3 을 Docker 20.10.8 런타임으로 설치하는 중
```

minikube 기본 driver을 `virtualbox`로 설정

클러스터의 셋팅을 변경해줄 수 있음 (설정 후 minikube 재시작 필요)

```Sh
# 기본 driver 설정
$ minikube config set driver virtualbox

# minikube 셋팅 변경
$ minikube config set memory 8192
$ minikube config set cpu 2
$ minikube config set disk-size 20000mb

# minikube 현재 셋팅 확인
$ minikube config get memory

# 전체 확인
$ minikube config view vm-driver

```



Docker CLI에서 설치한 `minikube` 를 사용할 수 있도록 설정

```sh
$ eval $(minikube docker-env)

새로운 터미널 세션에서 자동으로 Docker 환경을 사용할 수 있게 하고 싶다면 .bash_profile 파일에 추가

minikube status > /dev/null && eval $(minikube docker-env)
```

`docker ps `로 Kubernetes 관련 컨테이너가 나오면 성공

### Airflow는 Docker로 테스트를 하자.. k8s 까지 하기엔 기반지식이 부족하기도 하고 오버엔지니어링인듯

#### docker는 위 셋팅한 minikube를 이용해서 사용하자



Docker-compose 사용시 `docker-credential-desktop not installed or not available in PATH` 에러가 나온다면

`~/.docker/config.json` 파일 수정 `credsStore -> credStore`





## 

