"""
插件名称:

插件描述:


插件初始化自动导入包:

try:
    import requests
except ImportError:
    import os
    os.system('pip install requests')
    import requests

"""