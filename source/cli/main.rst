.. _main_module:

===================
命令管理模块说明
===================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``main.py`` 是 PhyMLP Kit 工具包的命令行接口主模块，负责提供所有功能的统一入口。
它通过子命令系统组织不同的功能模块，用户可以通过 ``phymlp-kit`` 命令调用各种工具。

模块架构
========

.. mermaid::
   :caption: PhyMLP Kit 模块架构

   graph TB
       A[phymlp-kit 主程序] --> B[训练与验证模块]
       A --> C[数据转换模块]
       A --> D[数据集处理模块]
       A --> E[自动训练集生成模块]
       A --> F[VASP计算模块]
       A --> G[数据分析模块]
       A --> H[工作流模块]

       B --> B1[机器学习势训练]
       B --> B2[初始势函数生成]

       C --> C1[OUTCAR转Extxyz]
       C --> C2[CFG转Extxyz]
       C --> C3[Dump转POSCAR]

       D --> D1[数据集分割]
       D --> D2[KPATH生成]

       E --> E1[Materials Project获取]
       E --> E2[形变结构生成]
       E --> E3[微扰结构生成]

       F --> F1[VASP计算设置]
       F --> F2[VASP作业提交]
       F --> F3[POTCAR测试]

       G --> G1[形变结果处理]
       G --> G2[Birch-Murnaghan拟合]
       G --> G3[实验P-V拟合]
       G --> G4[Extxyz数据集生成]

       H --> H1[完整工作流]

模块详细说明
============

1. 训练与验证模块
----------------

1.1 train - 机器学习势训练
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def _train_command(args):
       run = RUN()
       info = run.Read(args.train_input)
       run.Key_and_parament(info)
       bool_train = run.Bool_commands(run.train)
       train_dir, train_cmd = run.Train_commands(bool_train)
       run.Train(bool_train, train_dir, train_cmd)
       bool_calc = run.Bool_commands(run.calculate)
       run.Calculate_dir(bool_calc)
       run.Rewrite_lammps_in(bool_calc)
       run.Execute(bool_calc)

**功能说明**：
- 读取训练配置文件（Inputfile.txt）
- 解析训练参数和计算参数
- 执行机器学习势训练
- 运行指定的物性计算
- 输出训练结果和计算数据

**使用示例**：
.. code-block:: bash

   phymlp-kit train --train_input Inputfile.txt

**相关类**：
- ``RUN``：训练和计算的核心控制器
- ``PUBLIC``：公共参数和工具类

1.2 init_phymlp - 初始势函数生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 从 PhyMLP 安装目录复制初始势函数文件
- 支持不同复杂度级别的势函数（06-16.PhyMLP）
- 为训练提供起点

**使用示例**：
.. code-block:: bash

   phymlp-kit init_phymlp --phymlp_load /path/to/phymlp --complexity 10.PhyMLP

**实现原理**：
通过 ``subprocess.run()`` 执行文件复制操作。

2. 数据转换模块
--------------

2.1 outcar2extxyz - OUTCAR 转 Extxyz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def extract_structures_from_outcar(outcar_path, output_path, step=1):
       # 从OUTCAR文件中提取结构信息并转换为Extxyz格式

**功能说明**：
- 解析 VASP OUTCAR 文件
- 提取原子结构、能量、力等信息
- 转换为标准的 Extxyz 格式
- 支持步长控制（提取间隔）

**使用示例**：
.. code-block:: bash

   phymlp-kit outcar2extxyz --outcar2extxyz_input ./OUTCAR --step 5

**相关函数**：
- ``extract_structures_from_outcar()``：OUTCAR 解析核心函数

2.2 cfg2extxyz - CFG 转 Extxyz
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def parse_cfg_file(cfg_path):
       # 解析CFG格式文件

   def write_extxyz(configs, output_path, type_map=None, float_fmt=".6f"):
       # 写入Extxyz格式

**功能说明**：
- 解析 CFG（原子配置文件）格式
- 支持多元素体系
- 原子类型到元素符号的映射
- 转换为 Extxyz 格式

**使用示例**：
.. code-block:: bash

   phymlp-kit cfg2extxyz --cfg2extxyz_input ./train.cfg --elements W

