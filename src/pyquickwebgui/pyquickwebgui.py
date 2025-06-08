# coding=utf-8


# 标准库
import inspect
import os , sys
import platform
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


import importlib.util


from  .base_plugins.BasePlugin import BasePlugin




static_app = None
class BaseDefaultServer:
    server: Callable
    get_server_kwargs: Callable






class DefaultServerFastApi:
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

    # 版本号
    version = "0.0.3"

    FLASKWEBGUI_USED_PORT = None
    FLASKWEBGUI_BROWSER_PROCESS = None

    # 默认浏览器
    DEFAULT_BROWSER = webbrowser.get().name
    # 操作系统
    OPERATING_SYSTEM = platform.system().lower()

    PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"

    BASE_PLUGINS_DIR = "base_plugins"

    BASE_PLUGIN_CLASS_NAME = "BasePlugin".lower()

    PLUGIN_CLASS_NAME = "plugin"
    # 插件目录
    PLUGINS_DIR = "plugins"

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
    # 只是web程序
    only_webserver: bool = False
    # 显示浏览器  默认显示
    show_browser: bool = True
    # 类型  默认为 command  ,  webview
    browser_type: str = "command"
    # 显示托盘
    stray : bool = False
    # 显示托盘图标
    stray_img : str = ""
    # 显示托盘名称
    stray_name :str =""
    # 显示托盘标题
    stray_title :str =""

    # 日志
    log :object = None
    log_level: str = "info"

    reload : bool = False

    def __post_init__(self):

        self.run_base_plugins()

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
            print("默认服务器配置: self.server {}".format(self.server))
            # 使用默认配置或生成新的服务器配置
            self.server_kwargs = self.server_kwargs or default_server.get_server_kwargs(
                app=self.app,
                port=self.port,
                reload= self.reload,
                log_level =self.log_level,
                base_path=self.base_path,
                flask_socketio=self.socketio
            )

            # 自动注入端口
            if "port" not in self.server_kwargs:
                self.server_kwargs["port"] = self.port
            print("默认服务器配置: self.port {}".format(self.port))
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

        QuikeUI.set_app(self)



    def get_browser_command(self):
        # https://peter.sh/experiments/chromium-command-line-switches/
        # https://www.cnblogs.com/Ghsoft/p/18359891

        flags = [
            self.browser_path,

            # 用户数据（设置、缓存等）的位置
            f"--user-data-dir={self.profile_dir}",
            # 不遵守同源策略。关闭web安全检查 允许跨域请求
            # "--disable-web-security",
            # 新窗口
            "--new-window",
            # 启动时不检查是否为默认浏览器
            "--no-default-browser-check",
            "--allow-insecure-localhost",
            "--no-first-run",
            "--disable-sync",
            # https 页面允许从 http 链接引用 javascript/css/plug-ins
            "--allow-running-insecure-content",
            # 启动隐身无痕模式
            # "--incognito",
            #设置语言为英语_美国
            #"--lang=en_US",
            # 禁用沙盒
            # "--no-sandbox",
            # 启用自助服务终端模式 全屏
            # "--kiosk",
            #隐藏所有消息中心通知弹出窗口
            "--suppress-message-center-popups",
            # 本地开发调试的话，需要忽略证书错误
            # 设置允许访问本地文件
            "--args --allow-file-access-from-files",
            # "--test-type",
            #禁用桌面通知，在 Windows 中桌面通知默认是启用的。
            "--disable-desktop-notifications",
            # 禁用ssl证书检查
            # "--ignore-certificate-errors-spki-list",
            # 在离线插页式广告上禁用恐龙复活节彩蛋。
            "--disable-dinosaur-easter-egg",
            # 禁用插件
            "--disable-plugins",
            # 禁用java
            "--disable-java",
            # 禁用同步
            "--disable-sync",
            # 禁用内部的Flash Player
            "--disable-internal-flash",
            # 禁用同步应用程序
            "--disable-sync-apps",
            # 禁用同步自动填充
            "--disable-sync-autofill",
            # 禁用弹出拦截
            "--disable-popup-blocking",
            # 仅使用信任的插件
            "--trusted-plugins",
            # 禁用翻译
            "--disable-translate",
            "--disable-features=Translate",
        ]

        if self.debug:
            flags.extend(["--auto-open-devtools-for-tabs"])

        # if self.frameless:
        #     flags.extend(["--headless=new"])

        # if self.frameless:
        #     # 启动时不建立窗口
        #     flags.extend(["--disable-desktop-notifications"])


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
        # 创建一个webview窗口

        import webview
        from contextlib import redirect_stdout
        from io import StringIO
        # print("==========>create_webview_window")
        stream = StringIO()
        with redirect_stdout(stream):
            self.browser_thread = webview.create_window('', self.url ,
                                    width=self.width,
                                    height=self.height,
                                    fullscreen=self.fullscreen )
            # print("=============>window.__class__>"+str(self.browser_thread.__class__))
            webview.start(debug=self.debug, gui='cef')

    def start_browser(self, server_process: Union[Thread,  Process]):
        self.log.info("==========>start_browser Quick version:" + QuickConfig.version)

        # print("browser_type:{}".format(self.browser_type))

        self.log.info("Command:{}".format(" ".join(self.browser_command)))

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

            if  self.stray is False:
                print("server_process.kill.")
                server_process.kill()

        else:
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)

            if  self.stray is False:
                print("QuickConfig.kill_port.")
                QuickConfig.kill_port(self.port)

    def load_base_plugins(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 加载系统插件
        base_plugins = []
        base_plugins_dir = os.path.join(current_dir,QuickConfig.BASE_PLUGINS_DIR)
        # print("============>base_plugins_dir:{}  ".format(base_plugins_dir  ))
        sys.path.append(base_plugins_dir)
        for filename in os.listdir(base_plugins_dir):
            if filename.endswith(".py"):
                path = os.path.join(base_plugins_dir, filename)
                name = filename[:-3]
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for item_name in dir(module):
                    if  str(item_name).lower().find(QuickConfig.PLUGIN_CLASS_NAME)>-1 and str(item_name).lower().find(QuickConfig.BASE_PLUGIN_CLASS_NAME)==-1:
                        item = getattr(module, item_name)
                        # print("=+++++=>item:{}  ".format(item) )
                        # print("============>not:{}  ".format(item is not BasePlugin  ))
                        base_plugins.append(item())

        # print("===========>base_plugins[]:{}".format(base_plugins))
        return base_plugins


    def run_base_plugins(self):
        # 加载插件
        self.base_plugins = self.load_base_plugins()
        for plugin in self.base_plugins:
            if hasattr(plugin, "run"):
                plugin.run(self)
            else:
                print(f"run_base_plugins :  {plugin.__name__} 没有定义 run()，跳过~")

    def load_plugins(self):

        # 插件系统
        self.plugins_class = []
        for filename in os.listdir(QuickConfig.PLUGINS_DIR):
            if filename.endswith(".py"):
                path = os.path.join(QuickConfig.PLUGINS_DIR, filename)
                name = filename[:-3]
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                for item_name in dir(module):
                    item = getattr(module, item_name)
                    if isinstance(item, type) and issubclass(item, BasePlugin) and item is not BasePlugin:
                        self.plugins_class.append(item())
        return self.plugins_class


    def run_plugins(self , class_name = ""):
        # 运行 插件
        # 加载插件

        if self.plugins_obj['class_name'] is not None:
            plugin = self.plugins_obj['class_name']
            if hasattr(plugin, "run"):
                plugin.run()

        self.plugins_class = self.load_plugins()
        for plugin in self.plugins:
            if hasattr(plugin, "run"):
                plugin.run()
            else:
                print(f"{plugin.__name__} 没有定义 run()，跳过~")


    def run(self):
        if self.on_startup is not None:
            self.on_startup()


        # 浏览器进程
        self.browser_thread=None

        # 服务器进程
        self.server_process=None


        # 系统托盘 进程
        self.stray_process=None


        print("=======>self.browser_type:"+self.browser_type)
        self.run_stray()
        self.run_server()
        self.run_browser()


        return self

    def run_stray(self):
        # 启动 系统托盘进程
        if self.stray and self.only_webserver is False:
            print("启动 系统托盘进程")
            self.stray_process =  Thread(target=self.start_stray , daemon=True , args=( ) )
            try:
                if self.stray_process :
                    self.stray_process.start()
                    # self.stray_process.join()

            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")

    def run_server(self):
        # 启动服务器进程
        try:
            print("========run_server")
            if QuickConfig.OPERATING_SYSTEM == "darwin":
                multiprocessing.set_start_method("fork")
                self.server_process = Process(
                    target=self.server, kwargs=self.server_kwargs or {}
                )
            else:
                self.server_process = Thread(target=self.server, kwargs=self.server_kwargs or {})

            self.server_process.start()
            # self.server_process.join()
        except Exception as e:
            print("run_server error:",e)

    def run_browser(self):
        if self.only_webserver  :
            return
        # 启动浏览器进程
        print("启动 browser进程")

        if self.browser_type == "command":
            self.browser_thread =  Thread(target=self.start_browser  , args=(self.server_process,))
            try:
                if self.show_browser :
                    self.browser_thread.start()
                    # self.browser_thread.join()
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")
        elif self.browser_type == "webview":
            try:
                # print("server_process.start")
                # self.server_process.start()
                # print("self.create_webview_window")
                if self.show_browser :
                    self.create_webview_window(self.server_kwargs)
                # self.server_process.join()
                # print("server_process.join")
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")

    def start_stray(self):
        print("show_stray!")
        # 创建一个系统托盘图标
        import pystray
        from PIL import Image

        # 定义托盘图标
        # self.stray_icon = None
        if len(self.stray_img) == 0:
            #默认白色
            self.stray_icon = Image.new('RGB', (64, 64), 'white')
        else:
            self.stray_icon = Image.open(self.stray_img)
        # 定义托盘图标被点击时的响应函数
        def on_activate(icon, item):
            """处理托盘图标点击事件"""
            print("托盘图标被点击")
        def on_menu_click(icon, item):
            """处理菜单项点击事件"""
            if str(item) == "Show":
                print("显示功能被触发")
                self.run_browser()
            # elif str(item) == "隐藏":
            #     print("隐藏功能被触发")
            elif str(item) == "Exit":
                self.close_application()

        # 创建一个系统托盘对象
        menu = (
            pystray.MenuItem("Show",lambda icon, item: on_menu_click(icon, item)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit",lambda icon, item: on_menu_click(icon, item)),
        )

        # 将托盘图标、菜单和点击响应函数传给系统托盘对象并启动
        pystray.Icon(
            name=self.stray_name,
            icon=self.stray_icon,
            title=self.stray_title,
            menu=menu,
            activate=on_activate  # 绑定点击事件
        ).run()

    @staticmethod
    def get_log():
        return QuikeUI.get_app().log

    @staticmethod
    def open_local_file(title="选择文件", file_filter = [("所有文件", "*.*")]  ):
        # 打开文件
        QuikeUI.get_app().log.info("open_local_file file_filter:{}".format(file_filter))
        import tkinter as tk
        from tkinter import filedialog
        # 创建一个Tkinter 本地 文件选择窗口
        try:
            # 创建Tkinter根窗口并隐藏
            root = tk.Tk()
            # 顶层
            root.attributes('-topmost', 'true')
            root.withdraw()  # 隐藏主窗口

            # 打开文件选择对话框
            file_path = filedialog.askopenfilename(
                parent=root,
                title=title,
                filetypes= file_filter # 可根据需求调整文件类型过滤
                #filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
            )

            # 如果用户取消选择，返回None
            if not file_path:
                QuikeUI.get_app().log.info("用户取消了文件选择操作")
                return ""

            return file_path  # 返回用户选择的文件路径

        except ImportError:
            QuikeUI.get_app().log.error("错误：未安装Tkinter模块，请确保系统支持Tkinter")
            return ""
        except Exception as e:
            QuikeUI.get_app().log.error(f"发生未知错误：{e}")
            return ""

    @staticmethod
    def open_local_file(title="选择文件", file_filter = [("所有文件", "*.*")]  ):
        import tkinter as tk
        from tkinter import filedialog
        
        
        
    @staticmethod
    def set_app(app):
       global static_app
       static_app = app



    @staticmethod
    def get_log():
        return QuikeUI.get_app().log

    @staticmethod
    def get_app():
        global static_app
        return static_app
    @staticmethod
    def close_application():
        QuikeUI.get_app().log.info("=============>close_application")
        QuikeUI.get_app().log.info("=============>window.__class__>"+str(QuikeUI.get_app().browser_thread.__class__))

        if QuikeUI.get_app().browser_type == "command":
            if QuickConfig.FLASKWEBGUI_BROWSER_PROCESS is not None:
                # 关闭浏览器进程
                QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.terminate()
        elif QuikeUI.get_app().browser_type == "webview":
            if QuikeUI.get_app().browser_thread is not None:
                # 关闭浏览器进程
                QuikeUI.get_app().browser_thread.destroy()

        # if QuikeUI.get_app().stray_icon is not None:
        #     # 停止托盘图标运行
        #     QuikeUI.get_app().stray_icon.stop()

        # 关闭后台进程
        QuickConfig.kill_port(QuickConfig.FLASKWEBGUI_USED_PORT)
