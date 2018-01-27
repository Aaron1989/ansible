#!/bin/sh

source /etc/profile
source /root/.bash_profile

pptpsetup --create pptpd --server {{ pptp_server }} --username {{ con_user }} --password {{ con_pass }} --start
route add -net <IP> dev ppp0
nohup ping www.baidu.com -i 20 &
