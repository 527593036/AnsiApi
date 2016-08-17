# -*-coding: utf-8-*-
'''
Created on 2016年8月12日

@author: zhujin
'''


from jinja2 import Template, Environment, FileSystemLoader

import os
PATH = os.path.split(os.path.realpath(__file__))[0]

import sys
sys.path.append(PATH+'/../')
from config import DBCONF
from Comm.db import MySQL


class NginxUpsConf(object):
    def get_tmeplate(self,tmpfp):
        j2_env = Environment(loader=FileSystemLoader(os.path.join(PATH, 'templates')))
        return j2_env.get_template(tmpfp)
        
    def create_config(self,services):
        config = self.get_tmeplate('upstreams.conf.jinja2').render(service_groups=self.group_services(services))

        if config is None:
            raise NginxException('生成配置，但配置为空，请检查!!')
            
        return config
        
    def update_config(self,config, path):
        with open(path, 'wb') as result:
            result.write(config.encode())
        
    def group_services(self,services):
        group_services = {'http': []}
        db = MySQL(DBCONF)
        for service in services:
            upstream_service_sql = "select service_name,ip,port from upstream_services where service_name='%s'" % service
            ret = db.query(upstream_service_sql)
            service_instance = []
            for row in ret:
                service_instance.append({'instance':{'Address':row[1],'ServicePort':row[2]}})
            group_services['http'].append({service:service_instance})
                
        return group_services
        

# todo
#class NginxVhostsConf(object):
        

if __name__ == '__main__':
    ups_obj = NginxUpsConf()
    services = ['test','test1']
    print ups_obj.group_services(services)
    ups_conf = ups_obj.create_config(services)
    print ups_conf
    ups_obj.update_config(ups_conf,PATH+'/conf/upstream_test_test1.conf')
    
    
                
            
            
            
        
        


