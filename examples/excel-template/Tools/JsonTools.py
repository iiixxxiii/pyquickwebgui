# coding=utf-8
import sys
import datetime
from LogTools import LogTools
import json


reload(sys)
sys.setdefaultencoding('utf-8')


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>MyEncoder obj="+ str(obj))
        s,v = self.test_number(obj)
        if s:
            return v
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj)
        if hasattr(obj, 'dtype'):
            # obj = obj.item()
            obj = str(obj)
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        #elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            # return json.JSONEncoder.default(self, obj)
            return str(obj).encode('ascii','backslashreplace').decode('unicode-escape')

    def test_number(self , s):
        s = str(s)
        try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
            return True , float(s)
        except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
            pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
        try:
            import unicodedata  # 处理ASCii码的包
            # 把一个表示数字的字符串转换为浮点数返回的函数
            return True , unicodedata.numeric(s)
        except (TypeError, ValueError):
            pass
        return False, s


class JsonTools():

    def __init__(self, log=None ):
        if log:
            self.log = log
        else:
            self.log = LogTools().getlogger()


    def dumps(self, data ):
        # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>dumps data=" + str(data))
        return json.dumps(obj=data,cls=MyEncoder,ensure_ascii=False)