2.3 dump_to_poscar - LAMMPS Dump 转 POSCAR
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 将 LAMMPS 的 dump 文件转换为 VASP 的 POSCAR 格式
- 支持原子类型映射
- 批量转换目录中的所有 dump 文件

**使用示例**：
.. code-block:: bash

   phymlp-kit dump_to_poscar --input_file input.yaml

3. 数据集处理模块
---------------

3.1 split_set - 数据集分割
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def split_extxyz_structures(input_file, train_file, val_file, val_ratio=0.1):
       # 将数据集分割为训练集和验证集

**功能说明**：
- 随机分割 Extxyz 数据集
- 可指定验证集比例
- 保持数据分布的随机性

**使用示例**：
.. code-block:: bash

   phymlp-kit split_set --input_file full.extxyz --val_ratio 0.2

3.2 generate_kpath - KPATH 生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 调用 VASPKIT 生成高对称点路径
- 用于能带计算
- 基于当前目录的 POSCAR 文件

**使用示例**：
.. code-block:: bash

   phymlp-kit generate_kpath --vaspkit_load /path/to/vaspkit

4. 自动训练集生成模块
-------------------

4.1 from_mp_structures - Materials Project 结构获取
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def _cmd_from_mp_structures(args):
       # 动态导入并执行from_mp_structures模块

**功能说明**：
- 连接 Materials Project 数据库
- 基于元素和关键词搜索结构
- 下载 CIF 和 POSCAR 格式的结构文件
- API 密钥验证

**配置文件**：
- 需要 ``input.yaml`` 配置文件
- 包含 API 密钥、元素列表等参数

4.2 deform_structures - 形变结构生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 对原始结构进行晶格缩放
- 生成拉伸/压缩的结构
- 控制最大原子数和扩胞倍数

**参数配置**：
.. code-block:: yaml

   deformation:
     max_atoms: 150
     scaling_factors: [0.8, 0.9, 1.0, 1.1, 1.2]
     max_supercell: 4

4.3 perturb_structures - 微扰结构生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 对结构进行随机微扰
- 包括晶格微扰和原子位置微扰
- 生成多样化的训练结构

**参数配置**：
.. code-block:: yaml

   perturbation:
     n_structures: 100
     cell_pert_fraction: 0.05
     atom_pert_distance: 0.05

5. VASP 计算模块
---------------

5.1 setup_vasp - VASP 计算设置
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 根据配置准备 VASP 计算目录
- 生成 INCAR、KPOINTS、POTCAR 等输入文件
- 批量处理多个结构

**配置文件**：
.. code-block:: yaml

   vasp_setup:
     input_paths: ["./structures"]
     output_dir: "./vasp_calculations"

   vasp:
     incar_parameters:
       ALGO: "normal"
       ENCUT: 400
       ISMEAR: 1

5.2 submit_vasp - VASP 作业提交
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 提交 VASP 计算作业到计算集群
- 支持 SLURM 作业调度系统
- 批量提交和作业状态监控

**参数配置**：
.. code-block:: yaml

   submission:
     slurm_headers:
       - "#SBATCH -N 1"
       - "#SBATCH -n 32"
     vasp_execution:
       - "srun --mpi=pmi2 vasp_std"

5.3 test_potcar - POTCAR 测试
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 测试 POTCAR 文件生成功能
- 验证元素设置和赝势文件
- 调试配置问题

6. 数据分析模块
-------------

6.1 process_deform - 形变结果处理
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 处理形变计算的结果文件
- 提取能量-体积数据
- 准备 Birch-Murnaghan 拟合数据

6.2 birch_murnaghan - Birch-Murnaghan 拟合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def _cmd_birch_murnaghan(args):
       # 执行Birch-Murnaghan状态方程拟合

**功能说明**：
- 拟合能量-体积曲线到 Birch-Murnaghan 状态方程
- 获取体弹模量 B₀、导数 B₁ 等参数
- 生成拟合曲线和参数文件

**拟合方程**：
.. math::

   E(V) = E_0 + \frac{9V_0B_0}{16} \left\{ \left[ \left( \frac{V_0}{V} \right)^{2/3} - 1 \right]^3 B_1 + \left[ \left( \frac{V_0}{V} \right)^{2/3} - 1 \right]^2 \left[ 6 - 4 \left( \frac{V_0}{V} \right)^{2/3} \right] \right\}

