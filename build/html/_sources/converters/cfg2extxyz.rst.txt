CFG到EXTXYZ格式转换器
===================

本模块用于将MTP结构CFG文件转换为EXTXYZ格式，支持能量、应力等物理信息的提取和转换。

模块概述
--------

该模块提供了一组函数，用于：

1. 解析包含多个CFG结构的文件
2. 提取原子结构、晶格、能量、应力等信息
3. 将解析的数据写入EXTXYZ格式文件
4. 支持原子类型到元素符号的映射

主要函数说明
------------

parse_cfg_file(file_path)
^^^^^^^^^^^^^^^^^^^^^^^^^

解析包含多个CFG结构的文件。

**参数：**
- ``file_path``: CFG文件路径（字符串）

**返回：**
- 包含所有配置信息的字典列表，每个字典代表一个结构

**返回值结构：**
- ``size``: 原子数量（整数）
- ``supercell``: 超胞晶格向量（3×3浮点数列表）
- ``volume``: 晶胞体积（浮点数）
- ``atoms``: 原子信息列表（字典列表）
- ``energy``: 能量值（浮点数，可选）
- ``stress``: 应力张量（字典，可选）

**作用：**
读取CFG格式文件，提取其中的结构信息，支持容错处理和数据验证。

write_extxyz(configs, output_file, type_map=None, float_fmt=".9f")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

将解析后的配置写入EXTXYZ文件。

**参数：**
- ``configs``: parse_cfg_file()返回的配置列表
- ``output_file``: 输出文件路径（字符串）
- ``type_map``: 原子类型到元素符号的映射字典（可选）
- ``float_fmt``: 浮点数格式字符串（默认".9f"）

**返回：**
- 无返回值

**作用：**
将解析的CFG结构数据写入标准的EXTXYZ格式文件，包含晶格、能量、应力等物理量。

原子类型映射（type_map）
----------------------

``type_map`` 参数用于将CFG中的整数原子类型映射为元素符号：

.. code-block:: python

    # 示例：将类型0映射为Ni，类型1映射为Cr
    type_map = {0: 'Ni', 1: 'Cr', 2: 'Fe'}

如果没有提供type_map，模块会：
1. 从命令行参数自动创建映射
2. 或使用默认映射 ``{0: 'X'}``
3. 或自动检测原子类型并使用 ``Elem0``, ``Elem1`` 等默认名称

输入文件格式（CFG）
------------------

CFG文件格式示例：

.. code-block:: text

    BEGIN_CFG
    Size
    2
    Supercell
    1.0 0.0 0.0
    0.0 1.0 0.0
    0.0 0.0 1.0
    AtomData: id type cartes_x cartes_y cartes_z fx fy fz
    1 0 0.0 0.0 0.0 0.0 0.0 0.0
    2 0 0.5 0.5 0.5 0.0 0.0 0.0
    Energy
    -10.5
    PlusStress
    0.0 0.0 0.0 0.0 0.0 0.0
    END_CFG

支持的关键字：
- ``BEGIN_CFG`` / ``END_CFG``: 结构块标记
- ``Size``: 原子数量
- ``Supercell``: 晶格向量
- ``AtomData``: 原子坐标和力
- ``Energy``: 体系能量
- ``PlusStress``: 应力张量

输出文件格式（EXTXYZ）
---------------------

EXTXYZ格式示例：

.. code-block:: text

    2
    Lattice="1.000000000 0.000000000 0.000000000 0.000000000 1.000000000 0.000000000 0.000000000 0.000000000 1.000000000" Properties=species:S:1:pos:R:3:forces:R:3 stress="0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000 0.000000000" free_energy=-10.500000000 energy=-10.500000000 pbc="T T T"
    Ni    0.000000000    0.000000000    0.000000000    0.000000000    0.000000000    0.000000000
    Ni    0.500000000    0.500000000    0.500000000    0.000000000    0.000000000    0.000000000

使用示例
--------

.. code-block:: bash

    # 命令行使用
    python cfg2extxyz.py train.cfg Ni Cr Fe

    # Python代码中使用
    from cfg2extxyz import parse_cfg_file, write_extxyz

    # 解析CFG文件
    configs = parse_cfg_file("train.cfg")

    # 设置原子类型映射
    type_map = {0: 'Ni', 1: 'Cr', 2: 'Fe'}

    # 写入EXTXYZ文件
    write_extxyz(configs, "output.extxyz", type_map=type_map)

错误处理
--------

模块包含完善的错误处理和日志记录：
- 文件不存在时会抛出FileNotFoundError
- 格式错误时会记录警告并尝试继续处理
- 缺少必要信息时会使用默认值或跳过该结构
- 所有操作都有详细的日志输出

注意事项
--------

1. CFG文件中每个结构必须用BEGIN_CFG和END_CFG包围
2. 原子类型编号从0开始，需要正确映射到元素符号
3. 如果没有力信息，会使用零向量作为默认值
4. 浮点数精度可通过float_fmt参数控制