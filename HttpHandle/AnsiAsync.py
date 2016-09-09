# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''
import json
import os
import yaml
from tornado import gen
from tornado.web import HTTPError
from tornado.web import RequestHandler, asynchronous
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from Core.logger import mylogger
from Core.AnsibleApi import AnsibleApi
import config

logger = mylogger("AnsiAsync", config.LOG_FP)

class IndexHandler(RequestHandler):
    def get(self):
        self.write("Ansible API")
        self.finish()
        

class CmdHandler(RequestHandler):
    executor = ThreadPoolExecutor(cpu_count())

    @asynchronous
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, e.message)
        logger.info("[CMD] post data: %s" % data)
        response = yield self.exec_cmd(data.get("group_or_host"), data.get("cmd"))
        logger.info("[CMD] %s" % response)
        self.write(json.dumps(response))
        self.finish()

    @run_on_executor
    def exec_cmd(self, group_or_host, cmd):
        res = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = res.shell_remote_execute(group_or_host, cmd)
        return result
        
class SetupHandler(RequestHandler):
    executor = ThreadPoolExecutor(cpu_count())

    @asynchronous
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, reason=e.message)
        logger.info("[SETUP] post data: %s" % data)
        group_or_host = data.get("group_or_host")
        if not group_or_host:
            raise HTTPError(400, reason="ansible setup module need group_or_host.")

        response = yield self.setup(group_or_host)
        logger.info("[SETUP] %s" % response)
        self.write(json.dumps(response))
        self.finish()

    @run_on_executor
    def setup(self, group_or_host):
        res = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = res.remote_setup(group_or_host)
        return result
    
class AdhocHandler(RequestHandler):
    executor = ThreadPoolExecutor(cpu_count())

    @asynchronous
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, reason=e.message)
        logger.info("[ADHOC] post data: %s" % data)
        module, group_or_host, arg = data.get("module"), data.get("group_or_host"), data.get("arg")
        if not(module and group_or_host and arg):
            raise HTTPError(400, reason="ansible module and group_or_host are required. if ansible module need arg,arg is required")

        response = yield self.adhoc(module, group_or_host, arg)
        logger.info("[ADHOC] %s" % response)
        self.write(json.dumps(response))
        self.finish()

    @run_on_executor
    def adhoc(self, module, group_or_host, arg=None):
        res = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = res.remote_execute(module, group_or_host, arg)
        return result
    
class PlaybookHandler(RequestHandler):
    executor = ThreadPoolExecutor(cpu_count())
    
    @asynchronous
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, reason=e.message)
        logger.info("[PLAYBOOK] post data: %s" % data) 
        
        yml_fp = data.get("yml").encode("utf-8") 
        if not os.path.isfile(yml_fp):
            raise HTTPError(400, reason="playbook file is required.")
            
        response =  yield self.pbex(yml_fp)
        logger.info("[PLAYBOOK] %s" % response)
        self.write(json.dumps(response))
        self.finish()
        
    @run_on_executor
    def pbex(self, yml_fp):
        resp = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = resp.playbook_api(yml_fp)
        return result 
