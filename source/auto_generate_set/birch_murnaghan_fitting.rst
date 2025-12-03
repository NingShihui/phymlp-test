.. _birch_murnaghan_module:

===============================
Birch-Murnaghan 拟合模块
===============================

.. contents:: 目录
   :depth: 2

概述
====

``birch_murnaghan_fitting.py`` 模块用于执行 Birch-Murnaghan 状态方程拟合，从 VASP 计算的能量-体积数据中提取材料的平衡性质参数。

输入配置
========

配置文件 (input.yaml)
--------------------

.. code-block:: yaml

   # 源数据配置
   birch_murnaghan_fitting:
     source:
       root_dir: "./vasp_calculations/deform/"  # 搜索a_V_E_P.txt的根目录
       search_recursive: true                   # 是否递归搜索子目录

     # 数据筛选条件
     data_filter:
       pressure_range: [-100, 100]     # 压力范围(GPa)
       energy_range: [-100, 10]        # 能量范围(eV)

     # 拟合参数配置
     fitting:
       initial_guess:
         E0: "auto"      # 平衡能量，auto表示自动选择最小值
         V0: "auto"      # 平衡体积，auto表示自动选择最小值对应体积
         B0: 100         # 初始体弹模量(GPa)
         B1: 4.0         # 初始体弹模量导数

     # 输出配置
     output:
       save_plot: true               # 是否保存拟合曲线图
       plot_format: "png"            # 图片格式
       plot_dpi: 300                 # 图片分辨率

输入数据文件
-----------

**a_V_E_P.txt 文件格式**：

.. code-block:: text

   a        V          E           P
   3.6000  46.656000  -24.567890   0.123456
   3.6050  46.860125  -24.568012  -0.034567
   3.6100  47.065000  -24.567945   0.056789

- **a**: 晶格常数 (Å)
- **V**: 体积 (Å³)
- **E**: 总能 (eV)
- **P**: 压力 (GPa)

主要函数
========

核心拟合函数
------------

.. py:function:: birch_murnaghan_eqn(params, V)

   计算 Birch-Murnaghan 方程值

   **输入**:
   - params: [E0, V0, B0, B1] 拟合参数
   - V: 体积数组 (Å³)

   **输出**:
   - E: 能量数组 (eV)

.. py:function:: perform_fitting(df, config)

   执行 Birch-Murnaghan 拟合

   **输入**:
   - df: DataFrame，包含V, E, P列的数据
   - config: 拟合配置字典

   **输出**:
   - result: SciPy least_squares 优化结果对象

数据处理函数
------------

.. py:function:: read_a_v_e_p_file(file_path)

   读取 a_V_E_P.txt 文件

   **输入**:
   - file_path: 数据文件路径

   **输出**:
   - df: pandas DataFrame，包含数值化的V, E, P数据

.. py:function:: filter_data(df, filter_config)

   根据条件筛选数据

   **输入**:
   - df: 原始数据DataFrame
   - filter_config: 筛选配置

   **输出**:
   - filtered_df: 筛选后的DataFrame

目录处理函数
------------

.. py:function:: find_a_v_e_p_files(root_dir, recursive=True)

   搜索 a_V_E_P.txt 文件

   **输入**:
   - root_dir: 搜索根目录
   - recursive: 是否递归搜索

   **输出**:
   - 列表: [(文件路径, 相对路径), ...]

.. py:function:: create_mirror_structure(source_files, bm_dir)

   创建镜像目录结构

   **输入**:
   - source_files: 找到的源文件列表
   - bm_dir: 目标BM目录

   **输出**:
   - dict: 结构信息字典

结果输出函数
------------

.. py:function:: save_fitting_results(result, df, output_dir, config, structure_name, source_path, reference_volume=None)

   保存拟合结果

   **输入**:
   - result: 拟合结果对象
   - df: 原始数据DataFrame
   - output_dir: 输出目录
   - config: 配置字典
   - structure_name: 结构名称
   - source_path: 源文件路径
   - reference_volume: 参考体积 (可选)

   **输出**:
   - dict: 拟合结果摘要

