自动化获取训练集配置文件
==================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``input.yaml`` 是 phymlp-kit 工具包的核心配置文件，用于定义从材料结构获取、VASP 计算、拟合分析到数据集生成的全流程参数。
用户通过修改此文件来自定义任务流程、计算参数和输出路径。

配置文件采用 YAML 格式，所有参数均为键值对形式，支持嵌套结构。

文件结构概览
------------

.. code-block:: yaml

   api:
     key: "your_api_key"
   elements:
     - "W"
   paths:
     ...
   user_poscar:
     ...
   deformation:
     ...
   perturbation:
     ...
   atom_type_mapping:
     ...
   conversion_tasks:
     ...
   vasp_setup:
     ...
   vasp:
     ...
   birch_murnaghan_fitting:
     ...
   experimental_pv_fitting:
     ...
   extxyz_generation:
     ...


详细参数说明
============

1. Materials Project API 配置
---------------------------

.. code-block:: yaml

   api:
     key: "pyDazqp7LIcTyIdMuckJiddBS7xKm0oa"

参数说明：

- **key**：Materials Project 网站的 API 密钥，用户需替换为自己的有效密钥。

2. 元素配置
-----------

.. code-block:: yaml

   elements:
     - "W"

参数说明：

- **elements**：体系包含的元素类型列表，例如 ``["W"]`` 表示只包含钨元素。

3. 输出路径配置
---------------

.. code-block:: yaml

   paths:
     base_dir: "./materials_project"
     cif_dir: "base/dir_CIF"
     poscar_dir: "base/dir_POSCAR"
     deform_dir: "deform"
     birch_murnaghan_dir: "Birch_Murnaghan_fit"
     extxyz_set_dir: "Extxyz_set"

参数说明：

- **base_dir**：基础输出目录，所有子目录的根路径。
- **cif_dir**：CIF 文件存放目录。
- **poscar_dir**：POSCAR 文件存放目录。
- **deform_dir**：形变结构存放目录。
- **birch_murnaghan_dir**：Birch-Murnaghan 拟合结果目录。
- **extxyz_set_dir**：Extxyz 数据集目录。

4. 用户自定义 POSCAR 配置
------------------------

.. code-block:: yaml

   user_poscar:
     enabled: true
     source_dir: "./input-poscar"

参数说明：

- **enabled**：是否启用用户自定义 POSCAR 结构，默认为 ``false``。
- **source_dir**：当启用时，指定存放自定义 POSCAR 文件的目录路径。

5. 形变参数配置
---------------

.. code-block:: yaml

   deformation:
     max_atoms: 150
     scaling_factors: [0.8, 0.9, 1.0, 1.1, 1.2]
     max_supercell: 4

参数说明：

- **max_atoms**：最大原子数限制。
- **scaling_factors**：晶格缩放系数列表，用于生成拉伸或压缩的结构。
- **max_supercell**：最大扩胞倍数。

6. 微扰参数配置
---------------

.. code-block:: yaml

   perturbation:
     max_atoms: 150
     max_supercell: 4
     n_structures: 100
     cell_pert_fraction: 0.05
     atom_pert_distance: 0.05
     atom_pert_style: "uniform"

参数说明：

- **max_atoms**：最大原子数限制。
- **max_supercell**：最大扩胞倍数。
- **n_structures**：生成的微扰结构数量。
- **cell_pert_fraction**：盒子微扰比例。
- **atom_pert_distance**：原子坐标扰动距离（单位：Å）。
- **atom_pert_style**：扰动样式，可选 ``uniform`` 或 ``const``。

7. 经验势函数结构转换配置
-----------------------

.. code-block:: yaml

   atom_type_mapping:
     1: W
   conversion_tasks:
     - input_path: "./fs_potential_md/dump_files"
       output_dir: "./fs_dump_to_poscar_output"
       description: "批量转换目录中的所有dump文件"

参数说明：

- **atom_type_mapping**：LAMMPS 中原子类型与元素符号的映射，例如 ``1: W`` 表示类型 1 对应钨元素。
- **conversion_tasks**：转换任务列表，每个任务包含：
   - **input_path**：输入路径（可为文件或目录）。
   - **output_dir**：输出目录。
   - **description**：任务描述。

8. VASP 计算配置
--------------

8.1 VASP 任务设置
~~~~~~~~~~~~~~~~

.. code-block:: yaml

   vasp_setup:
     input_paths:
       - "./fs_to_poscar_output"
     output_dir: "./vasp_calculations"
     prefix: "calc"

参数说明：

- **input_paths**：输入路径列表，支持多个路径。
- **output_dir**：VASP 计算结果输出目录。
- **prefix**：计算目录名前缀。

8.2 VASP 参数配置
~~~~~~~~~~~~~~~~

