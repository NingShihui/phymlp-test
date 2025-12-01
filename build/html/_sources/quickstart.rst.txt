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