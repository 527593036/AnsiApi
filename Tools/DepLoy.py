# -*-coding: utf-8-*-
'''
Created on 2016年8月24日

@author: zhujin
'''

import argparse
import json

import os
PATH = os.path.split(os.path.realpath(__file__))[0]

import sys
sys.path.append(PATH+'/../')
from config import AnsiApiHost
from Comm.AnsiClient import AnsiClient


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-yml', action="store", dest='yaml_file', help='/path/for/yaml/file')
    parser.add_argument('-m', action="store", dest='module', help='ansible module')
    parser.add_argument('-goh', action="store", dest='group_or_hosts', help='ansible group or hosts,example: all or 192.168.1.11,192.168.12')
    parser.add_argument('-a', action="store", dest='arg', help='ansible argument')
    
    args = parser.parse_args()
    
    yaml_file = args.yaml_file
    goh = args.group_or_hosts
    m = args.module
    argument = args.arg
    
    ansi_api_client = AnsiClinet(AnsiApiHost)
    
    if yaml_file:
        yaml_file = PATH + '/yaml/' + yaml_file
        data = {
            'yml': yaml_file,
        }
        print json.dumps(ansi_api_client.playbook(data),indent=4)
    elif goh and m:
        if argument:
            data = {
            	'module': m,
                'group_or_host': goh,
                'arg': argument,
            }
        else:
            data = {
            	'module': m,
                'group_or_host': goh,
            }    
        print json.dumps(ansi_api_client.adhoc(data))
    else:
        print "Usage: python DepLoy.py -h,example: python DepLoy.py -yaml test.yml or python DepLoy.py -m shell -goh all -a pwd"
        
if __name__ == '__main__':
    main()
            
    