.. code-block:: yaml

   vasp:
     incar_parameters:
       ALGO: "normal"
       EDIFF: 1E-3
       KSPACING: 0.2
       ENCUT: 400
       ISIF: 2
       ISMEAR: 1
       NELM: 400
       NSW: 0
       PREC: "Accurate"
       SIGMA: 0.1
       NCORE: 32
       KPAR: 2
       LREAL: "Auto"
     potcar:
       method: "auto"
       potcar_base_dir: "G:/mlp-train/.../POTCAR/"
       functional: "PBE"
       potcar_variants: {}
     submission:
       slurm_headers:
         - "#SBATCH -N 1"
         - "#SBATCH -n 32"
       modules:
         - "module purge"
         - "module load vasp-6.3.2-intelmpi2017_optcell"
       environment:
         - "export MKL_DEBUG_CPU_TYPE=5"
       vasp_execution:
         - "srun --mpi=pmi2 vasp_std"
       max_batch_size: 10
       check_interval: 60

参数说明：

- **incar_parameters**：INCAR 文件参数，用户可根据需要修改。
- **potcar**：POTCAR 配置，包括方法、基目录和泛函。
- **submission**：作业提交配置，支持自定义 SLURM 头、模块加载、环境变量和 VASP 执行命令。
   - **max_batch_size**：每批次同时运行的最大任务数。
   - **check_interval**：检查后台任务状态的间隔时间（秒）。

9. Birch-Murnaghan 拟合配置
--------------------------

.. code-block:: yaml

   birch_murnaghan_fitting:
     source:
       root_dir: "./materials_project/vasp_calculations/deform/"
       search_recursive: true
     results:
       root_dir: "./Birch_Murnaghan_fit"
     data_filter:
       pressure_range: [-100, 100]
       energy_range: [-100, 10]
     fitting:
       initial_guess:
         E0: "auto"
         V0: "auto"
         B0: 100
         B1: 4.0
       optimization:
         max_iterations: 1000
         tolerance: 1e-6
     output:
       save_plot: true
       plot_format: "png"

参数说明：

- **source**：数据源目录配置。
- **results**：拟合结果目录。
- **data_filter**：数据筛选条件，包括压力和能量范围。
- **fitting**：拟合参数配置，包括初始猜测和优化设置。
- **output**：输出配置，支持保存图像和参数文件。

10. 实验 P-V 数据拟合配置
------------------------

.. code-block:: yaml

   experimental_pv_fitting:
     DFT_a0: 3.524
     EXP_data_file: "EXP.data"
     output_directory: "./exp_pv_fitting"
     num_fit_points: 1000
     polynomial_degree: 4

参数说明：

- **DFT_a0**：DFT 计算的零压晶格常数。
- **EXP_data_file**：实验数据文件路径。
- **output_directory**：输出目录。
- **num_fit_points**：拟合曲线点数。
- **polynomial_degree**：多项式拟合阶数。

11. Extxyz 数据集生成配置
-----------------------

.. code-block:: yaml

   extxyz_generation:
     vasp:
       outcar_search_dir: "./vasp_calculations"
       search_recursive: true
       extraction_step: 1
     birch_murnaghan:
       fitting_results_dir: "./Birch_Murnaghan_fit"
       search_recursive: false
       volume_range: "auto"
       n_structures_per_fit: 50
       include_original_points: true
       use_outcar_structures: true
       scaling_factors: [0.8, 1.2]
       pressure_filter:
         enabled: true
         pressure_range: [-100, 100]
     fit_a_P:
       reference_structure: "./init.extxyz"
       fit_a_P_data: "./exp_pv_fitting/fit_a_P.data"
       pressure_range: [0, 100]
       n_structures: 200

参数说明：

- **vasp**：从 OUTCAR 提取结构的配置。
- **birch_murnaghan**：基于 Birch-Murnaghan 拟合生成结构的配置。
- **fit_a_P**：基于实验拟合数据生成结构的配置。

使用示例
========

以下是一个针对钨体系的配置示例：

.. code-block:: yaml

   api:
     key: "your_own_api_key"
   elements:
     - "W"
   paths:
     base_dir: "./tungsten_project"
   user_poscar:
     enabled: false
   deformation:
     scaling_factors: [0.85, 0.95, 1.0, 1.05, 1.15]
   vasp_setup:
     input_paths:
       - "./tungsten_structures"
     output_dir: "./tungsten_vasp"

注意事项
========

1. 所有路径均可自定义，建议使用绝对路径或相对于当前工作目录的相对路径。
2. 若启用用户自定义 POSCAR，请确保 ``source_dir`` 中存在有效的 POSCAR 文件。
3. VASP 计算部分需根据实际集群环境调整 SLURM 参数和模块加载命令。
4. 拟合部分的数据筛选范围可根据实际计算数据范围调整。
5. 批量转换和生成任务支持多任务并发，可通过 ``max_batch_size`` 控制。

相关文档
========

- :ref:`vasp_calculations`
- :ref:`birch_murnaghan_fitting`
- :ref:`extxyz_generation`