#!/usr/bin/env python
import os
import sys
import re
import socket
import difflib
import json
import math
reload(sys)
sys.setdefaultencoding( "utf-8" )
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupsRequest
from aliyunsdkecs.request.v20140526 import DescribeInstanceStatusRequest
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest

def ChkScecuGp():
    print '#'*10+"Staring Check The ECS Security Group"+'#'*10

    request=DescribeSecurityGroupsRequest.DescribeSecurityGroupsRequest()
    request.set_accept_format('json')
    request.set_action_name('DescribeSecurityGroups')
    request.set_query_params(dict(Action='DescribeSecurityGroups'))
    result = clt.do_action(request)
    result_dict=json.loads(result)  #result_dict is dict; loop with another dict with key "SecurityGroups"
    # print type(result_dict['SecurityGroups']) #check the result_dict['SecurityGroups'] type
    # for key in result_dict['SecurityGroups']:
    #     print key
    #     print result_dict['SecurityGroups'][key]
    securgp=result_dict['SecurityGroups']['SecurityGroup'] #result_dict['SecurityGroup']['SecurityGroup'] is a value in dict
                                                               #this is a list, including info we need
    securgpfile=open('securgp.txt','w')
    for i in securgp:
        print i['SecurityGroupId'].encode('utf-8').ljust(20),
        print str(i['CreationTime']).ljust(30),
        print i['SecurityGroupName']
        securlist=i['SecurityGroupId'].encode('utf-8')+'\t'+i['CreationTime'].encode('utf-8')+'\t'+i['SecurityGroupName'].encode('utf-8')+'\n'
        securgpfile.write(securlist)
    securgpfile.close()
    print '#'*10+'Check ECS Security Group Finished'+'#'*10

def GetPags():
    # the function used for get the total number of ECS

    request=DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    request.set_accept_format('json')
    request.set_action_name('DescribeInstanceStatus')
    request.set_query_params(dict(Action='DescribeInstanceStatus',PageSize=1))
    result = clt.do_action(request)
    result_dict=json.loads(result)
    total_ecs=result_dict['TotalCount']
    # print total_ecs
    # print type(total_ecs)
    return total_ecs


def ChkEcsStatus():
    print '#'*10+"Staring Check The ECS Status Attribute"+'#'*10
    total_ecs=GetPags()
    # print type(total_ecs)
    kep_file='ecsstat.txt'
    ecsstatfile=open( kep_file,'w')
    ecsstatfile.truncate()
    pgsize=20
    pags_ecs=int(math.ceil(int(total_ecs)/pgsize))+2  #the whole list will split into $pags_ecs
    print "The Process Will Split into:\t",total_ecs

    request=DescribeInstanceStatusRequest.DescribeInstanceStatusRequest()
    request.set_accept_format('json')
    request.set_action_name('DescribeInstanceStatus')
    for i in range(1,pags_ecs):
        request.set_query_params(dict(Action='DescribeInstanceStatus',PageNumber=i,PageSize=pgsize))
        result = clt.do_action(request)
        result_dict=json.loads(result)  #result_dict is dict; loop with another dict with key "SecurityGroups"
        # print type(result_dict['SecurityGroups']) #check the result_dict['SecurityGroups'] type
        # for key in result_dict['SecurityGroups']:
        #     print key
        #     print result_dict['SecurityGroups'][key]
        print "The total ECS number:\t",result_dict['TotalCount']
        print "Current Page:\t",result_dict['PageNumber']
        print "The Page Size:\t",result_dict['PageSize']
        #ecslist=result_dict['InstanceStatus']   #result_dict['SecurityGroup']['SecurityGroup'] is a value in dict
                                                              #this is a list, including info we need
        install=result_dict['InstanceStatuses']            #it's a dict for all the ecs name and status list
        instlist=install['InstanceStatus']                 #it's a list, for ecs status and name
        ecsstatfile=open(kep_file,'a')
    # print type(instlist)  # the instlist type is list
        for j in instlist:
            print str(j)[1:-1].replace("u'","'")
            ecsstatfile.write(str(j).replace("u'","'")[1:-1]+'\n')
            #ecsstatfile.write(str(j).encode('utf-8')[1:-1]+'\n')
    ecsstatfile.close()
    print '#'*10+'Check ECS Status Finished'+'#'*10

