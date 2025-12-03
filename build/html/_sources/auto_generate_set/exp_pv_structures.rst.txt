实验P-V数据拟合模块
========================================

概述
----

实验P-V数据拟合模块用于将实验测量的压力-体积数据转换为机器学习势训练所需的晶体结构数据。该模块通过拟合实验数据与DFT计算的晶格常数，生成压力与晶格缩放因子的对应关系，为基于实验数据生成训练集提供支持。

主要功能
--------

- **实验数据读取**: 支持多种编码格式的实验数据文件
- **数据转换**: 将实验P-V数据转换为晶格常数与压力的关系
- **多项式拟合**: 使用多项式拟合压力与晶格常数的关系
- **结果可视化**: 生成拟合结果的图形展示
- **数据导出**: 输出拟合数据供后续结构生成使用

核心函数
--------

read_config 函数
~~~~~~~~~~~~~~~~

**函数签名**: ``read_config(config_file)``

**功能说明**:
读取YAML配置文件，支持多种编码格式以防止编码问题。

**参数**:
- ``config_file`` (str): 配置文件路径

**返回值**:
- ``dict``: 解析后的配置字典

**异常**:
- ``ValueError``: 当所有编码格式都失败时抛出

read_exp_data 函数
~~~~~~~~~~~~~~~~~

**函数签名**: ``read_exp_data(exp_file, dft_a0, pressure_range=None)``

**功能说明**:
读取实验数据文件并计算对应的晶格常数。

**参数**:
- ``exp_file`` (str): 实验数据文件路径
- ``dft_a0`` (float): DFT计算的零压晶格常数
- ``pressure_range`` (tuple, 可选): 压力范围筛选，格式为 (min, max)

**返回值**:
- ``tuple``: (pressures, a_values) - 压力数组和晶格常数数组

**计算公式**:
.. math::
   a = a_0 \times \left( \frac{V}{V_0} \right)^{1/3}

save_dft_a_p_data 函数
~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``save_dft_a_p_data(output_dir, pressures, a_values, dft_a0)``

**功能说明**:
保存DFT晶格常数与压力的对应关系数据。

**参数**:
- ``output_dir`` (str): 输出目录
- ``pressures`` (array): 压力数据数组
- ``a_values`` (array): 晶格常数数据数组
- ``dft_a0`` (float): DFT零压晶格常数

**返回值**:
- ``str``: 输出文件路径

**输出格式**:
包含三列数据：压力(GPa)、晶格常数(Å)、缩放因子

fit_pressure_relation 函数
~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``fit_pressure_relation(pressures, a_values, poly_degree=4)``

**功能说明**:
使用多项式拟合压力与晶格常数的关系。

**参数**:
- ``pressures`` (array): 压力数据
- ``a_values`` (array): 晶格常数数据
- ``poly_degree`` (int, 可选): 多项式次数，默认4

**返回值**:
- ``tuple``: (coefficients, poly_func) - 拟合系数和多项式函数

**拟合模型**:
.. math::
   P(a) = B_0 + B_1 a + B_2 a^2 + B_3 a^3 + B_4 a^4

save_fitting_results 函数
~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``save_fitting_results(output_dir, coefficients, poly_func, a_values, pressures, dft_a0, pressure_range, num_points=1000)``

**功能说明**:
保存拟合结果和拟合曲线数据。

**参数**:
- ``output_dir`` (str): 输出目录
- ``coefficients`` (array): 拟合系数
- ``poly_func`` (function): 多项式函数
- ``a_values`` (array): 原始晶格常数数据
- ``pressures`` (array): 原始压力数据
- ``dft_a0`` (float): DFT零压晶格常数
- ``pressure_range`` (tuple): 使用的压力范围
- ``num_points`` (int, 可选): 拟合曲线采样点数，默认1000

**返回值**:
- ``tuple``: (a_fit, p_fit) - 拟合曲线的晶格常数和压力数据

**输出文件**:
1. ``fitting_coefficients.txt``: 拟合系数和统计信息
2. ``fit_a_P.data``: 拟合曲线数据

plot_fitting_results 函数
~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``plot_fitting_results(output_dir, a_values, pressures, a_fit, p_fit, dft_a0, pressure_range)``

**功能说明**:
绘制并保存拟合结果的可视化图像。

**参数**:
- ``output_dir`` (str): 输出目录
- ``a_values`` (array): 原始晶格常数数据
- ``pressures`` (array): 原始压力数据
- ``a_fit`` (array): 拟合曲线晶格常数数据
- ``p_fit`` (array): 拟合曲线压力数据
- ``dft_a0`` (float): DFT零压晶格常数
- ``pressure_range`` (tuple): 压力范围

**输出文件**:
- ``pressure_fitting.png``: 双面板拟合结果图

