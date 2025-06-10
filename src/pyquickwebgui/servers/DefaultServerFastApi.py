# -*- coding: utf-8 -*-
'''
@File    :   DefaultServerFastApi.py
@Time    :   2025/06/10 10:36:09
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''
from .BaseDefaultServer  import BaseDefaultServer

class DefaultServerFastApi(BaseDefaultServer):
    @staticmethod
    def get_server_kwargs(**kwargs):
        server_kwargs = {
            "app": kwargs.get("app"),
            "port": kwargs.get("port"),
            # "reload": kwargs.get("reload"),
            "log_level": kwargs.get("log_level")
        }
        return server_kwargs

    @staticmethod
    def server(**server_kwargs):
        import uvicorn
        print("======>staticmethod reload {}".format(server_kwargs.get("reload")))
        uvicorn.run(**server_kwargs)
        # print("======>staticmethod server2")
