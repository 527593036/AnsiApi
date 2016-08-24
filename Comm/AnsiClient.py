# -*-coding: utf-8-*-
'''
Created on 2016年7月24日

@author: zhujin
'''

import os
import json
import httplib2

PATH = os.path.split(os.path.realpath(__file__))[0]

class AnsiClient(object): 
    def __init__(self, ansible_api_host):
        self.ansible_api_host = ansible_api_host
        
    def _post_req(self, api, data, method="GET"):
        req_body = json.dumps(data)
        http = httplib2.Http()
        try:
            response, content = http.request(api, method, body=req_body, headers={'Content-Type': 'application/json'})
            content = json.loads(content)
            return [response.status, content]
        except httplib2.HttpLib2Error, e:
            raise e
            
    def command(self,data):
        cmd_api = self.ansible_api_host + '/exec_cmd'
        ret = self._post_req(cmd_api, data, method='POST')
        return ret
        
    def setup(self,data):
        adhoc_api = self.ansible_api_host + '/setup'
        ret = self._post_req(adhoc_api, data, method='POST')
        return ret
        
    def adhoc(self,data):
        adhoc_api = self.ansible_api_host + '/adhoc'
        ret = self._post_req(adhoc_api, data, method='POST')
        return ret
        
    def playbook(self,data):
        playbook_api = self.ansible_api_host + '/pb'
        ret = self._post_req(playbook_api, data, method='POST')
        return ret