# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''

import os

PATH = os.path.split(os.path.realpath(__file__))[0]

ANSIBLE_HOSTS_LIST = PATH + "/inventory.sh"
LOG_FP = PATH + "/logs/AnsiAsync.log"
AnsiApiHost = "http://xxx.xxx.xxx.xxx"

DBCONF = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'snakeman',
    'db': 'snakeman',
    'charset': 'utf8'
}
