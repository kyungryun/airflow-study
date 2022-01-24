## 잡다한 서버 설정 팁 정리 (현재 airflow 관련 설정만 보고있는데 추후 레포를 하나 파야할듯)


#### ssh-key 여러개 등록하기
[ssh_name] 라는 filename 으로 새로운 ssh key 생성 (RSA)

```bash
ssh-keygen -t rsa -f [ssh_name]
```

[ssh_name] (publick key)를 사용하고자 하는 서비스에 등록

$HOME/.ssh/config에 Host 등록

```bash
Host [host_url]
	User git
	Hostname [host_url]
	PreferredAuthentications publickey
	IdentityFile ~/.ssh/[ssh_name]
```
