# coding=utf-8
import sys, os
import logging
import getpass
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class LogTools(logging.Logger):
    """
    log = LogTools().getlogger()
    """
    def __init__(self,
                 level='DEBUG',
                 path=None,
                 format="%(asctime)s - %(name)s - [%(levelname)s] - [%(filename)s:%(lineno)d] Thread-%(thread)d - %(message)s"
                 ):
        # logging.Logger.__init__(self)
        login_user = self.to_utf8(getpass.getuser())
        # 设置用户
        logger = logging.getLogger(login_user)

        # 设置级别
        logger.setLevel(level)

        # 设置logging模块的默认编码为UTF-8
        # logging.basicConfig(stream=sys.stdout, level=logging.INFO, encoding='utf-8')
        # 调用模块时,如果错误引用，比如多次调用，每次会添加Handler，造成重复日志，这边每次都移除掉所有的handler，后面在重新添加，可以解决这类问题
        # while logger.hasHandlers():
        #     for i in logger.handlers:
        #         logger.removeHandler(i)
        self.level = level
        self.fmt = logging.Formatter(format)
        # # 初始化处理器
        # if not path:
        #     path = '/tmp/main.log'
        #     if os.path.exists("/tmp/" + login_user):
        #         path = "/tmp/" + login_user + "/main.log"
        # self.file_handle = logging.FileHandler(filename=path) #,encoding='UTF-8'
        # # 创建一个输出到文件的handler
        # # file_handler = logging.FileHandler('log.txt', encoding='utf-8')
        # self.file_handle.setLevel(self.level)
        # self.file_handle.setFormatter(self.fmt)
        # logger.addHandler(self.file_handle)

        self.stream_handler = logging.StreamHandler()
        # 设置handle 的级别
        self.stream_handler.setLevel(level)
        self.stream_handler.setFormatter(self.fmt)

        logger.addHandler(self.stream_handler)

        self.logger = logger

        self.logger.info(msg="==================================["+time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"]================================")


    def getlogger(self):
        return self.logger

    def set_log_file(self,path):
        """
        需要建立目录 参照  tools.init_log_file("./log/local.log")
        :param path:
        :return:
        """
        file_handle = logging.FileHandler(filename=path)
        file_handle.setFormatter(self.fmt)
        if hasattr(self,"file_handle") :
            self.logger.removeFilter(self.file_handle)
        self.logger.addHandler(file_handle)
        self.file_handle = file_handle
        print ("日志路径:"+path)

    def to_utf8(self, data):
        try:
            data_de = data.decode("utf-8")
            return data
        except:
            pass
        try:
            data_de = data.decode("ascii")
            data = data_de.encode("utf-8")
            return data
        except:
            pass
        try:
            data_de = data.decode("gbk")
            data = data_de.encode("utf-8")
            return data
        except:
            pass
        try:
            data_de = data.decode("utf-16-le")
            data = data_de.encode("utf-8")
            return data
        except:
            pass
        # 如果以上几种都不能解码成功，返回传过来的字符串
        return data
