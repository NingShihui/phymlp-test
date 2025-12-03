训练和检验配置文件
==================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``Inputfile.txt`` 是 PhyMLP-MLP 机器学习势（Machine Learning Potential）训练和性质计算的主要配置文件。
它定义了软件路径、训练参数、计算选项和物性计算相关的所有关键参数。

配置文件采用键值对格式，以等号 ``=`` 分隔参数名和值，支持多行定义。

文件结构概览
------------

.. code-block:: text

   # 必须自定义的参数
   PhyMLP_load      = "/path/to/phymlp"
   lmp_mpi_load     = "/path/to/lmp_mpi"
   vaspkit_load     = "/path/to/vaspkit"

   # 训练过程参数设置
   train            = "TRUE"
   extxyz_load      = "./train.extxyz"
   init_PhyMLP      = "./10.PhyMLP"
   iteration_limit  = "5000"
   al_mode          = "nbh"

   # 性质计算参数设置
   calculate        = "true"
   crystal_structure= "bcc"
   lattice          = "3.5"
   atomic_mass      = "183.84"
   pot_PhyMLP_load  = "./train/pot.PhyMLP"
   properties       = "E-V"
   properties       = "Elastic"
   properties       = "phonon"
   properties       = "P-V"

详细参数说明
============

1. 必须自定义的参数
-------------------

这些参数是系统运行的基础，用户必须根据本地环境正确设置。

1.1 软件路径设置
~~~~~~~~~~~~~~~~

.. code-block:: text

   PhyMLP_load      = "/work/home/ningshihui/mlp-develop-phymlp/getset_train_validation/software/phymlp-mpi"
   lmp_mpi_load     = "/work/home/ningshihui/mlp-develop-phymlp/getset_train_validation/software/interface-lammps-mlp/lmp_mpi"
   vaspkit_load     = "/work/home/ningshihui/mlp-develop-phymlp/getset_train_validation/software/vaspkit.1.5.1/bin/vaspkit"

参数说明：

- **PhyMLP_load**：PhyMLP 框架的安装主目录，即编译时执行 ``./configure`` 的目录。
- **lmp_mpi_load**：LAMMPS 可执行文件 ``lmp_mpi`` 的完整路径。
- **vaspkit_load**：VASPKIT 可执行文件的完整路径。

注意事项：
- 这些路径必须使用绝对路径。
- 确保所有软件具有正确的执行权限。

2. 训练过程参数设置（可选自定义）
---------------------------------

这些参数控制机器学习势的训练过程。

2.1 基本训练控制
~~~~~~~~~~~~~~~~

.. code-block:: text

   train            = "TRUE"
   extxyz_load      = "./train.extxyz"
   init_PhyMLP      = "./10.PhyMLP"
   iteration_limit  = "5000"
   al_mode          = "nbh"

参数说明：

- **train**：是否执行训练。可选值：
  - ``"TRUE"`` 或 ``"true"``：执行训练
  - ``"FALSE"`` 或 ``"false"``：跳过训练
- **extxyz_load**：训练集文件路径，通常为 Extxyz 格式的结构-能量-力数据集。
- **init_PhyMLP**：初始势函数级别文件路径，用于提供训练起点。
- **iteration_limit**：最大迭代次数，默认值为 5000。
- **al_mode**：训练模式，可选值：
  - ``"nbh"``：邻域模式（默认）
  - 其他模式根据 PhyMLP 版本支持

2.2 输出说明
~~~~~~~~~~~~

训练完成后，势函数文件默认保存为：

::

   ./train/pot.PhyMLP

此文件将在后续性质计算中使用。

3. 性质计算参数设置（可选自定义）
---------------------------------

这些参数控制使用训练好的势函数进行各种物性计算。

3.1 基本计算控制
~~~~~~~~~~~~~~~~

.. code-block:: text

   calculate        = "true"
   crystal_structure= "bcc"
   lattice          = "3.5"
   atomic_mass      = "183.84"
   pot_PhyMLP_load  = "./train/pot.PhyMLP"

参数说明：

- **calculate**：是否执行性质计算。可选值：
  - ``"true"`` 或 ``"TRUE"``：执行计算
  - ``"false"`` 或 ``"FALSE"``：跳过计算
