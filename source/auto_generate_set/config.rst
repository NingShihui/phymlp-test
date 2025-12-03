配置管理模块
======================

概述
----

配置管理模块是自动化训练集生成系统的核心模块，负责加载、解析和管理项目的所有配置参数。该模块通过 YAML 配置文件统一管理 Materials Project API 设置、路径配置、形变参数、VASP 计算参数等，确保整个工作流的可配置性和可扩展性。

主要功能
--------

- **YAML 配置加载**：从 YAML 文件加载项目配置
- **智能默认值设置**：为所有配置参数提供合理的默认值
- **配置验证**：确保配置的完整性和有效性
- **结构化配置**：提供层次化的配置参数管理

核心函数
--------

load_config 函数
~~~~~~~~~~~~~~~~

**函数签名**: ``load_config(config_file="input.yaml")``

**功能说明**：
加载和验证项目的 YAML 配置文件，并返回包含所有配置参数的字典。

**参数**：
- ``config_file`` (str, 可选): 配置文件的路径，默认为 ``"input.yaml"``

**返回值**:
- ``dict``: 包含所有配置参数的字典，已填充默认值

**异常**:
- ``FileNotFoundError``: 当指定的配置文件不存在时
- ``yaml.YAMLError``: 当配置文件格式错误时

**示例代码**:
.. code-block:: python

   import config
   # 加载配置文件
   config_data = config.load_config("my_config.yaml")
   # 获取 API 密钥
   api_key = config_data['api']['key']
   # 获取元素列表
   elements = config_data['elements']

_set_default_values 函数
~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``_set_default_values(config)``

**功能说明**：
为配置参数设置默认值，确保配置字典的完整性。

**参数**:
- ``config`` (dict): 原始配置字典

**返回值**:
- ``dict``: 包含默认值的完整配置字典

**内部函数**：此函数是内部函数，通常由 ``load_config`` 调用，不建议直接使用。

配置结构
--------

路径配置 (paths)
~~~~~~~~~~~~~~~~

控制文件系统的目录结构。

- ``base_dir``: 项目根目录
- ``cif_dir``: CIF 文件存储目录
- ``poscar_dir``: POSCAR 文件存储目录
- ``deform_dir``: 形变结构目录
- ``vasp_dir``: VASP 计算目录
- ``birch_murnaghan_dir``: Birch-Murnaghan 拟合结果目录
- ``extxyz_set_dir``: 最终训练集目录

形变参数 (deformation)
~~~~~~~~~~~~~~~~~~~~~~

控制晶格形变生成。

- ``max_atoms``: 每个结构的最大原子数（默认: 150）
- ``scaling_factors``: 体积缩放因子列表（默认: [0.8, 0.9, 1.0, 1.1, 1.2]）
- ``max_supercell``: 最大超胞倍数（默认: 4）

微扰参数 (perturbation)
~~~~~~~~~~~~~~~~~~~~~~~

控制原子位置微扰生成。

- ``max_atoms``: 每个结构的最大原子数（默认: 150）
- ``max_supercell``: 最大超胞倍数（默认: 4）
- ``n_structures``: 生成的微扰结构数量（默认: 100）
- ``cell_pert_fraction``: 晶胞扰动幅度（默认: 0.05）
- ``atom_pert_distance``: 原子扰动距离（默认: 0.05）
- ``atom_pert_style``: 扰动风格，如 "uniform"（默认）

VASP 计算参数 (vasp)
~~~~~~~~~~~~~~~~~~~~

控制第一性原理计算设置。

INCAR 参数 (incar_parameters)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- ``ALGO``: 电子最小化算法（默认: "normal"）
- ``EDIFF``: 能量收敛标准（默认: 1E-3）
- ``KSPACING``: K点间距（默认: 0.2）
- ``ENCUT``: 截断能（默认: 400）
- ``ISIF``: 离子位置和晶胞优化控制（默认: 2）

POTCAR 配置 (potcar)
^^^^^^^^^^^^^^^^^^^^

- ``method``: POTCAR 生成方法（默认: "auto"）
- ``functional``: 泛函类型（默认: "PBE"）
- ``potcar_variants``: 特定元素的赝势变体
- ``potcar_base_dir``: POTCAR 文件基础目录

作业提交配置 (submission)
^^^^^^^^^^^^^^^^^^^^^^^^^

- ``slurm_headers``: SLURM 作业头信息
- ``modules``: 环境模块加载命令
- ``environment``: 环境变量设置
- ``vasp_execution``: VASP 执行命令
- ``max_batch_size``: 最大批量提交数（默认: 10）
- ``check_interval``: 作业检查间隔（秒，默认: 60）

Birch-Murnaghan 拟合配置 (birch_murnaghan_fitting)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

控制状态方程拟合参数。

- ``source``: 数据源配置
- ``results``: 结果保存配置
- ``data_filter``: 数据过滤条件
- ``fitting``: 拟合算法参数
- ``output``: 输出配置

Extxyz 数据集生成配置 (extxyz_generation)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

控制训练集生成参数。

- ``vasp``: VASP 计算结果提取配置
- ``birch_murnaghan``: 基于拟合结果的配置
- ``pressure_filter``: 压力过滤条件

配置文件示例
------------

.. code-block:: yaml
   :caption: input.yaml 示例配置

   # Materials Project API 配置
   api:
     key: "your_mp_api_key_here"

   # 材料列表
   materials:
     - "mp-134"  # 材料ID
     - "Fe"       # 元素符号
     - "Fe3Al"    # 化合物

   # 路径配置
   paths:
     base_dir: "./my_project"
     cif_dir: "base/dir_CIF"
     poscar_dir: "base/dir_POSCAR"

   # 形变参数
   deformation:
     max_atoms: 100
     scaling_factors: [0.85, 0.90, 0.95, 1.0, 1.05, 1.10, 1.15]

   # VASP 计算参数
   vasp:
     incar_parameters:
       ENCUT: 520
       EDIFF: 1E-5
     potcar:
       functional: "PBE"

   # Birch-Murnaghan 拟合
   birch_murnaghan_fitting:
     fitting:
       initial_guess:
         B0: 150
         B1: 4.5

使用流程
--------

1. **准备配置文件**: 基于示例配置创建或修改 YAML 文件

2. **加载配置**: 在代码中使用 ``load_config`` 函数加载配置

   .. code-block:: python

      import config
      my_config = config.load_config("my_input.yaml")

3. **访问配置参数**: 通过字典键值访问具体配置

   .. code-block:: python

      # 访问路径配置
      base_dir = my_config['paths']['base_dir']

      # 访问 VASP 参数
      encut = my_config['vasp']['incar_parameters']['ENCUT']

      # 访问形变参数
      scaling_factors = my_config['deformation']['scaling_factors']

4. **传递配置**: 将配置字典传递给其他模块使用

   .. code-block:: python

      from my_module import process_materials
      process_materials(my_config)

依赖关系
--------

- **Python 包**:
  - PyYAML (``pyyaml``): YAML 文件解析

- **文件系统**:
  - 有效的 YAML 配置文件
  - 必要的目录结构

最佳实践
--------

1. **版本控制**: 将配置文件纳入版本控制系统
2. **环境变量**: 敏感信息（如 API 密钥）可通过环境变量注入
3. **配置模板**: 维护不同项目的配置模板
4. **配置验证**: 在关键节点验证配置的有效性

相关模块
--------

- :doc:`/phymlp/auto_generate_set` - 自动化训练集生成主模块
- :doc:`/phymlp/converters` - 数据格式转换工具
- :doc:`/phymlp/train_and_validation/core` - 训练和验证模块