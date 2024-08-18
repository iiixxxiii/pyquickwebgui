# coding=utf-8
import sys, os



reload(sys)
sys.setdefaultencoding('utf-8')



class CommonStaticTools:
    """
    静态参数
    """
    def __init__(self):
        file_path = os.path.abspath(__file__)
        self.root_path = os.path.dirname(file_path)
        self.root_path = self.root_path.replace("Tools","")
        if os.path.isdir("res"):
            self.root_path += "/res"

        self.static_path = os.path.join(self.root_path,"static")
        self.pages_path = os.path.join(self.static_path,"pages")

    def get_root_path(self):
        return self.root_path

    def get_static_path(self):
        return self.static_path

    def get_pages_path(self):
        return self.pages_path


CommonStatic = CommonStaticTools()



if __name__ == "__main__":
    print CommonStatic.get_static_path()