# coding=utf-8


# 标准库
from calendar import c
import os
import platform
from re import A, S
import traceback
import psutil
import shutil
import signal
import subprocess
import tempfile
import threading
import time
import uuid
import webbrowser
import socketserver
import multiprocessing
from multiprocessing import Process
from threading import Thread
# 第三方库
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

from pyrsistent import b




class BaseDefaultServer:
    server: Callable
    get_server_kwargs: Callable


class DefaultServerFastApi:
    @staticmethod
    def get_server_kwargs(**kwargs):
        server_kwargs = {"app": kwargs.get("app"), "port": kwargs.get("port")}
        return server_kwargs

    @staticmethod
    def server(**server_kwargs):
        import uvicorn

        uvicorn.run(**server_kwargs)


class DefaultServerFlask:
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


class DefaultServerDjango:
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


class DefaultServerFlaskSocketIO:
    @staticmethod
    def get_server_kwargs(**kwargs):
        return {
            "app": kwargs.get("app"),
            "flask_socketio": kwargs.get("flask_socketio"),
            "port": kwargs.get("port"),
        }

    @staticmethod
    def server(**server_kwargs):
        server_kwargs["flask_socketio"].run(
            server_kwargs["app"], port=server_kwargs["port"]
        )




class DefaultWebpyHtmlHandler:

    base_path = ""
    pages_path = ""
    render = None
    @staticmethod
    def set_base_path( _base_path ):
        import web
        print("set_base_path _base_path:%s" %(str(_base_path)))
        DefaultWebpyHtmlHandler.base_path = _base_path
        DefaultWebpyHtmlHandler.pages_path = _base_path + '/static/pages/'

        if 'Windows' == platform.system().lower():
            DefaultWebpyHtmlHandler.base_path = DefaultWebpyHtmlHandler.base_path.replace('\\', '/')
            DefaultWebpyHtmlHandler.pages_path= DefaultWebpyHtmlHandler.pages_path.replace('\\', '/')

        DefaultWebpyHtmlHandler.render = web.template.render(DefaultWebpyHtmlHandler.pages_path)
    def GET(self, filename="index"):
        import web
        web.header('Content-Type', 'text/html;charset=UTF-8')
        path = DefaultWebpyHtmlHandler.pages_path + filename + '.html'
        if 'Windows' == platform.system().lower():
            path = path.replace('\\', '/')

        print("HtmlHandler path:%s" %(str(path)))
        fpt = ""
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding="UTF-8") as fp:
                   return fp.read()
                    # fpt = web.template.Template(fp.read())(filename)
                    # return DefaultWebpyHtmlHandler.render.layout(fpt)
        except Exception as e:
            print(traceback.format_exc())
            return "500 err"
        return "not found"

class DefaultWebpyStaticHandler:

    def GET(self, filename=""):

        path = DefaultWebpyHtmlHandler.pages_path + filename
        if 'Windows' == platform.system().lower():
            path = path.replace('\\', '/')
        print("=========>StaticHandler path:%s" %(str(path)))
        try:
            if os.path.isfile(path):
                with open(path, 'r', encoding="UTF-8") as fp:
                   return fp.read()
        except Exception as e:
            print(traceback.format_exc())
            return "500 err"
        return "not found"


class DefaultServerWebpy:

    @staticmethod
    def get_server_kwargs(**kwargs):

        DefaultWebpyUrls =  (
                            '/', 'DefaultWebpyHtmlHandler',
                            '/page/(.*)\.html', 'DefaultWebpyHtmlHandler',
                            '/static/(.*)\.(js|css|png|jpg|gif|ico|svg)', 'DefaultWebpyStaticHandler',
                            )

        if "base_path" in kwargs :
            DefaultWebpyHtmlHandler.set_base_path(kwargs.get("base_path"))
        return {
            "app": kwargs.get("app"),
            "urls":kwargs.get("urls") if "urls" in kwargs else DefaultWebpyUrls,
            "fvars": kwargs.get("fvars") if "fvars" in kwargs  else  globals(),
            "port": kwargs.get("port") ,
        }

    @staticmethod
    def server(**server_kwargs):
        import web
        class WebApp(web.application):
            '''
            2024年6月29日 py web
            '''
            def __init__(self, urls=(),  fvars=globals()):
                """
                :type urls: object 路径
                """
                self.urls = urls
                web.application.__init__(self, self.urls, fvars)

            def run(self, port=18080, *middleware):
                func = self.wsgifunc(*middleware)
                return web.httpserver.runsimple(func, ('0.0.0.0', port))
        # print("==========>DefaultServerWebpy-server port={} urls={}".format( server_kwargs["port"],server_kwargs["urls"] ))
        WebApp(urls= server_kwargs["urls"] , fvars =server_kwargs["fvars"]).run(port = server_kwargs["port"] )


