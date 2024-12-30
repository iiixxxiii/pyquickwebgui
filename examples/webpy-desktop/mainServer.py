
import os
import platform
import web
from pyquickwebgui import QuikeUI






class index:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        return "hello world web.py"





if __name__ in {"__main__", "__mp_main__"}:

    QuikeUI(server="webpy",base_path=os.getcwd()).run()

    # QuikeUI(
    #     server="webpy",
    #     server_kwargs = {
    #                         "urls" : (
    #                                 '/', 'index'
    #                         ),
    #                         "fvars" : globals()
    #                     },
    #     width=800,
    #     height=600,
    #     fullscreen = True,
    #     on_startup=lambda: print("start"),
    #     on_shutdown=lambda: print("close"),
    # ).run()
