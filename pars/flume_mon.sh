#!/bin/bash
#获取当前flume进程数目
flume_process=`ps -ef|grep "/usr/local/flume/conf/flume-conf" |grep -v grep|cut -c 10-15|wc -l`
num=1
#echo $flume_process
# 如果进程数目不等于1，则杀掉相关进程并重新启动
if [ $flume_process -ne $num ]
then
  for pid in $(ps -ef|grep "/usr/local/flume/conf/flume-conf"|grep -v grep|cut -c 10-15);
  do
    echo $pid
    kill -9 $pid
  done

  sleep 5
  /usr/local/flume/bin/start_flume.sh > ../flume_start.log 2>&1
  exit 0
fi
