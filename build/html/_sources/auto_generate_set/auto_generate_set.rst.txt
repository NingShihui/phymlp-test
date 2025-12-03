自动训练集生成模块
========================================

概述
----

自动化训练集生成模块是 PhyMLP Kit 的核心功能模块之一，提供了一套完整的、自动化的机器学习势训练集构建流程。该模块通过结合材料数据库、第一性原理计算和结构生成算法，实现了从零开始构建高质量训练集的完整工作流。

主要特点
--------

- **全自动流程**：从结构获取到数据集生成的完整自动化流程
- **多数据源支持**：支持从 Materials Project 数据库获取初始结构
- **多尺度采样**：包含晶格形变、原子微扰等多种结构采样方法
- **VASP集成**：自动设置和提交第一性原理计算任务
- **智能后处理**：自动处理计算结果并生成训练集

核心功能
--------

从 Materials Project 获取结构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit from_mp_structures --input_file config.yaml

从 Materials Project 数据库获取初始晶体结构，支持：
- 通过材料ID（如 mp-12345）或化学式（如 Ni3Al）检索
- 自动下载晶体结构并保存为 POSCAR 格式
- 支持多结构批量下载

结构形变生成
~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit deform_structures --input_file config.yaml

生成晶格形变结构，用于采样能量-体积（E-V）曲线：
- Birch-Murnaghan 状态方程驱动的体积变化
- 各向同性/各向异性形变
- 自定义形变范围和步长

原子位置微扰
~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit perturb_structures --input_file config.yaml

生成原子位置微扰结构，用于采样构型空间：
- 随机原子位移
- 温度相关的热扰动
- 自定义扰动幅度和方向

VASP 计算设置
~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit setup_vasp --input_file config.yaml

自动设置第一性原理计算环境：
- 生成 INCAR、KPOINTS、POTCAR 等输入文件
- 根据结构自动选择合适的计算参数
- 支持不同的泛函和赝势

VASP 作业提交
~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit submit_vasp --input_file config.yaml

自动提交 VASP 计算任务：
- 支持 SLURM、PBS 等作业调度系统
- 批量作业提交和管理
- 作业状态监控和错误处理

POTCAR 生成测试
~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit test_potcar --poscar POSCAR --input_file config.yaml

测试 POTCAR 文件生成：
- 验证赝势文件可用性
- 元素匹配检查
- 赝势版本兼容性验证

形变结果处理
~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit process_deform --input_file config.yaml

处理形变计算的结构和能量：
- 提取 OUTCAR 中的能量和应力信息
- 结构弛豫结果分析
- 能量-体积数据整理

Birch-Murnaghan 拟合
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit birch_murnaghan --input_file config.yaml

执行 Birch-Murnaghan 状态方程拟合：
- 从能量-体积数据拟合状态方程参数
- 计算体模量、平衡体积等物理量
- 生成拟合曲线和数据报告

实验 P-V 数据拟合
~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit exp_pv_structures --input_file config.yaml

基于实验 P-V 数据生成训练结构：
- 导入实验压力-体积数据
- 插值生成对应体积的结构
- 支持多种实验数据格式

数据转 POSCAR
~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit dump_to_poscar --input_file config.yaml

将各类数据转换为 POSCAR 格式：
- 支持多种中间格式转换
- 保持晶体对称性信息
- 原子类型和坐标格式标准化

Extxyz 数据集生成
~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit generate_extxyz --input_file config.yaml

生成最终的训练数据集：
- 整合所有计算结构
- 转换为 PhyMLP 兼容的 extxyz 格式
- 包含能量、力、应力等信息

完整工作流
~~~~~~~~~~

.. code-block:: bash

   phymlp-kit full_workflow --input_file config.yaml

执行从结构获取到数据集生成的完整流程：
- 顺序执行所有步骤
- 支持步骤跳过和断点续做
- 进度监控和错误恢复

配置系统
--------

所有功能都通过 YAML 配置文件控制，配置文件包含以下主要部分：

