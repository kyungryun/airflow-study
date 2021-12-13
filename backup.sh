#!/bin/bash

# 인자가 하나라도 null이라면
if [ -z $1 ] || [ -z $2 ] 
then
	# 사용법 출력
    echo usage: $0 source_dir target_dir
else
    SRCDIR=$1
    DSTDIR=$2
    # date 명령을 통해 Filename 정의
    # 반드시 $(date(공백)+%...)
    filename=backup.$(date +%y%m%d%H%M%S).tar.gz

	# 디렉토리가 존재한다면 mkdir 수행 X
    if [ -d $DSTDIR ]
    then    
        tar -cvzf $DSTDIR/$filename $SRCDIR
    else
        mkdir $DSTDIR
        tar -xvzf $DSTDIR/$filename $SRCDIR
    fi
fi
