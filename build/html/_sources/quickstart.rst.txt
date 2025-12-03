<<<<<<< HEAD
快速开始指南
===========

.. contents:: 目录
   :depth: 3
   :local:

概述
====

PhyMLP Kit 是一个用于机器学习势（Machine Learning Potential）训练、验证和数据集生成的综合工具包。本指南将帮助您快速上手使用 PhyMLP Kit 的主要功能。

安装与设置
==========

1. 环境要求
------------

- Python 3.8+
- VASP（用于第一性原理计算）
- LAMMPS（用于分子动力学计算）
- VASPKIT（用于能带路径生成）
- PhyMLP（机器学习势框架）

2. 安装 PhyMLP Kit
--------------------

.. code-block:: bash

   # 克隆仓库
   git clone <repository-url>（目前项目仍处于开发阶段，如需使用请联系开发者ningshihui@hnu.edu.cn或者b240700371@hnu.edu.cn）
   cd phymlp-kit

   # 安装依赖
   pip install -r requirements.txt

   # 安装为可执行包
   pip install -e .

3. 配置软件路径
----------------

确保以下软件已正确安装并配置好环境变量：

   - **VASP**：第一性原理计算软件
   - **LAMMPS**：分子动力学软件（需支持 PhyMLP）
   - **VASPKIT**：VASP 辅助工具
   - **PhyMLP**：机器学习势框架

基本使用
========

PhyMLP Kit 提供了丰富的命令行工具，基本语法格式为：

.. code-block:: bash

   phymlp-kit <command> [--options]

查看帮助信息：

.. code-block:: bash

   # 查看所有命令
   phymlp-kit --help

   # 查看特定命令帮助
   phymlp-kit <command> --help

核心功能模块
============

1. 机器学习势训练
----------------

使用 ``train`` 命令进行机器学习势的训练和验证：

.. code-block:: bash

   # 基本训练
   phymlp-kit train --train_input Inputfile.txt

   # 查看训练选项
   phymlp-kit train --help

训练配置文件 ``Inputfile.txt`` 需要包含：

- 软件路径设置
- 训练参数
- 计算参数

2. 初始势函数生成
----------------

获取不同复杂度的初始势函数：

.. code-block:: bash

   # 获取默认的 10.PhyMLP
   phymlp-kit init_phymlp --phymlp_load /path/to/phymlp

   # 获取特定复杂度的势函数
   phymlp-kit init_phymlp --phymlp_load /path/to/phymlp --complexity 12.PhyMLP

支持的复杂度级别：06.PhyMLP, 08.PhyMLP, 10.PhyMLP, 12.PhyMLP, 14.PhyMLP, 16.PhyMLP

3. 数据格式转换
--------------

3.1 OUTCAR 转 Extxyz
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 转换单个 OUTCAR 文件
   phymlp-kit outcar2extxyz --outcar2extxyz_input ./OUTCAR --outcar2extxyz_output ./train.extxyz

   # 指定提取步长
   phymlp-kit outcar2extxyz --outcar2extxyz_input ./OUTCAR --step 5

3.2 CFG 转 Extxyz
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 转换 CFG 格式数据
   phymlp-kit cfg2extxyz --cfg2extxyz_input ./train.cfg --elements W

   # 多元素体系
   phymlp-kit cfg2extxyz --cfg2extxyz_input ./train.cfg --elements Ni Cr Co Fe

3.3 Dump 转 POSCAR
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 转换 LAMMPS dump 文件
   phymlp-kit dump_to_poscar --input_file input.yaml

4. 数据集处理
--------------

4.1 数据集分割
~~~~~~~~~~~~~

.. code-block:: bash

   # 分割训练集和验证集
   phymlp-kit split_set --input_file full_dataset.extxyz --set_train train.extxyz --set_val validation.extxyz --val_ratio 0.1

4.2 KPATH 生成
~~~~~~~~~~~~~

