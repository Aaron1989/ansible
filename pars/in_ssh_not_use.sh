#!/bin/sh
# \
exec expect -f "$0" "$@"
if { $argc != 2 } {
    puts "Usage: $argv0 <host> <passwd>"
    exit 1
}
set timeout 10
set password [lindex $argv 1]
spawn ssh-copy-id -i /root/.ssh/id_rsa.pub [lindex $argv 0]
expect "(yes/no)?"
send "yes\r"
expect "password:"
send "$password\r"
expect eof
