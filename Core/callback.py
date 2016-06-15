#-*-coding: utf-8-*-
'''
Created on 2016年6月13日

@author: zhujin
'''

from ansible.plugins.callback import CallbackBase

class SilentCallbackModule(CallbackBase):
    def __init__(self):
        self.unreachable = {}
        self.contacted = {}

    def runner_on_ok(self, host, result):
        self.contacted[host] = {
            'success': True,
            'result': result
        }

    def runner_on_failed(self, host, result, ignore_errors=False):
        self.contacted[host] = {
            'success': False,
            'result': result
        }

    def runner_on_unreachable(self, host, result):
        self.unreachable[host] = result
