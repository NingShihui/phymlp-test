extxyz数据集生成模块
====================

本模块用于从VASP计算结果和Birch-Murnaghan拟合结果生成extxyz格式数据集。

模块概述
--------

该模块提供了一组函数，用于：

1. 从VASP的OUTCAR文件中提取结构信息
2. 从Birch-Murnaghan拟合结果生成扩展结构
3. 从fit_a_P.data数据生成晶格常数-压力对应结构
4. 合并不同来源的结构数据

主要函数说明
------------

find_outcar_files(search_dir, recursive=True)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在目录树中查找所有的OUTCAR文件。

**参数：**
- ``search_dir``: 搜索目录路径
- ``recursive``: 是否递归搜索子目录（默认True）

**返回：**
- OUTCAR文件路径列表

extract_structures_from_outcar(outcar_file, output_file, step=10)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从OUTCAR文件中提取结构并保存为extxyz格式。

**参数：**
- ``outcar_file``: OUTCAR文件路径
- ``output_file``: 输出extxyz文件路径
- ``step``: 提取步长（默认10，即每10个结构提取一个）

**返回：**
- 提取的结构总数

generate_vasp_extxyz(config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从VASP计算结果生成extxyz文件。

**参数：**
- ``config``: 配置字典，包含VASP相关设置

**返回：**
- 提取的结构总数

load_birch_murnaghan_fitting_results(bm_dir, recursive=False)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

加载Birch-Murnaghan拟合结果。

**参数：**
- ``bm_dir``: Birch-Murnaghan拟合目录
- ``recursive``: 是否递归搜索子目录（默认False）

**返回：**
- 拟合结果信息字典

extract_structures_from_outcar_scale(outcar_scale_dir, output_file, step=10)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从OUTCAR_scale目录中的OUTCAR文件提取结构。

**参数：**
- ``outcar_scale_dir``: OUTCAR_scale目录路径
- ``output_file``: 输出文件路径
- ``step``: 提取步长（默认10）

**返回：**
- 提取的结构总数

find_reference_structure(outcar_scale_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

在OUTCAR_scale目录中查找参考结构。

**参数：**
- ``outcar_scale_dir``: OUTCAR_scale目录路径

**返回：**
- 参考原子结构（ASE Atoms对象）

filter_data_by_pressure(data_file, pressure_range)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

根据压力范围筛选数据。

**参数：**
- ``data_file``: 数据文件路径
- ``pressure_range``: 压力范围 [最小值, 最大值]

**返回：**
- 筛选后的数据（DataFrame）

calculate_pressure_from_birch_murnaghan(params, volume)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

根据Birch-Murnaghan方程计算压力。

**参数：**
- ``params``: [E0, V0, B0, B1] 拟合参数
- ``volume``: 体积

**返回：**
- 压力值（GPa）

generate_structures_from_fitting_curve(reference_atoms, fitted_data, output_file, structure_name, n_structures=50, pressure_range=None, original_data=None, scaling_factors_range=None, bm_params=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

根据拟合曲线数据生成扩展结构。

**参数：**
- ``reference_atoms``: 参考原子结构
- ``fitted_data``: 拟合数据DataFrame
- ``output_file``: 输出文件路径
- ``structure_name``: 结构名称
- ``n_structures``: 生成的结构数量（默认50）
- ``pressure_range``: 压力范围筛选
- ``original_data``: 原始数据用于压力筛选
- ``scaling_factors_range``: 缩放因子范围
- ``bm_params``: Birch-Murnaghan拟合参数

**返回：**
- 生成的结构总数

generate_birch_murnaghan_extxyz(config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从Birch-Murnaghan拟合结果生成extxyz文件。

**参数：**
- ``config``: 配置字典

**返回：**
- 生成的结构总数

load_fit_a_P_data(fit_a_P_file)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

加载fit_a_P.data文件数据。

**参数：**
- ``fit_a_P_file``: fit_a_P.data文件路径

**返回：**
- 包含晶格常数、缩放因子和压力的数据（DataFrame）

gpa_to_ev_per_ang3(pressure_gpa)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

将压力从GPa转换为eV/Å³。

**参数：**
- ``pressure_gpa``: 压力值（GPa）

**返回：**
- 压力值（eV/Å³）

generate_structures_from_fit_a_P(config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

根据fit_a_P.data数据生成extxyz结构。

**参数：**
- ``config``: 配置字典

**返回：**
- 生成的结构总数

merge_extxyz_files(config)
^^^^^^^^^^^^^^^^^^^^^^^^^^

合并VASP、Birch-Murnaghan和fit_a_P的extxyz文件。

**参数：**
- ``config``: 配置字典

**返回：**
- 合并后的结构总数

generate_extxyz_dataset(config_path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

生成完整的Extxyz数据集。

**参数：**
- ``config_path``: 配置文件路径

**返回：**
- 合并后的结构总数

generate_extxyz_from_config(config_path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

从配置文件生成extxyz数据集的入口函数。

**参数：**
- ``config_path``: 配置文件路径

**返回：**
- 合并后的结构总数

使用示例
--------

.. code-block:: bash

    # 直接运行脚本
    python generate_extxyz_dataset.py --input_file input.yaml

    # 或在Python代码中调用
    from generate_extxyz_dataset import generate_extxyz_from_config
    total_structures = generate_extxyz_from_config('input.yaml')

配置文件说明
-----------

需要提供YAML格式的配置文件，包含以下主要部分：

- ``paths``: 路径配置
- ``vasp``: VASP提取配置
- ``extxyz_generation``: extxyz生成配置
- ``birch_murnaghan_fitting``: Birch-Murnaghan拟合配置

输出文件
--------

模块将生成以下文件：

1. ``Extxyz_set/vasp/vasp.extxyz`` - VASP提取的结构
2. ``Extxyz_set/birch_murnaghan_fitting/birch.extxyz`` - Birch-Murnaghan生成的结构
3. ``Extxyz_set/fit_a_P/fit_a_P.extxyz`` - fit_a_P生成的结构
4. ``Extxyz_set/merged_dataset.extxyz`` - 合并后的完整数据集