.. code-block:: bash

   # 为能带计算生成高对称点路径
   phymlp-kit generate_kpath --vaspkit_load /path/to/vaspkit

5. 自动训练集生成流程
-------------------

5.1 从 Materials Project 获取结构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit from_mp_structures --input_file input.yaml

5.2 生成形变结构
~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit deform_structures --input_file input.yaml

5.3 生成微扰结构
~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit perturb_structures --input_file input.yaml

5.4 设置 VASP 计算
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit setup_vasp --input_file input.yaml

5.5 提交 VASP 计算
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit submit_vasp --input_file input.yaml

6. 数据分析与拟合
---------------

6.1 处理形变计算结果
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit process_deform --input_file input.yaml

6.2 Birch-Murnaghan 状态方程拟合
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit birch_murnaghan --input_file input.yaml

6.3 实验 P-V 数据拟合
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit exp_pv_structures --input_file input.yaml

7. 数据集生成
------------

7.1 生成 Extxyz 数据集
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit generate_extxyz --input_file input.yaml

7.2 测试 POTCAR 生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   phymlp-kit test_potcar --poscar POSCAR --input_file input.yaml

8. 完整工作流
--------------

执行从结构获取到数据集生成的完整流程：

.. code-block:: bash

   # 完整流程
   phymlp-kit full_workflow --input_file input.yaml

   # 跳过 VASP 提交（仅准备输入文件）
   phymlp-kit full_workflow --input_file input.yaml --skip_vasp_submit

   # 跳过 Extxyz 生成
   phymlp-kit full_workflow --input_file input.yaml --skip_extxyz

典型工作流程示例
================

以下是一个完整的钨（W）体系机器学习势训练流程示例：

1. 准备阶段
------------

.. code-block:: bash

   # 1. 获取初始势函数
   phymlp-kit init_phymlp --phymlp_load /path/to/phymlp --complexity 10.PhyMLP

   # 2. 从 VASP 计算结果提取训练数据
   phymlp-kit outcar2extxyz --outcar2extxyz_input ./OUTCAR --outcar2extxyz_output ./w_data.extxyz

   # 3. 分割数据集
   phymlp-kit split_set --input_file w_data.extxyz --set_train w_train.extxyz --set_val w_val.extxyz --val_ratio 0.2

2. 训练阶段
------------

.. code-block:: bash

   # 准备 Inputfile.txt 配置文件
   # 设置软件路径、训练参数等

   # 执行训练
   phymlp-kit train --train_input Inputfile.txt

3. 扩展训练集（可选）
---------------------

.. code-block:: bash

   # 1. 生成更多训练结构
   phymlp-kit deform_structures --input_file input.yaml
   phymlp-kit perturb_structures --input_file input.yaml

   # 2. 设置并运行 VASP 计算
   phymlp-kit setup_vasp --input_file input.yaml
   phymlp-kit submit_vasp --input_file input.yaml

   # 3. 提取新的训练数据
   phymlp-kit outcar2extxyz --outcar2extxyz_input ./new_OUTCAR --outcar2extxyz_output ./new_data.extxyz

4. 验证阶段
------------

训练完成后，势函数文件保存在 ``./train/pot.PhyMLP``，可用于各种物性计算。

配置说明
========

1. 主配置文件（input.yaml）
---------------------------

用于自动训练集生成的 YAML 配置文件，包含：

- Materials Project API 配置
- 元素配置
- 路径配置
- 形变和微扰参数
- VASP 计算参数
- 拟合参数

2. 训练配置文件（Inputfile）
-------------------------------

用于机器学习势训练和性质计算的配置文件，包含：

- 软件路径设置
- 训练参数
- 计算参数
- 物性计算选项

常见问题
========

1. 软件路径错误
----------------

   **问题**：运行命令时提示找不到软件
   **解决**：检查 ``Inputfile`` 中的软件路径设置，确保使用绝对路径

