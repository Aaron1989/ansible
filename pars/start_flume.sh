#!/bin/bash

nohup /usr/local/flume/bin/flume-ng agent -n agent1 -c /usr/local/flume/conf/ -f /usr/local/flume/conf/flume-conf -Dflume.monitoring.type=http -Dflume.monitoring.port=41414 &
