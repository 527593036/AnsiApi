# -*-coding: utf-8-*-
'''
Created on 2016年6月11日

@author: zhujin
'''

from HttpHandle import AnsiAsync
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

define("port", default=8001, help="Port to listen on", type=int)

def main():
    urls = [
        (r"/", AnsiAsync.IndexHandler),
        (r"/exec_cmd", AnsiAsync.CmdHandler),
        (r"/setup", AnsiAsync.SetupHandler),
        (r"/adhoc", AnsiAsync.AdhocHandler),
        (r"/pb", AnsiAsync.PlaybookHandler),
    ]

    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=urls, debug=False)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
    
    