- **crystal_structure**：晶体结构类型。当前版本支持：
  - ``"fcc"``：面心立方
  - ``"bcc"``：体心立方（示例中使用的类型）
  - ``"hcp"``：六方最密堆积
- **lattice**：平衡晶格常数（单位：Å）。
- **atomic_mass**：元素的相对原子质量（单位：g/mol）。
- **pot_PhyMLP_load**：训练好的 PhyMLP 势函数文件路径。

3.2 物性计算选项
~~~~~~~~~~~~~~~~

物性计算通过多次定义 ``properties`` 参数来选择：

.. code-block:: text

   properties       = "E-V"      # 单原子能量-体积计算
   properties       = "Elastic"  # 弹性常数计算
   properties       = "phonon"   # 声子谱计算
   properties       = "P-V"      # 压力-体积计算

参数说明：

- **properties = "E-V"**：计算能量-体积曲线（E-V curve）。
- **properties = "Elastic"**：计算弹性常数，作为势函数性质的检验。
- **properties = "phonon"**：计算声子谱（phonon dispersion）。
- **properties = "P-V"**：计算压力-体积曲线（P-V curve）。

注意：
- 可以同时选择多个性质计算，程序将按顺序执行。
- 默认情况下，如果启用计算，会同时计算 ``"E-V"`` 和 ``"Elastic"``。

3.3 单位系统
~~~~~~~~~~~~

性质计算使用的默认单位系统：

- **长度**：埃（Å）
- **能量**：电子伏特（eV）
- **压强**：吉帕斯卡（GPa）
- **时间**：皮秒（ps）

配置示例
========

以下是一个完整的钨（W）体系配置示例：

.. code-block:: text

   ###必须自定义的参数###
   PhyMLP_load      = "/home/user/phymlp"
   lmp_mpi_load     = "/home/user/lammps/lmp_mpi"
   vaspkit_load     = "/home/user/vaspkit/bin/vaspkit"

   ###可选自定义的参数###
   ###训练过程参数设置##
   train            = "TRUE"
   extxyz_load      = "./W_train.extxyz"
   init_PhyMLP      = "./10.PhyMLP"
   iteration_limit  = "3000"
   al_mode          = "nbh"

   ###可选自定义的参数###
   ###性质计算参数设置####默认单位：长度埃，能量ev，压强GPa，时间ps
   calculate        = "true"
   crystal_structure= "bcc"
   lattice          = "3.165"
   atomic_mass      = "183.84"
   pot_PhyMLP_load  = "./train/pot.PhyMLP"
   properties       = "E-V"
   properties       = "Elastic"
   properties       = "phonon"

使用流程
========

1. **准备工作**：
   - 安装 PhyMLP、LAMMPS 和 VASPKIT
   - 准备训练数据集（Extxyz 格式）

2. **配置文件修改**：
   - 设置正确的软件路径
   - 指定训练集文件
   - 选择需要计算的性质

3. **执行程序**：
   - 程序将先进行势函数训练
   - 然后使用训练好的势进行性质计算

4. **结果获取**：
   - 训练结果保存在 ``./train/`` 目录
   - 性质计算结果保存在各自的输出文件中

常见问题
========

1. **路径错误**：
   - 确保所有软件路径使用绝对路径
   - 检查文件权限：``chmod +x /path/to/executable``

2. **训练失败**：
   - 检查训练集文件格式是否正确
   - 确认初始势函数级别文件存在

3. **计算失败**：
   - 检查晶格常数和晶体结构是否匹配
   - 确认势函数文件路径正确

4. **单位混淆**：
   - 注意输入参数的单位（如晶格常数单位为 Å）
   - 输出结果遵循默认单位系统

相关文档
========

- :ref:`extxyz_format` - 训练数据集格式说明
- :ref:`phymlp_training` - PhyMLP 训练详细流程
- :ref:`lammps_integration` - LAMMPS 与 PhyMLP 集成指南

版本说明
========

- 当前版本支持：fcc、bcc、hcp 晶体结构
- 默认计算单位：Å、eV、GPa、ps
- 支持多性质并行计算