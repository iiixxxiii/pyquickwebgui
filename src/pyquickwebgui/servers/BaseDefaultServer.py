# -*- coding: utf-8 -*-
'''
@File    :   BaseDefaultServer.py
@Time    :   2025/06/10 10:36:03
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''
from typing import  Callable




class BaseDefaultServer:
    server: Callable
    get_server_kwargs: Callable
