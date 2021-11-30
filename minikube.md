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

Docker CLI에서 설치한 `minikube` 를 사용할 수 있도록 설정

```sh
$ eval $(minikube docker-env)
```

`docker ps `로 Kubernetes 관련 컨테이너가 나오면 성공
