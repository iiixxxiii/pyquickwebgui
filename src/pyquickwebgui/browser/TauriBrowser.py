# -*- coding: utf-8 -*-
'''
@File    :   DefaultServerFlask.py
@Time    :   2025/06/10 10:36:03
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''

from .BaseBrowser  import BaseBrowser



class TauriBrowser(BaseBrowser):
    @staticmethod
    def get_view_kwargs(**kwargs):
        return {"app": kwargs["app"], "port": kwargs["port"]}

    @staticmethod
    def view(**server_kwargs):
        import waitress
        from whitenoise import WhiteNoise

        application = WhiteNoise(server_kwargs["app"])
        server_kwargs.pop("app")

        waitress.serve(application, threads=100, **server_kwargs)
