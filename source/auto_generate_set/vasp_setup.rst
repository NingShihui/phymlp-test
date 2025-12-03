VASP计算设置模块
===============

本模块用于自动设置VASP计算任务，支持多个输入路径和灵活的输出配置。

模块概述
--------

该模块提供了一组函数，用于：

1. 自动发现结构文件和目录
2. 创建VASP计算所需的所有输入文件
3. 保持原有的目录分类结构
4. 生成可自定义的提交脚本

主要函数说明
------------

create_incar(config)
^^^^^^^^^^^^^^^^^^^^

创建INCAR文件。

**参数：**
- ``config``: 配置字典，包含INCAR参数

**返回：**
- Incar对象

**作用：**
根据配置参数生成VASP的INCAR输入文件。

setup_vasp_calculation(poscar_path, output_dir, config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

为单个结构设置VASP计算。

**参数：**
- ``poscar_path``: POSCAR文件路径
- ``output_dir``: 输出目录路径
- ``config``: 配置字典

**返回：**
- 布尔值，表示设置是否成功

**作用：**
为单个结构创建完整的VASP计算目录，包括POSCAR、INCAR、POTCAR和提交脚本。

create_submission_script(output_dir, config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建完全可自定义的SLURM提交脚本。

**参数：**
- ``output_dir``: 输出目录路径
- ``config``: 配置字典，包含提交脚本配置

**返回：**
- 无返回值

**作用：**
根据配置文件生成适应不同HPC环境的SLURM提交脚本。

discover_structure_dirs(input_paths)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

自动发现所有输入路径中的结构目录。

**参数：**
- ``input_paths``: 输入路径列表

**返回：**
- 发现的目录信息列表，每个元素包含name、path、prefix、type等信息

**作用：**
扫描输入路径，识别包含.vasp文件的目录，为后续处理做准备。

process_directory_for_vasp(input_dir, output_base_dir, config, prefix="")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

处理整个目录的结构用于VASP计算。

**参数：**
- ``input_dir``: 输入目录路径
- ``output_base_dir``: 输出基础目录
- ``config``: 配置字典
- ``prefix``: 目录前缀（可选）

**返回：**
- 设置的计算任务数量

**作用：**
遍历目录中的所有.vasp文件，为每个结构设置VASP计算，保持原有目录结构。

配置参数说明
------------

配置文件需要包含以下VASP设置相关参数：

.. code-block:: yaml

    vasp_setup:
        input_paths:        # 输入路径列表
            - './deformed_structures'
            - './perturbed_structures'
        output_dir: './vasp_calculations'  # 输出目录

    vasp:
        incar_parameters:   # INCAR参数
            PREC: 'Accurate'
            ENCUT: 500
            ...
        submission:         # 提交脚本配置
            slurm_headers:
                - '#SBATCH --job-name=vasp_calculation'
                - '#SBATCH --nodes=1'
            modules:
                - 'module load vasp/5.4.4'
            vasp_execution:
                - 'srun vasp_std'

输入输出结构
-----------

**输入结构：**
任意包含.vasp文件的目录结构，如：

::

    deformed_structures/
    ├── BaTiO3/
    │   ├── BaTiO3_mp-2998_supercell.vasp
    │   └── BaTiO3_mp-2998_perturb_0001.vasp
    └── SrTiO3/
        └── SrTiO3_mp-5229.vasp

**输出结构：**
保持原有结构，每个结构一个计算目录：

::

    vasp_calculations/
    ├── BaTiO3/
    │   ├── BaTiO3_mp-2998_supercell/
    │   │   ├── POSCAR
    │   │   ├── INCAR
    │   │   ├── POTCAR
    │   │   └── submit.sh
    │   └── BaTiO3_mp-2998_perturb_0001/
    └── SrTiO3/
        └── SrTiO3_mp-5229/

使用示例
--------

.. code-block:: bash

    # 直接运行模块
    python vasp_setup.py

    # 或在Python代码中调用
    from vasp_setup import main
    main("input.yaml")

注意事项
--------

1. 需要正确配置INCAR参数以适应计算需求
2. POTCAR生成依赖potcar_generator模块
3. 提交脚本需要根据实际HPC环境调整配置
4. 已完成的计算（存在OUTCAR）会自动跳过
5. 保持原有目录结构便于数据管理和追溯