import logging
import os
from BasePlugin import BasePlugin

# 定义颜色代码
COLORS = {
    'DEBUG': '\033[94m',  # 蓝色
    'INFO': '\033[92m',   # 绿色
    'WARNING': '\033[93m',  # 黄色
    'ERROR': '\033[91m',   # 红色
    'CRITICAL': '\033[95m',  # 紫色
    'RESET': '\033[0m'     # 重置颜色
}

class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        color_code = COLORS.get(record.levelname, COLORS['RESET'])
        return f"{color_code}{log_message}{COLORS['RESET']}"






class LogPlugin(BasePlugin):

    def __init__(self, name="QuikeUILogger"):
        super().__init__()

         # 配置日志
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        formatter_str = "%(levelname)s: %(asctime)s [%(filename)s:%(lineno)d]: %(message)s"
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        # 使用自定义的 Formatter
        c_formatter = ColoredFormatter(formatter_str)
        console_handler.setFormatter(c_formatter)

        # 创建 FileHandler，指定日志文件路径
        log_file_path = "./logs/app.log"  # 日志文件保存路径
        # 确保日志目录存在
        os.makedirs("./logs", exist_ok=True)  # 如果目录不存在，则创建
        file_handler = logging.FileHandler(log_file_path)
        f_formatter = logging.Formatter(formatter_str)
        file_handler.setFormatter(f_formatter)


        # 添加处理器到 logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)





    def run(self , app):
        # 注册 logger 到 app
        if app is not None and self.logger is not None and app.log is None:
            app.log = self.logger
        app.log.info("LogPlugin is running")
        print("LogPlugin is running")
# 测试继承关系
def check_inheritance():
    if issubclass(LogPlugin, BasePlugin) and LogPlugin is not BasePlugin:
        print(f"{LogPlugin.__name__} 是 {BasePlugin.__name__} 的子类")
    else:
        print(f"{LogPlugin.__name__} 不是 {BasePlugin.__name__} 的子类")


if __name__ == "__main__":
    log =  LogPlugin("ColorLogger")
    # 测试日志
    log.logger.debug("这是一个调试信息")
    log.logger.info("这是一个普通信息")
    log.logger.warning("这是一个警告信息")
    log.logger.error("这是一个错误信息")
    log.logger.critical("这是一个严重错误信息")

    check_inheritance()