工具函数模块
===========

本模块提供了一系列通用的工具函数，用于支持其他模块的操作。

模块概述
--------

该模块包含了一组辅助函数，主要用于：

1. 文件和目录操作
2. 化学系统和元素组合处理
3. 路径和文件安全检查
4. 配置验证

主要函数说明
------------

mkdir_output_load(path)
^^^^^^^^^^^^^^^^^^^^^^^

创建输出目录，如果已存在则清空。

**参数：**
- ``path``: 目录路径

**返回：**
- 无返回值

**作用：**
确保输出目录存在且为空，避免文件残留影响后续处理。

chemsys_comb(elements)
^^^^^^^^^^^^^^^^^^^^^^

生成所有可能的元素组合。

**参数：**
- ``elements``: 元素符号列表，如 ['Ba', 'Ti', 'O']

**返回：**
- 所有可能的元素组合字符串列表，如 ['Ba', 'Ti', 'O', 'Ba-Ti', 'Ba-O', 'Ti-O', 'Ba-Ti-O']

**作用：**
用于化学系统组合生成，便于搜索多种元素组合的材料。

get_formula_from_filename(filename)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从文件名中提取化学式。

**参数：**
- ``filename``: 文件名，如 'BaTiO3-mp-2998.vasp'

**返回：**
- 提取的化学式字符串，如 'BaTiO3'

**作用：**
从包含Material Project ID的文件名中提取纯化学式部分。

safe_copy(src, dst)
^^^^^^^^^^^^^^^^^^^

安全复制文件。

**参数：**
- ``src``: 源文件路径
- ``dst``: 目标文件路径

**返回：**
- 布尔值，表示复制是否成功

**作用：**
封装文件复制操作，提供错误处理和日志记录。

check_potcar_availability(config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

检查POTCAR配置是否可用。

**参数：**
- ``config``: 配置字典

**返回：**
- 布尔值，表示POTCAR配置是否可用

**作用：**
验证POTCAR生成方法的相关配置和依赖是否正常。

safe_path_join(*args)
^^^^^^^^^^^^^^^^^^^^^

安全的路径连接，处理混合的路径分隔符。

**参数：**
- ``*args``: 路径组成部分

**返回：**
- 标准化后的完整路径字符串

**作用：**
处理不同操作系统和用户输入的路径分隔符问题，确保路径连接正确。

check_file_exists(file_path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

检查文件是否存在，提供详细的错误信息。

**参数：**
- ``file_path``: 文件路径

**返回：**
- 布尔值，表示文件是否存在

**作用：**
增强的文件存在性检查，提供详细的诊断信息帮助调试。

使用示例
--------

.. code-block:: python

    from utils import *

    # 创建目录
    mkdir_output_load('./output')

    # 生成元素组合
    elements = ['Ba', 'Ti', 'O']
    combos = chemsys_comb(elements)  # ['Ba', 'Ti', 'O', 'Ba-Ti', ...]

    # 提取化学式
    formula = get_formula_from_filename('BaTiO3-mp-2998.vasp')  # 'BaTiO3'

    # 安全复制
    success = safe_copy('input.vasp', 'output/POSCAR')

    # 检查配置
    potcar_ok = check_potcar_availability(config)

    # 路径操作
    full_path = safe_path_join('parent', 'subdir', 'file.txt')

    # 文件检查
    exists = check_file_exists('POSCAR')

注意事项
--------

1. ``mkdir_output_load`` 会清空已存在的目录，使用时需谨慎
2. ``chemsys_comb`` 的组合数量随元素数量指数增长，需控制元素数量
3. ``safe_path_join`` 主要解决Windows/Linux路径分隔符兼容问题
4. ``check_file_exists`` 主要用于调试，提供详细的文件系统信息