#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
Created on 2016年5月20日

@author: zhujin
'''

from ansible.runner import Runner
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils


class Ansible1Runner(object):
    def __init__(self,ansible_host_list):
        self.ansible_host_list = ansible_host_list
        
    def execute(self, ansible_mod, ansible_patt, ansible_args=None):
        ret = None
        
        if ansible_args:
            runner_obj = Runner(
                    module_name=ansible_mod,
                    module_args=ansible_args,
                    host_list=self.ansible_host_list,
                    pattern=ansible_patt,
                    become=True,
                    become_user='root',
                )
        else:
            runner_obj = Runner(
                    module_name=ansible_mod,
                    host_list=self.ansible_host_list,
                    pattern=ansible_patt,
                    become=True,
                    become_user='root',
                )
        
        ret = runner_obj.run()
        
    def playbook_api(self,yml_fp):
        ret = None
        
        stats = callbacks.AggregateStats()
        playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
        
        pb = PlayBook(
            playbook=yml_fp,
            host_list=self.ansible_host_list,
            stats=stats,
            callbacks=playbook_cb,
            runner_callbacks=runner_cb
        )
    
        ret = pb.run()
        
    