.. code-block:: yaml

   # 示例配置文件结构
   materials_project:
     api_key: "your_mp_api_key"
     materials: ["mp-12345", "Ni3Al"]

   structure_generation:
     deformation:
       volume_range: [0.85, 1.15]
       num_structures: 10
     perturbation:
       displacement: 0.02
       num_perturbations: 5

   vasp_calculation:
     functional: "PBE"
     encut: 520
     kpoints: [4, 4, 4]
     convergence:
       ediff: 1e-6
       ediffg: -0.02

   data_processing:
     output_format: "extxyz"
     include_forces: true
     include_stress: true

工作流程
--------

典型的自动化训练集生成流程如下：

.. mermaid::

   graph TD
       A[开始] --> B[从MP获取结构];
       B --> C[生成形变结构];
       B --> D[生成微扰结构];
       C --> E[设置VASP计算];
       D --> E;
       E --> F[提交VASP作业];
       F --> G[等待计算完成];
       G --> H[提取计算结果];
       H --> I[数据处理];
       I --> J[生成训练集];
       J --> K[完成];

依赖关系
--------

- **Python包**:
  - pymatgen: 材料结构处理
  - numpy, scipy: 数值计算和拟合
  - pyyaml: 配置文件解析

- **外部软件**:
  - VASP: 第一性原理计算
  - PhyMLP: 机器学习势训练

- **服务**:
  - Materials Project API: 材料数据库访问

使用示例
--------

基本使用
~~~~~~~~

.. code-block:: bash

   # 1. 准备配置文件
   cp auto_generate_set/example_config.yaml my_config.yaml

   # 2. 编辑配置文件
   # 修改 materials_project, structure_generation 等部分

   # 3. 执行完整工作流
   phymlp-kit full_workflow --input_file my_config.yaml

分步执行
~~~~~~~~

.. code-block:: bash

   # 分步执行以获得更多控制
   phymlp-kit from_mp_structures --input_file config.yaml
   phymlp-kit deform_structures --input_file config.yaml
   phymlp-kit setup_vasp --input_file config.yaml
   phymlp-kit submit_vasp --input_file config.yaml
   # 等待VASP计算完成...
   phymlp-kit process_deform --input_file config.yaml
   phymlp-kit generate_extxyz --input_file config.yaml

常见问题
--------

Q1: 如何获取 Materials Project API 密钥？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 访问 https://materialsproject.org
2. 注册账户并登录
3. 在个人设置中生成 API 密钥
4. 在配置文件中添加 ``api_key: "your_key"``

Q2: VASP 计算失败如何处理？
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. 检查 ``vasp_calculation`` 配置参数
2. 验证 POTCAR 文件路径和内容
3. 查看 VASP 输出文件（OUTCAR, OSZICAR）
4. 调整收敛标准和计算参数

Q3: 如何自定义结构生成策略？
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

修改 ``structure_generation`` 部分：
- ``deformation.volume_range``: 体积变化范围
- ``deformation.num_structures``: 形变结构数量
- ``perturbation.displacement``: 微扰幅度
- ``perturbation.num_perturbations``: 微扰数量

进阶使用
--------

自定义插件
~~~~~~~~~~

可通过继承基类实现自定义结构生成器：

.. code-block:: python

   from phymlp.auto_generate_set.base import StructureGenerator

   class MyGenerator(StructureGenerator):
       def generate_structures(self, base_structure):
           # 自定义结构生成逻辑
           pass

批量处理
~~~~~~~~

支持多个材料的并行处理：

.. code-block:: yaml

   materials_project:
     materials: ["mp-12345", "mp-67890", "Ni3Al", "TiAl"]

   parallel:
     enabled: true
     max_workers: 4

相关文档
--------

- :doc:`/phymlp/converters` - 数据格式转换工具
- :doc:`/phymlp/tools/split_set` - 数据集分割工具
- :doc:`/phymlp/train_and_validation/core` - 训练和验证模块
- `Materials Project 文档 <https://docs.materialsproject.org/>`_
- `VASP 文档 <https://www.vasp.at/>`_