class BasePlugin:
    def run(self):
        raise NotImplementedError("插件必须实现 run 方法")