**图像内容**:
- 左图：晶格常数 vs 压力
- 右图：缩放因子 vs 压力

main 函数
~~~~~~~~~

**函数签名**: ``main(config_file)``

**功能说明**:
模块主函数，执行完整的实验P-V数据拟合流程。

**参数**:
- ``config_file`` (str): 配置文件路径

**执行流程**:
1. 读取配置文件
2. 读取实验数据
3. 数据转换和计算
4. 多项式拟合
5. 保存结果
6. 生成可视化图像

配置文件结构
------------

实验P-V拟合配置位于配置文件中的 ``experimental_pv_fitting`` 部分：

.. code-block:: yaml

   experimental_pv_fitting:
     # 必需参数
     DFT_a0: 3.615           # DFT计算的零压晶格常数（Å）
     EXP_data_file: "experimental_data.txt"  # 实验数据文件路径

     # 可选参数
     output_directory: "./exp_pv_fitting"  # 输出目录
     polynomial_degree: 4                   # 多项式拟合次数
     num_fit_points: 1000                   # 拟合曲线采样点数
     pressure_range: [0, 100]               # 压力范围筛选（GPa）

实验数据格式
------------

实验数据文件应为纯文本格式，每行包含压力值和V/V₀比值：

.. code-block:: text

   # 压力(GPa)  V/V₀
   0.0   1.0000
   10.0  0.9876
   20.0  0.9754
   30.0  0.9635
   40.0  0.9520

输出文件说明
------------

模块运行后生成以下文件：

1. **DFT_a_P.data**: 转换后的实验数据
   - 格式：压力(GPa) | 晶格常数(Å) | 缩放因子

2. **fit_a_P.data**: 拟合曲线数据
   - 格式：晶格常数(Å) | 缩放因子 | 压力(GPa)

3. **fitting_coefficients.txt**: 拟合系数和统计信息
   - 包含：拟合系数、R²值、DFT_a0、数据统计等

4. **pressure_fitting.png**: 可视化图像
   - 左图：晶格常数 vs 压力
   - 右图：缩放因子 vs 压力

使用方式
--------

命令行调用
~~~~~~~~~~

.. code-block:: bash

   # 通过phymlp-kit调用
   phymlp-kit exp_pv_structures --input_file config.yaml

   # 或直接运行Python脚本
   python exp_pv_structures.py input.yaml

Python脚本调用
~~~~~~~~~~~~~~

.. code-block:: python

   import exp_pv_structures

   # 直接运行
   exp_pv_structures.main("my_config.yaml")

   # 分步处理
   config = exp_pv_structures.read_config("my_config.yaml")
   pressures, a_values = exp_pv_structures.read_exp_data(
       "exp_data.txt",
       dft_a0=3.615
   )
   coefficients, poly_func = exp_pv_structures.fit_pressure_relation(
       pressures,
       a_values
   )

依赖关系
--------

- **Python包**:
  - numpy: 数值计算和拟合
  - matplotlib: 数据可视化
  - PyYAML: 配置文件解析

- **数据依赖**:
  - 实验P-V数据文件
  - DFT计算的零压晶格常数

常见问题
--------

Q1: 实验数据文件读取失败
~~~~~~~~~~~~~~~~~~~~~~~~

**可能原因**:
1. 文件编码不兼容
2. 文件格式不符合要求
3. 数据超出压力范围

**解决方案**:
1. 确保文件使用UTF-8或ASCII编码
2. 检查数据格式是否符合要求
3. 调整配置文件中的压力范围

Q2: 拟合效果不理想（R²值过低）
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**可能原因**:
1. 实验数据质量差
2. 多项式次数不合适
3. 数据范围过大

**解决方案**:
1. 检查实验数据质量
2. 调整 ``polynomial_degree`` 参数
3. 缩小压力范围

Q3: 晶格常数计算错误
~~~~~~~~~~~~~~~~~~~~

**可能原因**:
1. DFT_a0 参数错误
2. V/V₀ 数据格式错误

**解决方案**:
1. 检查DFT计算的晶格常数是否正确
2. 确认实验数据中的V/V₀比值是否正确

应用场景
--------

该模块主要用于：

1. **实验数据验证**: 验证DFT计算与实验数据的一致性
2. **训练集扩展**: 基于实验数据生成额外的训练结构
3. **状态方程校准**: 校准机器学习势的状态方程参数
4. **多尺度建模**: 连接原子尺度计算与宏观实验数据

相关模块
--------

- :doc:`/phymlp/auto_generate_set/deform_structures` - 形变结构生成
- :doc:`/phymlp/auto_generate_set/birch_murnaghan_fitting` - 状态方程拟合
- :doc:`/phymlp/auto_generate_set/generate_extxyz_dataset` - 训练集生成