# 1. 项目基础信息
project = 'PhyMLP'
copyright = 'NSH'
author = 'nsh'
release = '1.0.0'          # 当前版本号，会显示在左下角
language = 'zh_CN'         # 中文界面（RTD 主题按钮等会显示中文）

# 2. 固定写法：让 Sphinx 找到你自己的扩展目录（如有）
import os
import sys
sys.path.append(os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('G:\mlp-train\mtp-sofeware-connection\sphins-phymlp'))  # 假设docs目录在项目根目录下
sys.path.insert(0, os.path.abspath('G:\mlp-train\mtp-sofeware-connection\sphins-phymlp\phymlp'))  # 添加包目录到路径

# 3. 加载最小扩展集合
#    - sphinx.ext.autodoc：自动提取 docstring
#    - sphinx.ext.viewcode：生成「[source]」链接
#    - sphinx.ext.githubpages：生成 .nojekyll，方便 GitHub Pages
#    'sphinx.ext.napoleon',   # 开启 Google / NumPy 风格解析

# 显示更深的目录树
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'titles_only': False
}

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.napoleon',
]

# 4. 源文件后缀与主入口
source_suffix = '.rst'
master_doc = 'index'       # 首页文件 index.rst

# 5. 主题设置
html_theme = 'sphinx_rtd_theme'