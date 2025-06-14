# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


import os
import sys

sys.path.insert(0, os.path.abspath('../../src'))  # 注意：不是 src/pyquickwebgui

project = 'pyquickwebgui'
copyright = '2025, lx'
author = 'lx'
release = '0.0.5'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',     # 自动生成文档的核心扩展
    'sphinx.ext.viewcode',    # 添加源码链接
    'sphinx.ext.napoleon',    # 支持 Google/NumPy 风格 docstring
]

templates_path = ['_templates']
exclude_patterns = []

language = 'zh_CN'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'sphinx_rtd_theme'


# -- Options for Autodoc ----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

autodoc_default_options = {
    'members': True,          # 自动包含所有成员（属性、方法等）
    'undoc-members': False,   # 不包括没有文档字符串的成员
    'private-members': False, # 不包括私有成员（如 _xxx）
    'special-members': False, # 不包括特殊方法（如 __init__）
    'inherited-members': True,# 包括继承的方法
    'show-inheritance': True, # 显示继承关系
    'member-order': 'bysource', # 按源码顺序显示成员
}