class QuickConfig:
    version = "0.0.1"
    FLASKWEBGUI_USED_PORT = None
    FLASKWEBGUI_BROWSER_PROCESS = None

    DEFAULT_BROWSER = webbrowser.get().name
    OPERATING_SYSTEM = platform.system().lower()
    PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"


    linux_browser_paths = [
        r"/usr/bin/google-chrome",
        r"/usr/bin/microsoft-edge",
        r"/usr/bin/brave-browser",
        r"/usr/bin/chromium",
        # Web browsers installed via flatpak portals
        r"/run/host/usr/bin/google-chrome",
        r"/run/host/usr/bin/microsoft-edge",
        r"/run/host/usr/bin/brave-browser",
        r"/run/host/usr/bin/chromium",
        # Web browsers installed via snap
        r"/snap/bin/chromium",
        r"/snap/bin/brave-browser",
        r"/snap/bin/google-chrome",
        r"/snap/bin/microsoft-edge",
    ]

    mac_browser_paths = [
        r"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        r"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        r"/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ]

    windows_browser_paths = [
        #优先 启动 chrome
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    ]

    browser_path_dispacher: Dict[str, Callable[[], str]] = {
        "windows": lambda: QuickConfig.find_browser_in_paths(QuickConfig.windows_browser_paths),
        "linux": lambda: QuickConfig.find_browser_in_paths(QuickConfig.linux_browser_paths),
        "darwin": lambda: QuickConfig.find_browser_in_paths(QuickConfig.mac_browser_paths),
    }


    webserver_dispacher: Dict[str, BaseDefaultServer] = {
        "fastapi": DefaultServerFastApi,
        "flask": DefaultServerFlask,
        "flask_socketio": DefaultServerFlaskSocketIO,
        "django": DefaultServerDjango,
        "webpy": DefaultServerWebpy,
    }

    @staticmethod
    def get_free_port():
        with socketserver.TCPServer(("localhost", 0), None) as s:
            free_port = s.server_address[1]
        return free_port

    @staticmethod
    def kill_port(port: int):
        for proc in psutil.process_iter():
            try:
                for conns in proc.net_connections(kind="inet"):
                    if conns.laddr.port == port:
                        proc.send_signal(signal.SIGTERM)
            except psutil.AccessDenied:
                continue

    @staticmethod
    def find_browser_in_paths(browser_paths: List[str]):

        compatible_browser_path = None
        for path in browser_paths:

            if not os.path.exists(path):
                continue

            if compatible_browser_path is None:
                compatible_browser_path = path

            if QuickConfig.DEFAULT_BROWSER in path:
                return path

        return compatible_browser_path





@dataclass
class QuikeUI:

    server: Union[str, Callable[[Any], None]]

    server_kwargs: dict = None


    app: Any = None

    # 服务器端口
    port: int = None

    # 窗户宽度。默认值为 800px。
    width: int = 800
    # 窗户高度。默认值为 600px。
    height: int = 600
    # 从全屏模式开始。默认为 False
    fullscreen: bool = False

    on_startup: Callable = None
    on_shutdown: Callable = None
    # 扩展信息
    extra_flags: List[str] = None
    browser_path: str = None
    browser_command: List[str] = None
    socketio: Any = None
    profile_dir_prefix: str = "flaskwebgui"
    app_mode: bool = True
    browser_pid: int = None
    base_path :str = None
    # 创建一个无框窗口。默认值为 False。
    frameless: bool = False
    # 开启调试模式
    debug: bool = False
    # x 窗口 x 坐标。默认值居中。
    x: int = 0
    # y 窗口 y 坐标。默认值居中
    y: int = 0
    # 显示浏览器  默认显示  不显示只是web程序
    show_browser: bool = True
    # 类型  默认为 command  ,  webview
    browser_type: str = "command"

    def __post_init__(self):
        # 初始化键盘中断标志为False
        self.__keyboard_interrupt = False
        # 如果未指定端口，则尝试从服务器配置中获取，若获取失败则调用方法获取一个空闲端口
        if self.port is None:
            self.port = (
                self.server_kwargs.get("port")
                if self.server_kwargs and "port" in self.server_kwargs
                else QuickConfig.get_free_port()
            )

        # 更新全局变量，记录当前使用的端口
        QuickConfig.FLASKWEBGUI_USED_PORT = self.port

        # 如果服务器参数为字符串，则通过调度器获取默认服务器配置
        if isinstance(self.server, str):
            default_server = QuickConfig.webserver_dispacher[self.server]
            self.server = default_server.server

            # 使用默认配置或生成新的服务器配置
            self.server_kwargs = self.server_kwargs or default_server.get_server_kwargs(
                app=self.app,
                port=self.port,
                base_path=self.base_path,
                flask_socketio=self.socketio
            )

            # 自动注入端口
            if "port" not in self.server_kwargs:
                self.server_kwargs["port"] = self.port

        # 生成临时的profile目录路径
        self.profile_dir = os.path.join(
            tempfile.gettempdir(), self.profile_dir_prefix + uuid.uuid4().hex
        )
        # 构造浏览器访问的URL
        self.url = f"http://127.0.0.1:{self.port}"

        # 如果未指定浏览器路径，则尝试根据操作系统获取默认浏览器路径
        self.browser_path = (
            self.browser_path or QuickConfig.browser_path_dispacher.get(QuickConfig.OPERATING_SYSTEM)()
        )
        # 如果未指定浏览器命令，则调用方法生成默认的浏览器命令
        self.browser_command = self.browser_command or self.get_browser_command()

    def get_browser_command(self):
        # https://peter.sh/experiments/chromium-command-line-switches/

        flags = [
            self.browser_path,
            # 用户数据（设置、缓存等）的位置
            f"--user-data-dir={self.profile_dir}",
            # 新窗口
            "--new-window",
            # 启动时不检查是否为默认浏览器
            "--no-default-browser-check",
            "--allow-insecure-localhost",
            "--no-first-run",
            "--disable-sync",
            # 启动隐身无痕模式
            # "--incognito",
            # 不遵守同源策略。关闭web安全检查 允许跨域请求
            "--disable-web-security",
            # 本地开发调试的话，需要忽略证书错误
            # 设置允许访问本地文件
            "--allow-file-access-from-files",
            # "--test-type",
            # "--ignore-certificate-errors",
            # 在离线插页式广告上禁用恐龙复活节彩蛋。
            "--disable-dinosaur-easter-egg",
            # 禁用插件
            "--disable-plugins",
            # # 禁用弹出拦截
            # "--disable-popup-blocking",
        ]

        if self.debug:
            flags.extend(["--auto-open-devtools-for-tabs"])

        # if self.frameless:
        #     flags.extend(["--headless=new"])

        if self.width and self.height and self.app_mode:
            flags.extend([f"--window-size={self.width},{self.height}"])
        elif self.fullscreen:
            flags.extend(["--start-maximized"])

        if self.extra_flags:
            flags = flags + self.extra_flags

        if self.app_mode:
            flags.append(f"--app={self.url}")
        else:
            flags.extend(["--guest", self.url])

        return flags

    def create_webview_window(self,server_kwargs):
        import webview
        from contextlib import redirect_stdout
        from io import StringIO
        print("==========>create_webview_window")
        stream = StringIO()
        with redirect_stdout(stream):
            window = webview.create_window('', self.url ,
                                    width=self.width,
                                    height=self.height,
                                    fullscreen=self.fullscreen )
            webview.start(debug=self.debug)



    def start_browser(self, server_process: Union[Thread,  Process]):
        print("==========>start_browser Quick version:" + QuickConfig.version)

        print("browser_type:{}".format(self.browser_type))

        print("Command:", " ".join(self.browser_command))

        if QuickConfig.OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")


        if self.browser_type == "command":
            QuickConfig.FLASKWEBGUI_BROWSER_PROCESS = subprocess.Popen(self.browser_command)
            self.browser_pid = QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.pid
            QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.wait()
        # else:
        #     multiprocessing.Process( target=self.create_webview_window, kwargs=self.server_kwargs).run()


        if self.browser_path is None:
            while self.__keyboard_interrupt is False:
                time.sleep(1)

        if isinstance(server_process, Process):
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            server_process.kill()

        else:
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)
            QuickConfig.kill_port(self.port)

    def file_path(self):

        return

    def run(self):
        if self.on_startup is not None:
            self.on_startup()


        self.browser_thread=None
        self.server_process=None
        if QuickConfig.OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")
            server_process = Process(
                target=self.server, kwargs=self.server_kwargs or {}
            )
        else:
            server_process = Thread(target=self.server, kwargs=self.server_kwargs or {})

        print("=======>self.browser_type:"+self.browser_type)
        if self.browser_type == "command":
            browser_thread =  Thread(target=self.start_browser  , args=(server_process,))
            try:
                server_process.start()
                if self.show_browser :
                    browser_thread.start()
                    browser_thread.join()
                server_process.join()

            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")
        else:
            try:
                # print("server_process.start")
                server_process.start()
                # print("self.create_webview_window")
                if self.show_browser :
                    self.create_webview_window(self.server_kwargs)
                server_process.join()
                # print("server_process.join")
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")


        return self

    @staticmethod
    def close_application():
        if QuickConfig.FLASKWEBGUI_BROWSER_PROCESS is not None:
            QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.terminate()

        QuickConfig.kill_port(QuickConfig.FLASKWEBGUI_USED_PORT)
