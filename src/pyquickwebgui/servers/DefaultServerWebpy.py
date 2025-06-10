
import os
import platform
import traceback
from .BaseDefaultServer  import BaseDefaultServer

class DefaultWebpyHtmlHandler:

    base_path = ""
    pages_path = ""
    render = None
    @staticmethod
    def set_base_path( _base_path ):
        import web
        print("set_base_path _base_path:%s" %(str(_base_path)))
        DefaultWebpyHtmlHandler.base_path = _base_path
        DefaultWebpyHtmlHandler.pages_path = _base_path + '/static/pages/'

        if 'Windows' == platform.system().lower():
            DefaultWebpyHtmlHandler.base_path = DefaultWebpyHtmlHandler.base_path.replace('\\', '/')
            DefaultWebpyHtmlHandler.pages_path= DefaultWebpyHtmlHandler.pages_path.replace('\\', '/')

        DefaultWebpyHtmlHandler.render = web.template.render(DefaultWebpyHtmlHandler.pages_path)
    def GET(self, filename="index"):
        import web
        web.header('Content-Type', 'text/html;charset=UTF-8')
        path = DefaultWebpyHtmlHandler.pages_path + filename + '.html'
        if 'Windows' == platform.system().lower():
            path = path.replace('\\', '/')

        print("HtmlHandler path:%s" %(str(path)))
        fpt = ""
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding="UTF-8") as fp:
                   return fp.read()
                    # fpt = web.template.Template(fp.read())(filename)
                    # return DefaultWebpyHtmlHandler.render.layout(fpt)
        except Exception as e:
            print(traceback.format_exc())
            return "500 err"
        return "not found"

class DefaultWebpyStaticHandler:

    def GET(self, filename=""):

        path = DefaultWebpyHtmlHandler.pages_path + filename
        if 'Windows' == platform.system().lower():
            path = path.replace('\\', '/')
        print("=========>StaticHandler path:%s" %(str(path)))
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding="UTF-8") as fp:
                   return fp.read()
        except Exception as e:
            print(traceback.format_exc())
            return "500 err"
        return "not found"


class DefaultServerWebpy(  BaseDefaultServer ):

    @staticmethod
    def get_server_kwargs(**kwargs):

        DefaultWebpyUrls =  (
                            '/', 'DefaultWebpyHtmlHandler',
                            '/page/(.*)\.html', 'DefaultWebpyHtmlHandler',
                            '/static/(.*)\.(js|css|png|jpg|gif|ico|svg)', 'DefaultWebpyStaticHandler',
                            )

        if "base_path" in kwargs :
            DefaultWebpyHtmlHandler.set_base_path(kwargs.get("base_path"))
        return {
            "app": kwargs.get("app"),
            "urls":kwargs.get("urls") if "urls" in kwargs else DefaultWebpyUrls,
            "fvars": kwargs.get("fvars") if "fvars" in kwargs  else  globals(),
            "port": kwargs.get("port") ,
        }

    @staticmethod
    def server(**server_kwargs):
        import web
        class WebApp(web.application):
            '''
            2024年6月29日 py web
            '''
            def __init__(self, urls=(),  fvars=globals()):
                """
                :type urls: object 路径
                """
                self.urls = urls
                web.application.__init__(self, self.urls, fvars)

            def run(self, port=18080, *middleware):
                func = self.wsgifunc(*middleware)
                return web.httpserver.runsimple(func, ('0.0.0.0', port))
        # print("==========>DefaultServerWebpy-server port={} urls={}".format( server_kwargs["port"],server_kwargs["urls"] ))
        WebApp(urls= server_kwargs["urls"] , fvars =server_kwargs["fvars"]).run(port = server_kwargs["port"] )

