处理形变计算结果模块
===================

本模块用于对形变计算结果目录进行分类和VASP数据提取，生成统一格式的数据文件。

模块概述
--------

该模块提供了一组函数，用于：

1. 对形变计算目录进行自动分类整理
2. 创建按基础结构和缩放系数分类的目录结构
3. 从VASP计算结果文件中提取关键物理量
4. 生成统一格式的数据文件用于后续分析

主要函数说明
------------

classify_deform_directories(root_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

对形变计算目录进行分类。

**参数：**
- ``root_dir``: 包含形变计算结果的根目录路径

**返回：**
- 字典，分类后的目录结构：``{base_name: [dir_paths]}``

**作用：**
识别形变目录模式（如 ``structure_0.8``, ``structure_1.0``），按基础名称进行分组。

create_classified_structure(root_dir, classified_dict)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建分类后的目录结构。

**参数：**
- ``root_dir``: 根目录路径
- ``classified_dict``: 分类后的目录字典

**返回：**
- 无返回值

**作用：**
创建新的目录结构，将形变目录按基础名称和缩放系数重新组织。

extract_vasp_data(directory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从VASP计算结果中提取数据。

**参数：**
- ``directory``: 包含VASP计算结果的目录路径

**返回：**
- 字典，包含提取的数据：``{'a', 'V', 'E', 'P'}``

**作用：**
从POSCAR、OSZICAR、OUTCAR文件中提取晶格常数、体积、能量和压力数据。

process_all_deform_results(root_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

处理所有形变计算结果。

**参数：**
- ``root_dir``: 根目录路径

**返回：**
- 无返回值

**作用：**
整合所有处理步骤：目录分类、结构重组、数据提取，生成最终的数据文件。

输出文件结构
-----------

处理后生成的目录结构：

::

    root_dir/
    ├── base_structure_1/           # 基础结构目录
    │   ├── scale_0.8/              # 缩放系数0.8
    │   ├── scale_0.9/              # 缩放系数0.9
    │   ├── scale_1.0/              # 缩放系数1.0
    │   └── a_V_E_P.txt             # 提取的数据文件
    ├── base_structure_2/
    └── ...

数据文件格式
-----------

生成的数据文件 ``a_V_E_P.txt`` 格式：

.. code-block:: text

    a     V     E     P
    3.905     60.245     -27.6834     0.000
    4.010     64.120     -27.6521     0.125
    4.115     68.345     -27.6012     0.275

列说明：
- ``a``: 晶格常数（Å）
- ``V``: 单元格体积（Å³）
- ``E``: 能量（eV）
- ``P``: 压力（GPa）

使用示例
--------

.. code-block:: bash

    # 直接运行脚本
    python process_deform_results.py --root_dir ./deform_calculations

    # 或在Python代码中调用
    from process_deform_results import process_all_deform_results
    process_all_deform_results('./deform_calculations')

注意事项
--------

1. 原始目录命名需符合模式：``basename_scalefactor``（如 ``BaTiO3_0.95``）
2. 目录中需要包含完整的VASP计算结果文件（POSCAR、OSZICAR、OUTCAR）
3. 数据提取可能受VASP输出格式影响，需要适当调整正则表达式
4. 处理过程会移动原始目录，建议先备份数据