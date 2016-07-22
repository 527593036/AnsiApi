#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
Created on 2016年5月20日

@author: zhujin
'''

import os
import json
import ansible

PATH = os.path.split(os.path.realpath(__file__))[0]

ANSIBLE_VERSION = int(ansible.__version__.split('.')[0])

if ANSIBLE_VERSION < 2:
    from ansi1v import Ansible1Runner as AnsiRun
elif ANSIBLE_VERSION >= 2:
    from ansi2v import Ansible2Runner as AnsiRun
    
    
class AnsibleApi(object):
    def __init__(self, ansible_host_list):
        self.ansible_host_list = ansible_host_list
        
    def remote_execute(self, ansible_mod, ansible_patt, ansible_args=None):
        ret = None
        
        runner_obj = AnsiRun(self.ansible_host_list)
        ret = runner_obj.execute(ansible_mod, ansible_patt, ansible_args)
        
        return json.dumps(ret,indent=4)
    
    def shell_remote_execute(self, ansible_patt, ansible_args):
        mod = "shell"
        ret = self.remote_execute(mod, ansible_patt, ansible_args)
        return ret
    
    def remote_ping(self, ansible_patt):
        mod = "ping"
        ret = self.remote_execute(mod, ansible_patt)
        return ret
    
    def remote_setup(self, ansible_patt):
        mod = "setup"
        ret = self.remote_execute(mod, ansible_patt)
        return ret
    
    def fetch_remote_file(self, ansible_patt, src_file, dest_dir):
        mod = "fetch"
        ansible_args = "src=%s dest=%s" % (src_file, dest_dir)
        ret = self.remote_execute(mod, ansible_patt, ansible_args)
        return ret
    
    def playbook_api(self, yml_fp):
        ret = None
        runner_obj = AnsiRun(self.ansible_host_list)
        ret = runner_obj.playbook_api(yml_fp)
            
        return json.dumps(ret,indent=4)

if __name__ == '__main__':
    run_obj = AnsibleApi(PATH + "/../hosts/inentory.sh")
    ret_shell = run_obj.shell_remote_execute('192.168.33.11,192.168.33.12,192.168.33.10', 'uname -a')
    print ret_shell
    # ret_ping = run_obj.remote_ping('all')
    # print ret_ping
    # ret_setup = run_obj.remote_setup('192.168.33.12')
    # print ret_setup
    ret_playbook = run_obj.playbook_api(PATH + "/../hosts/test.yml")
    print ret_playbook
    #ret_fetch_file = run_obj.fetch_remote_file('192.168.33.11,192.168.33.12', '/home/zhujin/db.sqlite3', 'logs/')
    #print ret_fetch_file
    