主工作流程
----------

.. py:function:: process_all_birch_murnaghan_fitting(config_path)

   批量处理所有拟合

   **输入**:
   - config_path: 配置文件路径

   **输出**:
   - 无返回值，结果保存到文件系统

输出文件
========

每个结构目录生成以下文件：

.. list-table:: 输出文件说明
   :widths: 30 70
   :header-rows: 1

   * - 文件名
     - 描述
   * - ``fitting_parameters.txt``
     - 拟合参数：E0, V0, B0, B1, R², RMSE
   * - ``fitted_data.csv``
     - 拟合曲线数据：体积和能量
   * - ``BM_fitting.png``
     - 拟合可视化图表
   * - ``OUTCAR_scale/``
     - 收集的原始VASP计算结果

拟合参数文件示例
----------------

.. code-block:: text

   Birch-Murnaghan Fitting Parameters
   ==================================

   Structure: W_bcc

   Equilibrium Energy (E0): -24.567890 eV
   Equilibrium Volume (V0): 46.656000 Å³
   Bulk Modulus (B0): 320.4567 GPa
   Pressure Derivative (B1): 4.1234

   R-squared: 0.999876
   Root Mean Square Error: 0.000123 eV

使用方式
========

命令行使用
----------

.. code-block:: bash

   # 直接运行
   python birch_murnaghan_fitting.py --input_file input.yaml

   # 通过phymlp-kit
   phymlp-kit birch_murnaghan --input_file input.yaml

Python API使用
--------------

.. code-block:: python

   from birch_murnaghan_fitting import process_all_birch_murnaghan_fitting

   # 批量处理
   process_all_birch_murnaghan_fitting("input.yaml")

   # 或单独处理
   from birch_murnaghan_fitting import (
       read_a_v_e_p_file,
       perform_fitting,
       save_fitting_results
   )

   # 读取数据
   df = read_a_v_e_p_file("path/to/a_V_E_P.txt")

   # 执行拟合
   result = perform_fitting(df, config)

   # 保存结果
   save_fitting_results(result, df, "output_dir", config, "structure_name", "source_path")

目录结构
========

输入目录结构
------------

::

   vasp_calculations/
   └── deform/
       ├── structure_1/
       │   └── a_V_E_P.txt
       ├── structure_2/
       │   └── a_V_E_P.txt
       └── structure_3/
           └── a_V_E_P.txt

输出目录结构
------------

::

   Birch_Murnaghan_fit/
   ├── structure_1/
   │   ├── a_V_E_P.txt          # 复制的原始数据
   │   ├── fitting_parameters.txt
   │   ├── fitted_data.csv
   │   ├── BM_fitting.png
   │   └── OUTCAR_scale/        # 收集的OUTCAR文件
   ├── structure_2/
   └── structure_3/

注意事项
========

1. **数据要求**：至少需要4个有效数据点才能执行拟合
2. **单位系统**：体积(Å³)，能量(eV)，压力(GPa)
3. **文件格式**：a_V_E_P.txt使用空格分隔，必须有表头
4. **配置参数**：确保配置文件中的路径正确存在

常见问题
========

Q1: 拟合失败，提示"Not enough data points"
------------------------------------------

**原因**：筛选后数据点少于4个。

**解决**：放宽筛选条件或增加计算数据点。

Q2: 找不到 a_V_E_P.txt 文件
--------------------------

**原因**：配置文件中的 root_dir 路径错误。

**解决**：检查配置文件中的 source.root_dir 路径。

Q3: 拟合结果不合理（B0为负数等）
-------------------------------

**原因**：初始猜测参数不合适。

**解决**：调整 initial_guess 中的 B0、B1 值。

相关模块
========

- :ref:`main_py` - 主命令行接口
- :ref:`core_module` - 核心工具模块
- :ref:`tools_modules` - 其他工具模块