#!/usr/bin/env python
# -*-coding: utf-8-*-
'''
Created on 2016年5月20日

@author: zhujin
'''

import os
import ansible

PATH = os.path.split(os.path.realpath(__file__))[0]

ANSIBLE_VERSION = int(ansible.__version__.split('.')[0])

if ANSIBLE_VERSION < 2:
    from ansible.runner import Runner
    from ansible.playbook import PlayBook
    from ansible import callbacks
    from ansible import utils
elif ANSIBLE_VERSION >= 2:
    from collections import namedtuple
    from ansible.parsing.dataloader import DataLoader
    from ansible.vars import VariableManager
    from ansible.inventory import Inventory
    from ansible.playbook.play import Play
    from ansible.playbook import Playbook
    from ansible.executor.task_queue_manager import TaskQueueManager
    from ansible.executor.playbook_executor import PlaybookExecutor
    from callback import SilentCallbackModule

class Ansible2Runner(object):
    def __init__(self, ansible_host_list, module_name=None,ansible_patt=None,ansible_args=None):
        self.ansible_host_list = ansible_host_list
        self.module_name = module_name
        self.ansible_patt = ansible_patt
        self.module_args = ansible_args
        self.Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check'])
        self.options = self.Options(connection='local', module_path='/path/to/mymodules', forks=100, become=None, become_method=None, become_user=None, check=False)
        self.passwords = dict(vault_pass='secret')


    def execute(self):
        loader = DataLoader()
        variable_manager = VariableManager()

        inventory = Inventory(
            loader=loader,
            variable_manager=variable_manager,
            host_list=self.ansible_host_list
        )

        variable_manager.set_inventory(inventory)

        play_source = {}
        if self.module_args:
            play_source = {
                'name': "Suitable Play",
                'hosts': self.ansible_patt,
                'gather_facts': 'no',
                'tasks': [{
                    'action': {
                        'module': self.module_name,
                        'args': self.module_args
                    }
                }]
            }
        else:
            play_source = {
                'name': "Suitable Play",
                'hosts': self.ansible_patt,
                'gather_facts': 'no',
                'tasks': [{
                    'action': {
                        'module': self.module_name
                    }
                }]
            }

        play = Play.load(
            play_source,
            variable_manager=variable_manager,
            loader=loader
        )

        task_queue_manager = None
        callback = SilentCallbackModule()

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

    def evaluate_results(self, callback):
        ret = {}
        ret['dark'] = {}
        ret['contacted'] = {}
        for server, result in callback.unreachable.items():
            ret['dark']['server'] = result

        for server, answer in callback.contacted.items():
             ret['contacted']['server'] = answer['result']

        return ret

class AnsibleApi(object):
    def __init__(self, ansible_host_list):
        self.ansible_host_list = ansible_host_list

    def remote_execute(self, ansible_mod, ansible_patt, ansible_args=None):
        ret = None

        if ANSIBLE_VERSION < 2:
            if ansible_args:
                runner_obj = Runner(
                        module_name=ansible_mod,
                        module_args=ansible_args,
                        host_list=self.ansible_host_list,
                        pattern=ansible_patt,
                    )
            else:
                runner_obj = Runner(
                        module_name=ansible_mod,
                        host_list=self.ansible_host_list,
                        pattern=ansible_patt,
                    )

            ret = runner_obj.run()
        elif ANSIBLE_VERSION >= 2:
            runner_obj = Ansible2Runner(self.ansible_host_list, ansible_mod, ansible_patt, ansible_args)
            ret = runner_obj.execute()

        return ret

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
        if ANSIBLE_VERSION < 2:
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
        elif ANSIBLE_VERSION >= 2:
            ret = {'contacted': '暂时不支持'}

        return ret

if __name__ == '__main__':
    run_obj = AnsibleApi(PATH + "/hosts.py")
    # ret_shell = run_obj.shell_remote_execute('192.168.33.11', 'ps -ef | grep nginx')
    # print ret_shell
    # ret_ping = run_obj.remote_ping('all')
    # print ret_ping
    # ret_setup = run_obj.remote_setup('192.168.33.12')
    # print ret_setup
    # ret_playbook = run_obj.playbook_api("test.yml")
    # print ret_playbook
    ret_fetch_file = run_obj.fetch_remote_file('192.168.33.11,192.168.33.12', '/home/zhujin/db.sqlite3', 'logs/')
    print ret_fetch_file
