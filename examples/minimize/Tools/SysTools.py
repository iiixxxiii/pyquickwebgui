# coding=utf-8
import sys, os, urllib

from LogTools import LogTools

reload(sys)
sys.setdefaultencoding('utf-8')


class SysTools():

    def __init__(self, log=None):
        if log:
            self.log = log
        else:
            self.log = LogTools().getlogger()


    def byteify(self, input, encoding='utf-8'):
        if isinstance(input, dict):
            return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.byteify(element) for element in input]
        elif isinstance(input, unicode):
            print  "input:" + str(input)
            return input.encode(encoding)
        else:
            return input

    def url_decode(self, input):
        if isinstance(input, dict):
            return {self.url_decode(key): self.url_decode(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.url_decode(element) for element in input]
        else:
            return urllib.unquote(input)

    def cdir(self, path):
        # 判断路径是否存在
        isExists = os.path.exists(path)

        if not isExists:
            # 如果不存在，则创建目录（多层）
            os.makedirs(path)
            self.log.info('目录创建成功！' + path)
            return True
        else:
            # 如果目录存在则不创建，并提示目录已存在
            self.log.info('目录已存在！'+ path)
            return False

    def to_utf8(self, data):
        """
        未知编码字符串转为utf-8编码
        :param data: 未知编码字符串
        :return: utf-8编码字符串
        """
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