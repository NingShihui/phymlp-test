形变结构生成模块
======================================

概述
----

形变结构生成模块负责对基础晶体结构进行扩胞和晶格形变，生成用于训练机器学习势的体弹性数据集。该模块通过系统性地缩放晶格常数，生成一系列不同体积的晶体结构，为后续的第一性原理计算和状态方程拟合提供基础。

主要功能
--------

- **智能扩胞**: 自动计算最优扩胞倍数，控制原子数量
- **晶格形变**: 按指定缩放因子缩放晶格体积
- **结构分类**: 按化学式对生成的形变结构进行组织
- **批量处理**: 支持批量处理多个 POSCAR 文件

核心函数
--------

find_optimal_supercell 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``find_optimal_supercell(structure, max_atoms=150, max_supercell=4)``

**功能说明**:
寻找最优的扩胞倍数，使原子数接近但不超过设定的最大值。优先考虑三个方向同时扩胞以保持晶体的各向同性。

**参数**:
- ``structure`` (pymatgen.Structure): 原始晶体结构对象
- ``max_atoms`` (int): 每个结构允许的最大原子数，默认 150
- ``max_supercell`` (int): 最大扩胞倍数，默认 4

**返回值**:
- ``list``: 最优扩胞倍数列表，格式为 [scale_x, scale_y, scale_z]

create_supercell 函数
~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``create_supercell(structure, scaling_matrix)``

**功能说明**:
根据指定的扩胞矩阵创建超胞结构。

**参数**:
- ``structure`` (pymatgen.Structure): 原始晶体结构
- ``scaling_matrix`` (list): 扩胞矩阵，格式为 [scale_x, scale_y, scale_z]

**返回值**:
- ``pymatgen.Structure``: 扩胞后的超胞结构

scale_lattice 函数
~~~~~~~~~~~~~~~~~~

**函数签名**: ``scale_lattice(structure, scale_factor)``

**功能说明**:
按照指定的缩放因子缩放晶格常数，改变晶体体积。

**参数**:
- ``structure`` (pymatgen.Structure): 待缩放的结构
- ``scale_factor`` (float): 体积缩放因子（线性尺度）

**返回值**:
- ``pymatgen.Structure``: 缩放后的晶体结构

process_structure_for_deformation 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``process_structure_for_deformation(poscar_path, output_base_dir, config)``

**功能说明**:
处理单个 POSCAR 文件，执行完整的形变结构生成流程。

**参数**:
- ``poscar_path`` (str): 输入 POSCAR 文件的路径
- ``output_base_dir`` (str): 形变结构输出基目录
- ``config`` (dict): 配置参数字典

**返回值**:
- ``int``: 为该结构生成的形变文件数量

**处理流程**:
1. 读取和验证 POSCAR 文件
2. 提取化学式并创建分类目录
3. 计算最优扩胞倍数
4. 创建超胞结构
5. 按缩放因子生成形变结构
6. 保存为 VASP 格式文件

main 函数
~~~~~~~~~

**函数签名**: ``main(config_file="input.yaml")``

**功能说明**:
模块主函数，从配置文件加载参数，批量处理所有 POSCAR 文件。

**参数**:
- ``config_file`` (str): 配置文件路径，默认 "input.yaml"

**返回值**:
- ``None``: 直接在控制台输出处理结果

**执行流程**:
1. 加载配置文件
2. 检查输入目录
3. 创建输出目录
4. 遍历所有 POSCAR 文件
5. 对每个文件调用 process_structure_for_deformation
6. 统计并输出处理结果

配置参数
--------

路径配置
~~~~~~~~

从配置文件中读取的关键路径参数：

- ``paths.base_dir``: 项目根目录
- ``paths.poscar_dir``: 原始 POSCAR 文件目录
- ``paths.deform_dir``: 形变结构输出目录

形变参数
~~~~~~~~

控制形变生成的关键参数：

- ``deformation.max_atoms``: 每个结构最大原子数，默认 150
- ``deformation.max_supercell``: 最大扩胞倍数，默认 4
- ``deformation.scaling_factors``: 体积缩放因子列表，默认 [0.8, 0.9, 1.0, 1.1, 1.2]

文件命名规则
------------

生成的形变结构按以下规则命名：

.. code-block:: text

   {原始文件名}_scaled_{缩放因子}.vasp

例如：``Ni3Al_scaled_0.8.vasp``, ``Ni3Al_scaled_1.2.vasp``

目录组织结构
------------

形变结构按化学式分层组织：

.. code-block:: text

   deform_dir/
   ├── Ni3Al/
   │   ├── Ni3Al_mp-12345/
   │   │   ├── Ni3Al_mp-12345_scaled_0.8.vasp
   │   │   ├── Ni3Al_mp-12345_scaled_0.9.vasp
   │   │   └── ...
   │   └── Ni3Al_another/
   │       └── ...
   ├── Fe/
   └── ...

使用示例
--------

命令行调用
~~~~~~~~~~

.. code-block:: bash

   phymlp-kit deform_structures --input_file config.yaml

Python 脚本调用
~~~~~~~~~~~~~~~

.. code-block:: python

   import deform_structures

   # 直接运行
   deform_structures.main("my_config.yaml")

   # 或分步处理
   from config import load_config
   config = load_config("my_config.yaml")

   # 处理单个结构
   num_files = process_structure_for_deformation(
       "path/to/POSCAR.vasp",
       "output/deform",
       config
   )

依赖关系
--------

- **Python 包**:
  - pymatgen: 晶体结构操作
  - numpy: 数值计算

- **文件依赖**:
  - POSCAR 格式的晶体结构文件
  - YAML 配置文件

- **模块依赖**:
  - config: 配置管理模块
  - utils: 工具函数模块

常见问题
--------

Q1: 没有生成任何形变结构
~~~~~~~~~~~~~~~~~~~~~~~~

可能原因：
1. 输入目录中没有 POSCAR 文件
2. POSCAR 文件格式错误
3. 配置中的缩放因子列表为空

解决方案：
1. 检查 ``paths.poscar_dir`` 路径和文件
2. 验证 POSCAR 文件格式
3. 确认 ``deformation.scaling_factors`` 配置

Q2: 生成的原子数超过限制
~~~~~~~~~~~~~~~~~~~~~~~~

可能原因：
1. 原始结构原子数过多
2. 扩胞倍数设置过大

解决方案：
1. 调整 ``deformation.max_atoms`` 参数
2. 减小 ``deformation.max_supercell`` 值
3. 手动筛选原子数较少的结构

Q3: 化学式识别错误
~~~~~~~~~~~~~~~~~~

可能原因：
1. 文件名不符合命名规范
2. 特殊字符处理问题

解决方案：
1. 确保文件名包含可识别的化学式
2. 使用 ``get_formula_from_filename`` 函数进行调试

相关模块
--------

- :doc:`/phymlp/auto_generate_set/from_mp_structures` - 从 Materials Project 获取原始结构
- :doc:`/phymlp/auto_generate_set/config` - 配置管理模块
- :doc:`/phymlp/auto_generate_set/birch_murnaghan_fitting` - 状态方程拟合模块