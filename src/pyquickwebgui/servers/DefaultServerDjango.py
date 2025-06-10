# -*- coding: utf-8 -*-
'''
@File    :   DefaultServerFlask.py
@Time    :   2025/06/10 10:36:03
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''

from .BaseDefaultServer  import BaseDefaultServer



class DefaultServerDjango(BaseDefaultServer):
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {"app": kwargs["app"], "port": kwargs["port"]}

    @staticmethod
    def server(**server_kwargs):
        import waitress
        from whitenoise import WhiteNoise

        application = WhiteNoise(server_kwargs["app"])
        server_kwargs.pop("app")

        waitress.serve(application, threads=100, **server_kwargs)
