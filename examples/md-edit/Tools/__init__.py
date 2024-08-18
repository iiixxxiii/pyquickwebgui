# coding: UTF-8
from .OtherTools import *
from .LogTools import LogTools
from .TkTools import TkTools
from .SysTools import SysTools
 

class _Tools():
    def __init__(self):
        self.logTools  = LogTools()
        _log = self.logTools.getlogger()
        self.log = _log
        # 全局参数
        self.gdata = {}
        self.commonStatic = CommonStatic
        self.render = web.template.render(CommonStatic.root_path + '/static/pages/')
        self.returnData = ReturnData()
        self.out = OutTools(log=_log)
        self.sys = SysTools(log=_log)
        self.tk = TkTools(log=_log)
        # self.init_log_file("/tmp/main.log")


    def init_log_file(self,file_path):
        directory_path = os.path.dirname(os.path.abspath(file_path))
        print(directory_path)
        self.sys.cdir(directory_path)
        self.logTools.set_log_file(file_path)


tools = _Tools()

__all__ = ["WebApp","tools","LogTools"]

