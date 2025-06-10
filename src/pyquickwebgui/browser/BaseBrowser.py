# -*- coding: utf-8 -*-
'''
@File    :   BaseDefaultServer.py
@Time    :   2025/06/10 10:36:03
@Author  :   LX
@Version :   1.0.0
@Desc    :   None
'''
from typing import  Callable




class BaseBrowser:
    view: Callable
    get_view_kwargs: Callable