def GetEcsInfo():
     print '#'*10+"Staring Check The ECS Info"+'#'*10
     total_ecs=GetPags()
     kep_file='ecslist.txt'
     ecslist=open( kep_file,'w')
     ecslist.truncate()
     pgsize=20
     pags_ecs=int(math.ceil(int(total_ecs)/pgsize))+2  #the whole list will split into $pags_ecs
     print "The Process Will Split into:\t",pags_ecs

     request=DescribeInstancesRequest.DescribeInstancesRequest()
     request.set_accept_format('json')
     request.set_action_name('DescribeInstances')
     ecslistfile=open( kep_file,'a')

     print 'Hostname'.ljust(17)+'InstanceId'.ljust(18)+'SecurityGp'.ljust(35) \
             +"InterIP".ljust(22)+'PubIp'.ljust(20)+'Status'.ljust(11)+'InstanceName'

     for i in range(1,pags_ecs):
         request.set_query_params(dict(Action='DescribeInstances',PageNumber=i,Pagesize=pgsize))
         result = clt.do_action(request)
         result_dict=dict(json.loads(result))
         ins_info=result_dict['Instances']['Instance']            #get the ecs detailed info
         #print ins_info
         #print type(ins_info)

         for j in range(len(ins_info)):
            hostname=str(ins_info[j]['HostName'])
            insid=str(ins_info[j]['InstanceId'])
            securgp=str(ins_info[j]['SecurityGroupIds']['SecurityGroupId']).replace("u'","'")[1:-1]
            interip=str(ins_info[j]['InnerIpAddress']['IpAddress']).replace("u'","'")[1:-1]
            pubip=str(ins_info[j]['PublicIpAddress']['IpAddress']).replace("u'","'")[1:-1]
            insname=ins_info[j]['InstanceName']
            stats=ins_info[j]['Status']

            print hostname.ljust(16), \
            insid.ljust(16), \
            securgp.ljust(35), \
            interip.ljust(20), \
            pubip.ljust(20), \
            stats.ljust(10), \
            insname

            # a1=len(ins_info[j]['SecurityGroupIds']['SecurityGroupId'])   #transfer from list to charv don't need
            # b1=ins_info[j]['SecurityGroupIds']['SecurityGroupId']
            # if a1>0:
            #     for i in range(a1):
            #         print b1[i],
            # a2=len(ins_info[j]['InnerIpAddress']['IpAddress'])
            # b2=ins_info[j]['InnerIpAddress']['IpAddress']
            # if a2>0:
            #     for i in range(a2):
            #         print b2[i],
            # print ins_info[j]['InstanceName']

            ecslistfile.write(hostname+'\t'+insid+'\t'+securgp+'\t'+interip+'\t'+pubip+'\t'+insname+'\n')
     ecslistfile.close()

     print '#'*10+'Get ECS List Finished'+'#'*10

def GetProdList():
    print '#'*10+"Staring Get The Prod ECS List"+'#'*10
    total_ecs=GetPags()
    SgId='sg-28uhkoxkx' #for RPOD and STAGING
    # SgId='sg-28m5jr0vu' #for TESTING
    # SgId='sg-286emv3od' #for DEV
    kep_file='prodecslist.txt'
    ecslist=open( kep_file,'w')
    ecslist.truncate()
    pgsize=20
    pags_ecs=int(math.ceil(int(total_ecs)/pgsize))+2  #the whole list will split into $pags_ecs

    request=DescribeInstancesRequest.DescribeInstancesRequest()
    request.set_accept_format('json')
    request.set_action_name('DescribeInstances')
    ecslistfile=open( kep_file,'a')

    print "The Process Will Split into: %d with total: %d" % (pags_ecs,total_ecs)
    # print "InterIP".ljust(20)+'InstanceName'

    for i in range(1,pags_ecs):
        request.set_query_params(dict(Action='DescribeInstances',SecurityGroupId=SgId,PageNumber=i,Pagesize=pgsize))
        result = clt.do_action(request)
        result_dict=dict(json.loads(result))
        ins_info=result_dict['Instances']['Instance']            #get the ecs detailed info

        for j in range(len(ins_info)):
            interip=str(ins_info[j]['InnerIpAddress']['IpAddress']).replace("u'","'")[1:-1]
            insname=ins_info[j]['InstanceName']

            print interip.ljust(20), insname
            ecslistfile.write(interip+'\t'+insname+'\n')
    ecslistfile.close()

    print '#'*10+'Get Prod ECS List Finished'+'#'*10

def CompList(filename1,filename2,splitregex = '\t'):
    a1=set([])
    a2=set([])
    c1=set([])
    with open(filename1, 'rt') as handle1:
        for ln1 in handle1:
            # items = re.split(splitregex, ln1)
            items=re.split(splitregex,ln1)[0].split(',')[0]
            # yield items[0], items[1]
            # a1.append(items[0])
            a1.add(items[1:-1])
        # b1=set(sorted(a1,key = lambda x: (x.split('.')[0],x.split('.')[1],x.split('.')[2],x.split('.')[3])))
        print "the list from ecs"
        # print type(a1)
        print a1
        print len(a1)
        print ""

    with open(filename2,'rt') as handle2:
        for ln2 in handle2:
            if re.match('^prod-\S+',ln2):
            # if re.match('^dev-\S+',ln2):
            # if re.match('^testing-\S+',ln2):
                items=re.split(splitregex,ln2)[1].split('=')
                # a2.append(items[1])
                a2.add(items[1])
        # b2=set(sorted(a2,key = lambda x: (x.split('.')[0],x.split('.')[1],x.split('.')[2],x.split('.')[3])))
        print "the list from hosts"
        # print type(a2)
        print a2
        print len(a2)
        print ""

    c1=a1-a2
    print "the hosts haven't add in the hosts"
    print len(c1)
    # print type(c1)
    # print list(c1)
    for i in list(c1):
        print i

# comm out for list all security groups
# ChkScecuGp()

# comm out for list pages count, it's comm func
# GetPags()

# comm out for all ecs status check, it will run "GetPags()" and gen a file 4 keep as named "ecsstat.txt"
# ChkEcsStatus()

# comm out for get all ecs , it will run "GetPags()" and  gen a file 4 keep host list as naned "ecslist.txt"
# GetEcsInfo()

# comm out for get all prod ecs list as default , it will run "GetPags()" and  gen a file 4 keep host list as naned "prodecslist.txt"
# if you want to run for other env, do memeber change the security group parameter : SgId='sg-28uhkoxkx'
# GetProdList()

# comm out for hosts need to config, host.txt comes from ansible hosts need add manually, it will run "GetProdList()", the default for prod
# CompList("prodecslist.txt","host.txt",splitregex='\s+')