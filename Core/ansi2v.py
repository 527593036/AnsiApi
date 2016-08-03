#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
Created on 2016年7月14日

@author: zhujin
'''

import json
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.playbook import Playbook
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from callback import AnsiCallBack


class Ansible2Runner(object):
    def __init__(self, ansible_host_list):
        self.ansible_host_list = ansible_host_list
        #self.module_name = module_name
        #self.ansible_patt = ansible_patt
        #self.module_args = ansible_args
        self.Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts', 'listtasks', 'listtags', 'syntax'])
        # connection值'local'指ansible本机，非本机值为smart
        self.options = self.Options(connection='smart',
                                     module_path='/path/to/mymodules', 
                                     forks=100, 
                                     become=True, 
                                     become_method='sudo',
                                     become_user='root', 
                                     check=False,
                                     listhosts=False, 
                                     listtasks=False, 
                                     listtags=False, 
                                     syntax=False
                            )
        self.passwords = dict(vault_pass='secret')
    
    
    def execute(self,module_name,ansible_patt,ansible_args=None):
        loader = DataLoader()
        variable_manager = VariableManager()
        
        inventory = Inventory(
            loader=loader,
            variable_manager=variable_manager,
            host_list=self.ansible_host_list
        )
        
        variable_manager.set_inventory(inventory)
        
        play_source = {}
        if ansible_args:
            play_source = {
                'name': "AnsiApi Play",
                'hosts': ansible_patt,
                'gather_facts': 'no',
                'tasks': [{
                    'action': {
                        'module': module_name,
                        'args': ansible_args
                    }
                }]
            }
        else:
            play_source = {
                'name': "AnsiApi Play",
                'hosts': ansible_patt,
                'gather_facts': 'no',
                'tasks': [{
                    'action': {
                        'module': module_name
                    }
                }]
            }
        
        play = Play.load(
            play_source,
            variable_manager=variable_manager,
            loader=loader
        )
        
        task_queue_manager = None
        callback = AnsiCallBack()
        
        try:
            task_queue_manager = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=self.options,
                passwords=self.passwords,
                stdout_callback=callback
            )
            task_queue_manager.run(play)
        finally:
            if task_queue_manager is not None:
                task_queue_manager.cleanup()
                
        return self.evaluate_results(callback)
        
    def playbook_api(self,yml_fp):
        loader = DataLoader()
        variable_manager = VariableManager()
        
        inventory = Inventory(
            loader=loader,
            variable_manager=variable_manager,
            host_list=self.ansible_host_list
        )
        
        variable_manager.set_inventory(inventory)
        
        playbooks = ["%s" % yml_fp]
        
        pbex = PlaybookExecutor(
                      playbooks=playbooks,
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      options=self.options,
                      passwords=self.passwords
                )
                      
        callback = AnsiCallBack()
        pbex._tqm._stdout_callback = callback
        pbex.run()
        
        return self.evaluate_results(callback)
        
    
    def evaluate_results(self, callback):
        ret = {}
        ret['dark'] = {}
        ret['contacted'] = {}
        for server, result in callback.unreachable.items():
            ret['dark'][server] = result
            
        for server, answer in callback.contacted.items():
            ret['contacted'][server] = answer['result']
            
        return ret