6.3 exp_pv_structures - 实验 P-V 数据拟合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 拟合实验压力-体积数据
- 生成相应的结构文件
- 扩展训练数据集

6.4 generate_extxyz - Extxyz 数据集生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**功能说明**：
- 整合所有计算和拟合数据
- 生成统一的训练数据集
- 支持多种数据源

7. 工作流模块
-----------

7.1 full_workflow - 完整工作流
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   def _cmd_full_workflow(args):
       # 执行完整的工作流程

**功能说明**：
- 自动化执行从结构获取到数据集生成的完整流程
- 可配置跳过特定步骤
- 批量处理大量体系

**工作流程**：
1. 从 Materials Project 获取结构
2. 生成形变和微扰结构
3. 设置并运行 VASP 计算
4. 处理计算结果并进行拟合
5. 生成最终的 Extxyz 数据集

**使用示例**：
.. code-block:: bash

   # 完整流程
   phymlp-kit full_workflow --input_file input.yaml

   # 跳过VASP提交（仅准备文件）
   phymlp-kit full_workflow --input_file input.yaml --skip_vasp_submit

配置系统
========

1. 配置文件类型
--------------

- **``input.yaml``**：自动训练集生成的 YAML 格式配置文件
- **``Inputfile.txt``**：训练和计算的键值对格式配置文件

2. 配置解析机制
--------------

- **YAML 配置**：使用 PyYAML 库解析
- **键值对配置**：自定义解析器处理
- **路径处理**：支持相对路径和绝对路径

3. 动态模块导入
--------------

为了避免启动时依赖问题，采用动态导入策略：

.. code-block:: python

   def _cmd_from_mp_structures(args):
       try:
           # 动态添加路径
           sys.path.insert(0, auto_gen_dir)
           # 动态导入模块
           from from_mp_structures import main as from_mp_main
           from_mp_main(args.input_file)
       except ImportError as e:
           print(f"Error: Could not import from_mp_structures module: {e}")

错误处理机制
============

1. 导入错误处理
--------------

- 动态导入失败时提供清晰的错误信息
- 指导用户检查模块路径和依赖

2. 文件系统错误
--------------

- 检查文件存在性和权限
- 自动创建必要的目录结构
- 路径规范化处理

3. 计算错误处理
--------------

- VASP 计算失败检测
- 作业提交状态监控
- 计算结果验证

扩展与定制
==========

1. 添加新命令
------------

要添加新的子命令，需要：

1. 在 ``main()`` 函数中添加对应的子命令解析器
2. 实现相应的处理函数
3. 在主分发逻辑中添加调用

2. 模块扩展
----------

- 新功能模块应放置在 ``phymlp/auto_generate_set/`` 目录下
- 遵循统一的接口规范
- 支持通过 YAML 配置文件

性能优化
========

1. 批量处理
----------

- 支持批量结构处理
- 并行计算配置
- 内存使用优化

2. 缓存机制
----------

- 材料数据缓存
- 计算结果缓存
- 避免重复计算

使用建议
========

1. 新手建议
----------

- 从 ``train`` 和 ``outcar2extxyz`` 命令开始
- 使用默认配置进行测试
- 逐步添加复杂功能

2. 高级用户
----------

- 自定义工作流
- 批量处理多个体系
- 结合其他计算工具

3. 开发人员
----------

- 理解模块间的依赖关系
- 遵循现有的接口规范
- 添加充分的错误处理

相关链接
========

- :ref:`quickstart` - 快速开始指南
- :ref:`input_files/auto_trainset_input` - input.yaml 配置说明
- :ref:`input_files/train_input` - Inputfile.txt 配置说明
- `Materials Project API <https://materialsproject.org/api>`_
- `VASP 文档 <https://www.vasp.at/>`_
- `LAMMPS 文档 <https://docs.lammps.org/>`_

更新日志
========

- **v1.0**：初始版本，包含基本训练和转换功能
- **v1.1**：添加自动训练集生成模块
- **v1.2**：添加 VASP 计算和工作流管理
- **v1.3**：添加数据分析和拟合功能