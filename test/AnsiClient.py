# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''
import json
import httplib2

data = {
    'group_or_host': '192.168.33.11',
    'cmd': 'pwd'
}

req_body = json.dumps(data)

http = httplib2.Http()

api = "http://ansible.api.xz.com/exec_cmd"

response, content = http.request(api, 'POST', body=req_body, headers={'Content-Type': 'application/json'})

print response
print content

data = {
	'module': 'shell',
    'group_or_host': '192.168.33.11',
    #'arg': '/usr/local/bin/rsync_AnsiApi_to_src.sh'
    'arg': 'cd /usr/local/;pwd'
}

req_body = json.dumps(data)

api = "http://ansible.api.xz.com/adhoc"

response, content = http.request(api, 'POST', body=req_body, headers={'Content-Type': 'application/json'})

print response['status']
print content


data = {'yml': '/usr/local/AnsiApi/yaml/t.yml'}

req_body = json.dumps(data)

api = "http://ansible.api.xz.com/pb"

response, content = http.request(api, 'POST', body=req_body, headers={'Content-Type': 'application/json'})

print response
print content


