# -*- coding: utf-8 -*-
'''
@File    :   QuickConfig.py
@Time    :   2025/06/10 16:46:15
@Author  :   LX
@Version :   1.0.0
@Desc    :   配置类
'''


from typing import Any, Callable, Dict, List, Union
import webbrowser
from enum import Enum
import platform
import socketserver
import psutil
import signal
import os

from ..servers.BaseDefaultServer import BaseDefaultServer
from ..servers.DefaultServerDjango import DefaultServerDjango
from ..servers.DefaultServerFastApi import DefaultServerFastApi
from ..servers.DefaultServerFlask import DefaultServerFlask
from ..servers.DefaultServerFlaskSocketIO import DefaultServerFlaskSocketIO
from ..servers.DefaultServerWebpy import DefaultServerWebpy


from ..browser.BaseBrowser import BaseBrowser
from ..browser.CommandBrowser import CommandBrowser
from ..browser.TauriBrowser import TauriBrowser
from ..browser.WebviewBrowser import WebviewBrowser



class Browser_type_enum(Enum):
    """_summary_
    浏览器类型枚举
    :param Enum: _description_
    :type Enum: _type_
    """
    # 命令行启动浏览器
    COMMAND = "command"
    # webview 启动浏览器
    WEBVIEW = "webview"
    # tauri 启动浏览器
    TAURI = "tauri"

class Server_enum(Enum):
    """_summary_
    服务器枚举
    :param Enum: _description_
    :type Enum: _type_
    """
    #"fastapi"
    FASTAPI =  "fastapi"
    FLASK =  "flask"
    FLASK_SOCKETIO = "flask_socketio"
    DJANGO = "django"
    WEBPY = "webpy"



class QuickConfig:

    # 版本号
    version = "0.0.5"

    FLASKWEBGUI_USED_PORT = None
    FLASKWEBGUI_BROWSER_PROCESS = None

    # 默认浏览器
    DEFAULT_BROWSER = webbrowser.get().name
    # 操作系统
    OPERATING_SYSTEM = platform.system().lower()

    PY = "python3" if OPERATING_SYSTEM in ["linux", "darwin"] else "python"

    ROOTPLUGINS_DIR = "rootplugins"

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

    # 服务 调度器
    webserver_dispacher: Dict[str, BaseDefaultServer] = {
        Server_enum.FASTAPI.value : DefaultServerFastApi,
        Server_enum.FLASK.value : DefaultServerFlask,
        Server_enum.FLASK_SOCKETIO.value : DefaultServerFlaskSocketIO,
        Server_enum.DJANGO.value : DefaultServerDjango,
        Server_enum.WEBPY.value : DefaultServerWebpy,
    }

    # 浏览器 调度器
    browser_dispacher: Dict[str, BaseBrowser] = {
        Browser_type_enum.COMMAND.value : CommandBrowser,
        Browser_type_enum.WEBVIEW.value : WebviewBrowser,
        Browser_type_enum.TAURI.value : TauriBrowser,
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
    @staticmethod
    def get_browser_command(app):
        # https://peter.sh/experiments/chromium-command-line-switches/
        # https://www.cnblogs.com/Ghsoft/p/18359891

        flags = [
            app.browser_path,

            # 用户数据（设置、缓存等）的位置
            f"--user-data-dir={app.profile_dir}",
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

        if app.debug:
            flags.extend(["--auto-open-devtools-for-tabs"])

        # if app.frameless:
        #     flags.extend(["--headless=new"])

        # if app.frameless:
        #     # 启动时不建立窗口
        #     flags.extend(["--disable-desktop-notifications"])


        if app.width and app.height and app.app_mode:
            flags.extend([f"--window-size={app.width},{app.height}"])
        elif app.fullscreen:
            flags.extend(["--start-maximized"])

        if app.extra_flags:
            flags = flags + app.extra_flags

        if app.app_mode:
            flags.append(f"--app={app.url}")
        else:
            flags.extend(["--guest", app.url])

        return flags