#!/bin/sh

source /etc/profile
source /root/.bash_profile

pptpd_pro=`ps -ef |grep "pptpd updetach" |grep -v grep |wc -l`
ping_pro=`ps -ef |grep "ping www.baidu.com"|grep -v grep |wc -l`
num=1
#echo $pptpd_pro
#echo $ping_pro

if [ $pptpd_pro -ne $num ] || [ $ping_pro -ne $num ]
then
  for pid in $(ps -ef|grep 'pptpd\|nolaunchpppd\|www.baidu.com'|grep -v grep|cut -c 10-15);
  do
#    echo $pid;
    kill -9 $pid;
  done

  sleep 5

  /opt/pptp_agent/./start_pptpd.sh > mon.log 2>&1
  
  exit 0
fi