2. 训练失败
------------

   **问题**：训练过程中出错
   **解决**：
   - 检查训练集文件格式是否正确
   - 确认初始势函数文件存在
   - 检查元素映射是否正确

3. VASP 计算设置错误
---------------------

   **问题**：VASP 计算无法运行
   **解决**：
   - 检查 ``input.yaml`` 中的 VASP 参数
   - 确认 POTCAR 文件路径正确
   - 检查作业提交脚本配置

4. 数据集生成问题
-----------------

   **问题**：Extxyz 数据集生成失败
   **解决**：
   - 检查 OUTCAR 文件是否完整
   - 确认输入文件路径正确
   - 检查 YAML 配置文件格式

高级功能
========

1. 批量处理
------------

支持批量处理多个结构或计算任务：

.. code-block:: bash

   # 批量转换多个 OUTCAR 文件
   for file in *.OUTCAR; do
       phymlp-kit outcar2extxyz --outcar2extxyz_input $file --outcar2extxyz_output ${file%.*}.extxyz
   done

2. 自定义工作流
----------------

可根据需要组合不同命令构建自定义工作流：

.. code-block:: bash

   # 自定义工作流示例
   # 1. 获取结构
   phymlp-kit from_mp_structures --input_file config.yaml

   # 2. 生成形变
   phymlp-kit deform_structures --input_file config.yaml

   # 3. 运行计算
   phymlp-kit setup_vasp --input_file config.yaml
   phymlp-kit submit_vasp --input_file config.yaml

   # 4. 提取数据
   find ./vasp_calculations -name "OUTCAR" | xargs -I {} phymlp-kit outcar2extxyz --outcar2extxyz_input {} --step 10

3. 并行计算
-----------

部分命令支持并行处理，可通过调整配置提高效率：

- VASP 计算支持批量提交
- 数据集生成支持并行处理
- 拟合计算可并行执行

获取帮助
========

- 查看命令行帮助：``phymlp-kit --help``
- 查看具体命令帮助：``phymlp-kit <command> --help``
- 查看配置文件说明：参考 :ref:`input_files/auto_trainset_input` 和 :ref:`input_files/train_input`
- 报告问题：提交到项目 Issue 页面

下一步
======

- 阅读 :ref:`input_files/auto_trainset_input` 了解详细配置选项
- 参考 :ref:`input_files/train_input` 了解训练参数设置
- 查看示例文件了解具体使用方式
- 尝试运行提供的测试用例
=======
快速开始
========

PhyMLP Kit 是一个功能强大的机器学习势函数工具包，提供训练、验证、数据处理及自动训练集生成的全套命令行工具。

安装
----

.. code-block:: bash

    pip install phymlp-kit

基础使用
-------

查看所有可用命令：

.. code-block:: bash

    phymlp-kit -h

核心功能模块
-----------

训练与验证
~~~~~~~~~~

使用 ``Inputfile.txt`` 配置文件训练 PhyMLP 模型：

.. code-block:: bash

    phymlp-kit train --train_input Inputfile.txt

数据格式转换
~~~~~~~~~~

OUTCAR 转 extxyz 格式：

.. code-block:: bash

    phymlp-kit outcar2extxyz --outcar2extxyz_input OUTCAR --outcar2extxyz_output train.extxyz --step 1

CFG 转 extxyz 格式：

.. code-block:: bash

    phymlp-kit cfg2extxyz --cfg2extxyz_input train.cfg --cfg2extxyz_output train.extxyz --elements Ni Cr Co

数据集分割：

.. code-block:: bash

    phymlp-kit split_set --input_file dataset.extxyz --set_train train.extxyz --set_val validation.extxyz --val_ratio 0.1

工具函数
~~~~~~~

生成 K 路径：

.. code-block:: bash

    phymlp-kit generate_kpath --vaspkit_load /path/to/vaspkit

初始化 PhyMLP：

.. code-block:: bash

    phymlp-kit init_phymlp --phymlp_load /path/to/phymlp --complexity 10.PhyMLP

