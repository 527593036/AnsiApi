# AnsiApi

注意事项

AnsiApi暂时不支持ansible2的playbook

Installation

1、python环境安装

pip install tornado

pip install futures

pip install ansible==1.9.5

2、nginx安装（略）

3、supervisor安装(略)

Configuration

1、inventory配置

config.py中ANSIBLE_HOSTS_LIST配置成对应的inventory获取脚本

2、nginx配置,见nginx.conf

3、supervisor配置文件,见AnsiApi.conf

放置目录：/etc/supervisor/conf.d/AnsiApi.conf
