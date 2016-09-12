# AnsiApi

# 用途

AnsiApi是Ansible API，通过向AnsiApi发送命令，通过ansible远程执行命令

AnsiApi已支持ansible, ansible2的playbook,adhoc

# Installation

1、python环境安装

pip install tornado

pip install futures

pip install ansible

2、nginx安装（略）

3、supervisor安装(略)

# Configuration

1、inventory配置

config.py中ANSIBLE_HOSTS_LIST配置成对应的inventory获取脚本

2、nginx配置,见nginx.conf

3、supervisor配置文件,见AnsiApi.conf

放置目录：/etc/supervisor/conf.d/AnsiApi.conf

# Start

1、nginx启动

2、supervisor启动

# 使用方法

```shell
shell

curl -H "Content-type: application/json" -X POST \
 	-d '{"module":"shell","group_or_host":"192.168.33.11","arg":"pwd"}' \
 	http://xx.xx.com/adhoc;echo
```
```python

import httplib2

data = {
	'module': 'shell',
    'group_or_host': '192.168.33.10,192.168.33.11',
    'arg': 'cd /usr/local/;pwd'
}

req_body = json.dumps(data)

api = "http://xx.xx.com/adhoc"

response, content = http.request(api, 'POST', body=req_body, headers={'Content-Type': 'application/json'})

print response['status']

print content
```
