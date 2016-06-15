# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''
import json
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

class CmdHandler(RequestHandler):
    executor = ThreadPoolExecutor(cpu_count())

    @asynchronous
    @gen.coroutine
    def post(self):
        try:
            data = json.loads(self.request.body)
        except ValueError as e:
            raise HTTPError(400, e.message)
        logger.info("post data: %s" % data)
        response = yield self.exec_cmd(data.get("group_or_host"), data.get("cmd"))
        logger.info(response)
        self.write(json.dumps(response))
        self.finish()

    @run_on_executor
    def exec_cmd(self, group_or_host, cmd):
        res = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = res.shell_remote_execute(group_or_host, cmd)
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
        logger.info("post data: %s" % data)
        module, group_or_host, arg = data.get("module"), data.get("group_or_host"), data.get("arg")
        if not(module and group_or_host and arg):
            raise HTTPError(400, reason="ansible module and group_or_host are required. if ansible module need arg,arg is required")

        response = yield self.adhoc(module, group_or_host, arg)
        logger.info(response)
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
        logger.info("post data: %s" % data) 
        
        yml_fp = data.get("yml")
        if not(yml_fp):
            raise HTTPError(400, reason="playbook file is required.")
        
        response = self.pb(yml_fp)
        logger.info(response)
        self.write(json.dumps(response))
        self.finish()
        
    @run_on_executor
    def pb(self, yml_fp):
        res = AnsibleApi(config.ANSIBLE_HOSTS_LIST)
        result = res.playbook_api(yml_fp)
        return result
        
        
    





