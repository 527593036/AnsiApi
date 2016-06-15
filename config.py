# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''

import os

PATH = os.path.split(os.path.realpath(__file__))[0]

ANSIBLE_HOSTS_LIST = PATH + "/inventory.sh"
LOG_FP = "/tmp/AnsiAsync.log"
