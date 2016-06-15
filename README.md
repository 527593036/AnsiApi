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

2、nginx配置
upstream AnsiApi {
    server 127.0.0.1:10000;
    server 127.0.0.1:10001;
    server 127.0.0.1:10002;
    server 127.0.0.1:10003;
}

server {
    listen 80;
    server_name www.test.com;

    location /static/ {
        root /var/www/static;
        if ($query_string) {
            expires max;
        }
    }

    location / {
        proxy_pass_header Server;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Scheme $scheme;
        proxy_pass http://AnsiApi;
    }
}

3、supervisor配置文件(/etc/supervisor/conf.d/AnsiApi.conf)
[group:tornadoes]
programs=tornado-10000,tornado-10001,tornado-10002,tornado-10003

[program:tornado-10000]
command=python /usr/local/AnsiApi/AnsiApi.py --port=10000
directory=/usr/local/AnsiApi
user=root
autorestart=true
redirect_stderr=true
stdout_logfile=/usr/local/AnsiApi/logs/AnsiApi.log
loglevel=info

[program:tornado-10001]
command=python /usr/local/AnsiApi/AnsiApi.py --port=10001
directory=/usr/local/AnsiApi
user=root
autorestart=true
redirect_stderr=true
stdout_logfile=/usr/local/AnsiApi/logs/AnsiApi.log
loglevel=info

[program:tornado-10002]
command=python /usr/local/AnsiApi/AnsiApi.py --port=10002
directory=/usr/local/AnsiApi
user=root
autorestart=true
redirect_stderr=true
stdout_logfile=/usr/local/AnsiApi/logs/AnsiApi.log
loglevel=info

[program:tornado-10003]
command=python /usr/local/AnsiApi/AnsiApi.py --port=10003
directory=/usr/local/AnsiApi
user=root
autorestart=true
redirect_stderr=true
stdout_logfile=/usr/local/AnsiApi/logs/AnsiApi.log
loglevel=info
