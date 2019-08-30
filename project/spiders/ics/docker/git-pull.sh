#!/bin/bash

#刷新环境变量
source /etc/profile

#专门用来部署的帐号（因为gitlab不支持ssh的密钥部署方式）: ktgg_deployer JL.8Uba2pw，在生产环境中用这个帐号git pull一次让容器记住帐号密码，然后把git-pull.sh加入cron中就能自动更新了
# * * * * * /bin/bash /app/docker/git-pull.sh

#进入本目录
cd `dirname $0`

date >> git-pull.log

step=5 #间隔的秒数，不能大于60
for (( i = 0; i < 60; i=(i+step) )); do
    git pull  --ff-only >> git-pull.log 2>> git-pull_error.log
    sleep $step
done