# -*- coding: utf-8 -*-
'''
@File    :   DefaultServerFlask.py
@Time    :   2025/06/10 10:36:03
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''
from .BaseDefaultServer  import BaseDefaultServer

class DefaultServerFlask(BaseDefaultServer):
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {"app": kwargs.get("app"), "port": kwargs.get("port")}

    @staticmethod
    def server(**server_kwargs):
        app = server_kwargs.pop("app", None)
        server_kwargs.pop("debug", None)

        try:
            import waitress

            waitress.serve(app, **server_kwargs)
        except:
            app.run(**server_kwargs)

