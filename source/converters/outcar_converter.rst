OUTCAR到EXTXYZ格式转换器
======================

本模块用于从VASP的OUTCAR文件中提取结构信息并转换为EXTXYZ格式。

模块概述
--------

该模块提供了一个主要函数，用于：

1. 从VASP的OUTCAR文件中读取所有结构信息
2. 按指定步长提取结构帧
3. 将提取的结构保存为EXTXYZ格式文件

主要函数说明
------------

extract_structures_from_outcar(outcar_file, output_file, step=1)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从OUTCAR文件中提取结构并保存为extxyz文件。

**参数：**
- ``outcar_file``: OUTCAR文件路径（字符串）
- ``output_file``: 输出的extxyz文件路径（字符串）
- ``step``: 提取结构的步长（整数，默认1）

**返回：**
- 无返回值

**作用：**
读取OUTCAR文件中记录的所有结构帧，按指定步长间隔提取结构，并以EXTXYZ格式保存到输出文件中。

输入文件（OUTCAR）
-----------------

VASP OUTCAR文件通常包含：
- 原子坐标（包括离子步的坐标变化）
- 晶格参数
- 能量信息
- 力信息
- 应力信息

输出文件（EXTXYZ）
-----------------

生成的EXTXYZ文件包含：
- 原子种类和位置
- 晶格向量
- 能量（如果OUTCAR中包含）
- 原子受力
- 晶胞应力

使用示例
--------

**命令行使用：**

.. code-block:: bash

    # 基本用法：提取所有结构
    python outcar_converter.py OUTCAR

    # 指定输出文件
    python outcar_converter.py OUTCAR output.extxyz

    # 指定步长：每10步提取一个结构
    python outcar_converter.py OUTCAR output.extxyz 10

**Python代码中使用：**

.. code-block:: python

    from outcar_converter import extract_structures_from_outcar

    # 提取所有结构
    extract_structures_from_outcar("OUTCAR", "all_structures.extxyz")

    # 每5步提取一个结构
    extract_structures_from_outcar("OUTCAR", "sparse_structures.extxyz", step=5)

注意事项
--------

1. 需要安装ASE（Atomic Simulation Environment）库
2. 如果输出文件已存在，会被覆盖
3. 步长参数step=1表示提取所有结构，step=10表示每10个结构提取一个
4. 函数使用ASE的read函数读取OUTCAR，需要OUTCAR格式正确
5. 生成的EXTXYZ文件可以用VESTA、Ovito等软件查看

错误处理
--------

- 如果OUTCAR文件不存在，会抛出FileNotFoundError
- 如果OUTCAR格式不正确，会抛出ValueError
- 文件操作失败会显示相应的错误信息