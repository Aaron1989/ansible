#!/usr/bin/expect -f

if { $argc != 2 } {
    puts "Usage: $argv0 <host> <passwd>"
    exit 1
}

spawn ssh-copy-id -i /root/.ssh/id_rsa.pub [lindex $argv 0]
 
set timeout 3
set password [lindex $argv 1]

expect {
"(yes/no)?" { send "yes\r"; exp_continue}
"password:" { send "$password\r" }
}

log_file in_ssh.log
#expect "(yes/no?)"
#send "yes\r"
 
#expect "password:"
#send "$password\r"
 
expect eof
