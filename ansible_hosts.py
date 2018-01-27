#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Ansible_Host:
    def __init__(self,env,host='',user='',passwd='',port=''):
        self.__host = host
        self.__user = user
        self.__password = passwd
        self.__port = port
        self.env = env
        self.__results = self.ConnectMysql()

    def ConnectMysql(self):
        try:
            #连接数据库
            conn = MySQLdb.connect(host=self.__host,user=self.__user,passwd=self.__password,port=int(self.__port),charset='utf8')
            cur = conn.cursor()

            #连接库并操作
            conn.select_db('ops_asset')
            count = cur.execute('select * from ecs_instance')
            results = cur.fetchmany(count)

            #连接ecs_group库,得到对应的id和组名,生成一个新字典dict1
            count = cur.execute('select * from ecs_group')
            groups = cur.fetchmany(count)
            groupName = []
            id = []
            for i in groups:
                if str(list(i)[1]).startswith(self.env):
                    groupName.append(str(list(i)[1]))
                    id.append(str(list(i)[0]))
                else:
                    pass
            dict1 = dict(zip(id,groupName))
            self.dict1 = dict1
            self.groupName = groupName
            cur.close()
            conn.close()
            return results
        except MySQLdb.Error as e:
            print(e)

    def CreateHost(self):
            #写文件hosts
            with open('hosts','wb') as file:
                file.writelines('#'*45+'\n')
                file.writelines('#'+'\n')
                file.writelines('#The configuration is ' +self.env + ' environment here\n')
                file.writelines('#'+'\n')
                file.writelines('#'*45+'\n')
                file.writelines('[' +self.env +':children]\n')
                for i in self.groupName:
                    file.writelines(i+'\n')
                file.writelines('\n')
                for i in self.groupName:
                    file.writelines('\n')
                    file.writelines('[' +i + ']'+'\n')
                    for k,v in self.dict1.items():
                        if i == v:
                            for r in self.__results:
                                if str(list(r)[10]) == k:
                                    file.writelines(str(list(r)[1]).ljust(23) + 'ansible_ssh_host=' + str(list(r)[6]).ljust(20) +('#' + str(list(r)[8]).encode('UTF-8')).ljust(25))
                                    file.writelines('\n')
                                else:
                                    continue
                        else:
                            continue
            file.close()



if __name__== '__main__':
    task = Ansible_Host(env='dev')
    task.ConnectMysql()
    task.CreateHost()
