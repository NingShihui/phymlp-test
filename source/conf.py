# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- 添加Python路径以便识别phymlp模块 --
sys.path.insert(0, os.path.abspath('../..'))  # 假设docs在phymlp/docs目录下

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'PhyMLP Kit'
copyright = '2025, Hunan University, PhyMLP Development Team'
author = 'Shihui Ning, Yiqun Guo, Yangchun Chen, Bowen huang, Shifang Xiao, Wangyu Hu et al.'
release = '2.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',        # 自动从代码生成文档
    'sphinx.ext.napoleon',       # 支持Google/Numpy风格docstrings
    'sphinx.ext.viewcode',       # 添加源代码链接
    'sphinx.ext.autosummary',    # 生成自动摘要
    'sphinx.ext.intersphinx',    # 链接到其他项目文档
    'sphinx.ext.todo',           # 支持TODO列表
]

# Napoleon设置
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True

# 自动生成summary
autosummary_generate = True
autoclass_content = 'both'  # 显示类和__init__的文档

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# 支持中文
language = 'zh_CN'
locale_dirs = ['locale/']  # 如果有翻译文件

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# 使用sphinx_rtd_theme
html_theme = 'sphinx_rtd_theme'

# 主题选项
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'includehidden': True,
    'titles_only': False,
    'logo_only': False,
}


# -- 扩展配置 ---------------------------------------------------------

# 配置intersphinx映射（如果需要链接到其他项目）
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# 显示TODO
todo_include_todos = True