自动训练集生成工作流
-------------------

使用 ``input.yaml`` 配置文件自动化生成训练集：

1. 从 Materials Project 获取结构
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit from_mp_structures --input_file input.yaml

配置示例（input.yaml 相关部分）：

.. code-block:: yaml

    # Materials Project API配置
    api:
      key: "your_api_key_here"

    # 元素配置
    elements:
      - "Ni"
      - "Cr"

    # 输出路径配置
    paths:
      base_dir: "./materials_project"

2. 生成形变结构
~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit deform_structures --input_file input.yaml

配置示例：

.. code-block:: yaml

    # 形变参数配置
    deformation:
      max_atoms: 150
      scaling_factors: [0.8, 0.9, 1.0, 1.1, 1.2]
      max_supercell: 4

3. 生成微扰结构
~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit perturb_structures --input_file input.yaml

配置示例：

.. code-block:: yaml

    # 微扰参数配置
    perturbation:
      max_atoms: 150
      max_supercell: 4
      n_structures: 100
      cell_pert_fraction: 0.05
      atom_pert_distance: 0.05

4. 设置 VASP 计算
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit setup_vasp --input_file input.yaml

配置示例：

.. code-block:: yaml

    # VASP计算配置
    vasp:
      incar_parameters:
        ENCUT: 400
        ISIF: 2
        KSPACING: 0.2
      potcar:
        functional: "PBE"
      submission:
        slurm_headers:
          - "#SBATCH -N 1"
          - "#SBATCH -n 32"

5. 测试 POTCAR 生成
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit test_potcar --poscar POSCAR --input_file input.yaml

6. 提交 VASP 计算
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit submit_vasp --input_file input.yaml

7. 处理形变结果
~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit process_deform --input_file input.yaml

8. Birch-Murnaghan 拟合
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit birch_murnaghan --input_file input.yaml

配置示例：

.. code-block:: yaml

    # Birch-Murnaghan拟合配置
    birch_murnaghan_fitting:
      fitting:
        initial_guess:
          B0: 100
          B1: 4.0

9. 生成最终数据集
~~~~~~~~~~~~~~~~~

.. code-block:: bash

    phymlp-kit generate_extxyz --input_file input.yaml

配置文件详解
-----------

训练配置文件 Inputfile.txt
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: none

    ### 必须自定义的参数 ###
    PhyMLP_load      = "/path/to/phymlp"           # PhyMLP安装目录
    lmp_mpi_load     = "/path/to/lmp_mpi"          # LAMMPS可执行文件路径
    vaspkit_load     = "/path/to/vaspkit"          # VASPKIT可执行文件路径

    ### 训练过程参数设置 ###
    train            = "true"                      # 训练指令
    extxyz_load      = "../train.extxyz"           # 训练集路径
    init_PhyMLP      = "./10.PhyMLP"               # 训练势函数level
    iteration_limit  = "1000"                      # 最大迭代次数
    al_mode          = "nbh"                       # 训练模式

    ### 性质计算参数设置 ###
    calculate        = "false"                     # 计算指令
    crystal_structure= "bcc"                       # 晶体结构类型
    lattice          = "3.5"                       # 平衡晶格常数
    atomic_mass      = "183.84"                    # 元素的相对原子质量
    pot_PhyMLP_load  = "./train/pot.PhyMLP"        # PhyMLP势文件路径
    properties       = "E-V"                       # 单原子能量-体积计算
    properties       = "Elastic"                   # 弹性常数计算
    properties       = "phonon"                    # 声子谱计算
    properties       = "P-V"                       # 压力-体积计算

