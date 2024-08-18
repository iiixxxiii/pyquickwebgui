# coding=utf-8
import web
import sys, os, time, math, json
import traceback

from LogTools import LogTools

reload(sys)
sys.setdefaultencoding('utf-8')


class WebApp(web.application):
    '''
    2024年6月29日 py web 后台 by lixin
    @version 1.0.0
    '''

    def __init__(self, urls=() , log=None , fvars = globals()):
        if log:
            self.log = log
        else:
            self.log = LogTools().getlogger()
        self.urls = urls
        self.log.info("urls:" + str(urls))
        web.application.__init__(self, self.urls,fvars)

    def run(self, port=8080, *middleware):
        os.system("start chrome 127.0.0.1:" + str(port))
        self.log.info("=========web ok!!!=========")
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))


class index_demo:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        return "hello"


if __name__ == "__main__":
    urls = ('/', 'index_demo')
    WebApp(urls).run(port=8080)
