# -*- coding: utf-8 -*-
'''
@File    :   pyquickwebgui.py
@Time    :   2025/06/10 10:51:30
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''

# 标准库
import os, sys
import shutil
import subprocess
import tempfile
import time
import uuid
import multiprocessing
from multiprocessing import Process
from threading import Thread

# 第三方库
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Union

import importlib.util

from .rootplugins.BasePlugin import BasePlugin
from .servers.BaseDefaultServer import BaseDefaultServer
from .browser.BaseBrowser import BaseBrowser
from .config.QuickConfig import (
    Server_enum,
    Browser_type_enum,
    QuickConfig
)

# 静态QuikeUI对象
static_app = None


@dataclass
class QuikeUI:
    """
    创建一个 QuikeUI 对象，用于启动 Web GUI 应用程序。

    Attributes:
        server (Union[str, Server_enum, Callable[[Any], None]]): 服务器类型或可调用对象，默认使用 FastAPI。
        server_kwargs (dict): 服务器配置参数。
        app (Any): Web 应用实例。
        port (int): 服务器端口。
        width (int): 窗口宽度，默认为 800px。
        height (int): 窗口高度，默认为 600px。
        fullscreen (bool): 是否全屏显示，默认为 False。
        on_startup (Callable): 启动时执行的函数。
        on_shutdown (Callable): 关闭时执行的函数。
        extra_flags (List[str]): 浏览器额外标志。
        browser_path (str): 浏览器路径。
        browser_command (List[str]): 浏览器启动命令。
        socketio (Any): Socket.IO 实例。
        profile_dir_prefix (str): 浏览器临时目录前缀。
        app_mode (bool): 是否以应用模式运行。
        browser_pid (int): 浏览器进程 ID。
        base_path (str): 基础路径。
        frameless (bool): 是否无边框窗口，默认为 False。
        debug (bool): 是否启用调试模式。
        x (int): 窗口 x 坐标，默认居中。
        y (int): 窗口 y 坐标，默认居中。
        only_webserver (bool): 是否仅作为 Web 服务运行。
        show_browser (bool): 是否显示浏览器界面，默认为 True。
        browser_type (Union[str, Browser_type_enum]): 浏览器类型，默认为 command。
        stray (dict): 托盘图标配置信息。
        log (object): 日志记录器对象。
        log_level (str): 日志级别，默认为 info。
        reload (bool): 是否启用热重载。
        ss (bool): 是否启用热重载。
    """

    server: Union[str, Server_enum, Callable[[Any], None]] = Server_enum.FASTAPI.value
    server_kwargs: dict = None
    app: Any = None
    port: int = None
    width: int = 800
    height: int = 600
    fullscreen: bool = False
    on_startup: Callable = None
    on_shutdown: Callable = None
    extra_flags: List[str] = None
    browser_path: str = None
    browser_command: List[str] = None
    socketio: Any = None
    profile_dir_prefix: str = "flaskwebgui"
    app_mode: bool = True
    browser_pid: int = None
    base_path: str = None
    frameless: bool = False
    debug: bool = False
    x: int = 0
    y: int = 0
    only_webserver: bool = False
    show_browser: bool = True
    browser_type: Union[str, Browser_type_enum] = Browser_type_enum.COMMAND.value
    stray: dict = None
    log: object = None
    log_level: str = "info"
    reload: bool = False
    ss: bool = False
    def __post_init__(self):
        """
        初始化后处理逻辑：
        - 枚举转字符串；
        - 加载插件；
        - 设置端口；
        - 生成浏览器 URL；
        - 设置全局当前应用。
        """
        # 枚举转换字符串值
        if isinstance(self.server, Server_enum):
            self.server = self.server.value
        if isinstance(self.browser_type, Browser_type_enum):
            self.browser_type = self.browser_type.value

        self.run_rootplugins()

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
                reload=self.reload,
                log_level=self.log_level,
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
        self.browser_command = self.browser_command or QuickConfig.get_browser_command(self)

        QuikeUI.set_app(self)

    def create_webview_window(self, server_kwargs):
        """
        创建一个 webview 窗口。

        Args:
            server_kwargs (dict): 服务器启动参数。
        """
        import webview
        from contextlib import redirect_stdout
        from io import StringIO

        stream = StringIO()
        with redirect_stdout(stream):
            self.browser_thread = webview.create_window('', self.url,
                                                        width=self.width,
                                                        height=self.height,
                                                        fullscreen=self.fullscreen)
            webview.start(debug=self.debug, gui='cef')

    def start_browser(self, server_process: Union[Thread, Process]):
        """
        启动浏览器进程。

        Args:
            server_process (Union[Thread, Process]): 服务器进程或线程对象。
        """
        self.log.info("==========>start_browser Quick version:" + QuickConfig.version)
        self.log.info("Command:{}".format(" ".join(self.browser_command)))

        if QuickConfig.OPERATING_SYSTEM == "darwin":
            multiprocessing.set_start_method("fork")

        if self.browser_type == "command":
            QuickConfig.FLASKWEBGUI_BROWSER_PROCESS = subprocess.Popen(self.browser_command)
            self.browser_pid = QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.pid
            QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.wait()

        if self.browser_path is None:
            while self.__keyboard_interrupt is False:
                time.sleep(1)

        if isinstance(server_process, Process):
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)

            if self.stray is False:
                print("server_process.kill.")
                server_process.kill()
        else:
            if self.on_shutdown is not None:
                self.on_shutdown()
            self.browser_pid = None
            shutil.rmtree(self.profile_dir, ignore_errors=True)

            if self.stray is False:
                print("QuickConfig.kill_port.")
                QuickConfig.kill_port(self.port)

    def load_rootplugins(self):
        """
        加载系统根插件。

        Returns:
            List[Any]: 插件实例列表。
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        rootplugins = []
        ROOTPLUGINS_DIR = os.path.join(current_dir, QuickConfig.ROOTPLUGINS_DIR)
        sys.path.append(ROOTPLUGINS_DIR)
        for filename in os.listdir(ROOTPLUGINS_DIR):
            if filename.endswith(".py"):
                path = os.path.join(ROOTPLUGINS_DIR, filename)
                name = filename[:-3]
                spec = importlib.util.spec_from_file_location(name, path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for item_name in dir(module):
                    if str(item_name).lower().find(QuickConfig.PLUGIN_CLASS_NAME) > -1 and \
                            str(item_name).lower().find(QuickConfig.BASE_PLUGIN_CLASS_NAME) == -1:
                        item = getattr(module, item_name)
                        rootplugins.append(item())
        return rootplugins

    def run_rootplugins(self):
        """
        运行加载的系统根插件。
        """
        self.rootplugins = self.load_rootplugins()
        for plugin in self.rootplugins:
            if hasattr(plugin, "run"):
                plugin.run(self)
            else:
                print(f"run_rootplugins :  {plugin.__name__} 没有定义 run()，跳过~")

    def load_plugins(self):
        """
        加载用户自定义插件。

        Returns:
            List[Any]: 插件类实例列表。
        """
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

    def run_plugins(self, class_name=""):
        """
        运行插件。

        Args:
            class_name (str): 要运行的插件类名。
        """
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

    def run(self, **kwargs):
        """
        启动整个 QuikeUI 应用。

        Args:
            kwargs (dict): 可选参数字典。

        Returns:
            QuikeUI: 当前 QuikeUI 实例。
        """

        # 浏览器进程
        self.browser_thread=None

        # 服务器进程
        self.server_process=None

        # 系统托盘 进程
        self.stray_process=None

        self.run_stray()
        self.run_server()
        self.run_browser()

        if self.on_startup is not None:
            self.on_startup()

        return self

    def run_stray(self):
        """
        启动系统托盘进程。
        """
        if self.stray and self.only_webserver is False:
            self.log.info("=============>启动 系统托盘进程")
            self.stray_process = Thread(target=self.start_stray, daemon=True, args=())
            try:
                if self.stray_process:
                    self.stray_process.start()
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")

    def run_server(self):
        """
        启动服务器进程。
        """
        self.log.info("=============>启动服务器进程")
        try:
            if QuickConfig.OPERATING_SYSTEM == "darwin":
                multiprocessing.set_start_method("fork")
                self.server_process = Process(target=self.server, kwargs=self.server_kwargs or {})
            else:
                self.server_process = Thread(target=self.server, kwargs=self.server_kwargs or {})

            self.server_process.start()
        except Exception as e:
            print("run_server error:", e)

    def run_browser(self):
        """
        启动浏览器进程。
        """
        if self.only_webserver:
            return
        self.log.info("=============>启动浏览器进程")
        if self.browser_type == "command":
            self.browser_thread = Thread(target=self.start_browser, args=(self.server_process,))
            try:
                if self.show_browser:
                    self.browser_thread.start()
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")
        elif self.browser_type == "webview":
            try:
                if self.show_browser:
                    self.create_webview_window(self.server_kwargs)
            except KeyboardInterrupt:
                self.__keyboard_interrupt = True
                print("Stopped")

    def start_stray(self):
        """
        创建并运行系统托盘图标。
        """
        import pystray
        from PIL import Image

        # 定义托盘图标
        if self.stray.get('icon') is None and len(self.stray.get('img', "")) > 0:
            self.stray['icon'] = Image.open(self.stray.get('img'))
        else:
            # 默认白色
            self.stray['icon'] = Image.new('RGB', (64, 64), 'white')

        # 定义托盘图标被点击时的响应函数
        def on_activate(icon, item):
            """处理托盘图标点击事件"""
            print("托盘图标被点击")

        def on_menu_click(icon, item):
            """处理菜单项点击事件"""
            if str(item) == "Show":
                print("显示功能被触发")
                self.run_browser()
            elif str(item) == "Exit":
                self.close_application()

        # 创建一个系统托盘对象
        default_menu = (
            pystray.MenuItem("Show", lambda icon, item: on_menu_click(icon, item)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", lambda icon, item: on_menu_click(icon, item)),
        )

        pystray.Icon(
            name=self.stray.get('name', ""),
            icon=self.stray.get('icon', ""),
            title=self.stray.get('title', ""),
            menu=self.stray.get('menu', default_menu),
            activate=self.stray.get('activate', on_activate)
        ).run()

    @staticmethod
    def get_log():
        """
        获取日志记录器。

        Returns:
            object: 日志对象。
        """
        return QuikeUI.get_app().log

    @staticmethod
    def open_local_file(title="选择文件", file_filter=[("所有文件", "*.*")]):
        """
        弹出本地文件选择对话框。

        Args:
            title (str): 文件选择窗口标题。
            file_filter (List[Tuple[str, str]]): 文件过滤规则列表。

        Returns:
            str: 用户选择的文件路径；若取消选择则返回空字符串。
        """
        print("open_local_file")
        QuikeUI.get_app().log.info("open_local_file")
        QuikeUI.get_app().log.info("open_local_file file_filter:{}".format(file_filter))
        import tkinter as tk
        from tkinter import filedialog
        try:
            root = tk.Tk()
            root.attributes('-topmost', 'true')
            root.withdraw()
            file_path = filedialog.askopenfilename(
                parent=root,
                title=title,
                filetypes=file_filter
            )
            if not file_path:
                QuikeUI.get_app().log.info("用户取消了文件选择操作")
                return ""
            return file_path
        except ImportError:
            QuikeUI.get_app().log.error("错误：未安装Tkinter模块，请确保系统支持Tkinter")
            return ""
        except Exception as e:
            QuikeUI.get_app().log.error(f"发生未知错误：{e}")
            return ""

    @staticmethod
    def set_app(app):
        """
        设置静态 QuikeUI 实例。

        Args:
            app (QuikeUI): QuikeUI 实例。
        """
        global static_app
        static_app = app

    @staticmethod
    def get_app():
        """
        获取当前 QuikeUI 实例。

        Returns:
            QuikeUI: QuikeUI 实例。
        """
        global static_app
        return static_app

    @staticmethod
    def close_application():
        """
        关闭应用程序：关闭浏览器、清理资源、终止后台进程。
        """
        QuikeUI.get_app().log.info("=============>close_application")
        QuikeUI.get_app().log.info("=============>window.__class__>"+str(QuikeUI.get_app().browser_thread.__class__))

        if QuikeUI.get_app().browser_type == "command":
            if QuickConfig.FLASKWEBGUI_BROWSER_PROCESS is not None:
                QuickConfig.FLASKWEBGUI_BROWSER_PROCESS.terminate()
        elif QuikeUI.get_app().browser_type == "webview":
            if QuikeUI.get_app().browser_thread is not None:
                QuikeUI.get_app().browser_thread.destroy()

        QuickConfig.kill_port(QuickConfig.FLASKWEBGUI_USED_PORT)