自动化训练集配置文件 input.yaml
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: yaml

    # Materials Project API配置
    api:
      key: "your_api_key_here"

    # 元素配置
    elements:
      - "Ni"
      - "Cr"

    # 输出路径配置
    paths:
      base_dir: "./materials_project"
      cif_dir: "base/dir_CIF"
      poscar_dir: "base/dir_POSCAR"

    # 用户自定义POSCAR配置
    user_poscar:
      enabled: true
      source_dir: "./input-poscar"

    # 形变参数配置
    deformation:
      max_atoms: 150
      scaling_factors: [0.8, 0.9, 1.0, 1.1, 1.2]

    # VASP计算配置
    vasp:
      incar_parameters:
        ENCUT: 400
        ISIF: 2
        KSPACING: 0.2
      submission:
        slurm_headers:
          - "#SBATCH -N 1"
          - "#SBATCH -n 32"

典型工作流程
-----------

快速开始示例：Ni-Cr 合金训练集生成
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **准备配置文件**：

创建 ``input.yaml``：

.. code-block:: yaml

    api:
      key: "your_mp_api_key"
    elements:
      - "Ni"
      - "Cr"
    paths:
      base_dir: "./NiCr_training"
    deformation:
      scaling_factors: [0.9, 1.0, 1.1]
    perturbation:
      n_structures: 50

2. **执行完整工作流**：

.. code-block:: bash

    phymlp-kit full_workflow --input_file input.yaml

3. **训练模型**：

创建 ``Inputfile.txt``：

.. code-block:: none

    PhyMLP_load = "/path/to/phymlp"
    lmp_mpi_load = "/path/to/lmp_mpi"
    train = "true"
    extxyz_load = "./NiCr_training/Extxyz_set/final_dataset.extxyz"
    init_PhyMLP = "./10.PhyMLP"

执行训练：

.. code-block:: bash

    phymlp-kit train --train_input Inputfile.txt

4. **验证模型**：

修改 ``Inputfile.txt``：

.. code-block:: none

    train = "false"
    calculate = "true"
    crystal_structure = "fcc"
    lattice = "3.6"
    pot_PhyMLP_load = "./train/pot.PhyMLP"
    properties = "E-V"
    properties = "Elastic"

进阶用法
-------

自定义训练参数
~~~~~~~~~~~~~

.. code-block:: none

    # 高级训练选项
    iteration_limit = "5000"
    al_mode = "al"                    # 主动学习模式
    init_PhyMLP = "./16.PhyMLP"       # 更高复杂度的势函数

自定义VASP计算
~~~~~~~~~~~~~

.. code-block:: yaml

    vasp:
      incar_parameters:
        ENCUT: 520
        PREC: "Accurate"
        EDIFF: 1e-6
      submission:
        slurm_headers:
          - "#SBATCH -p gpu"
          - "#SBATCH --gres=gpu:2"

批量处理多个体系
~~~~~~~~~~~~~~~

创建多个配置文件夹：

.. code-block:: bash

    # Ni-Cr体系
    phymlp-kit full_workflow --input_file NiCr_input.yaml
    # Ni-Co体系
    phymlp-kit full_workflow --input_file NiCo_input.yaml
    # Cr-Co体系
    phymlp-kit full_workflow --input_file CrCo_input.yaml

故障排除
-------

常见问题
~~~~~~~

1. **Materials Project API 错误**：
   - 检查 API 密钥是否正确
   - 确认网络连接

2. **VASP 计算失败**：
   - 检查 POTCAR 文件路径
   - 验证 INCAR 参数

3. **内存不足**：
   - 减小 ``max_atoms`` 参数
   - 调整 VASP 计算资源

4. **训练不收敛**：
   - 增加 ``iteration_limit``
   - 调整训练参数

获取帮助
~~~~~~~

查看具体命令的帮助信息：

.. code-block:: bash

    phymlp-kit train -h
    phymlp-kit from_mp_structures -h

下一步
-----

- 查看 :doc:`高级配置 </advanced_configuration>`
- 学习 :doc:`性能优化 </performance_tuning>`
- 参考 :doc:`API 文档 </api/modules>`
>>>>>>> 7a6a5473e5cf811ab04cbe26f0f092ca4909e88c
