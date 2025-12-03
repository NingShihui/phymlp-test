结构微扰模块
============

本模块用于对结构进行扩胞和微扰生成，基于dpdata库实现。

模块概述
--------

该模块提供了一组函数，用于：

1. 自动寻找最优扩胞倍数
2. 创建超胞结构
3. 对结构进行晶格和原子位置的微扰
4. 生成大量微扰后的结构用于机器学习训练

主要函数说明
------------

find_optimal_supercell(structure, max_atoms=150, max_supercell=4)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

寻找最优的扩胞倍数，使原子数接近但不超过最大限制。

**参数：**
- ``structure``: pymatgen的Structure对象，原始晶体结构
- ``max_atoms``: 最大允许原子数（默认150）
- ``max_supercell``: 最大扩胞倍数（默认4）

**返回：**
- 扩胞倍数列表 [a, b, c]，三个方向上的扩胞倍数

**作用：**
自动计算最佳扩胞策略，优先考虑三个方向同时扩胞，不满足要求时再考虑单方向扩胞。

create_supercell(structure, scaling_matrix)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

创建超胞结构。

**参数：**
- ``structure``: pymatgen的Structure对象，原始晶体结构
- ``scaling_matrix``: 扩胞倍数列表 [a, b, c]

**返回：**
- 扩胞后的Structure对象

**作用：**
根据给定的扩胞倍数创建超胞。

process_structure_for_perturbation(poscar_path, output_base_dir, config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

处理单个结构进行扩胞和微扰。

**参数：**
- ``poscar_path``: POSCAR文件路径
- ``output_base_dir``: 输出文件的基础目录
- ``config``: 配置字典，包含微扰参数

**返回：**
- 生成的微扰结构数量

**作用：**
读取POSCAR文件，进行扩胞处理，然后使用dpdata生成微扰结构。

generate_perturbation_fallback(structure, output_dir, base_filename, perturb_params)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

备用微扰生成方法（使用pymatgen）。

**参数：**
- ``structure``: 要微扰的结构（Structure对象）
- ``output_dir``: 输出目录
- ``base_filename``: 基础文件名
- ``perturb_params``: 微扰参数字典

**返回：**
- 生成的微扰结构数量

**作用：**
当dpdata不可用时，使用pymatgen进行简单的随机微扰。

main(config_file="input.yaml")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

主函数，驱动整个扩胞和微扰过程。

**参数：**
- ``config_file``: 配置文件路径（默认"input.yaml"）

**返回：**
- 无返回值

**作用：**
加载配置，遍历所有POSCAR文件，对每个结构进行扩胞和微扰处理。

配置参数说明
------------

配置文件需要包含以下微扰相关参数：

.. code-block:: yaml

    perturbation:
        max_atoms: 150           # 扩胞后最大原子数
        max_supercell: 4         # 最大扩胞倍数
        n_structures: 100        # 每个结构生成的微扰结构数
        cell_pert_fraction: 0.05 # 晶格微扰幅度（相对变化）
        atom_pert_distance: 0.05 # 原子位置微扰距离（Å）
        atom_pert_style: 'uniform' # 微扰样式

使用示例
--------

.. code-block:: bash

    # 直接运行模块
    python perturb_structures.py --config_file input.yaml

    # 或在Python代码中调用
    from perturb_structures import main
    main("input.yaml")

输出文件结构
-----------

模块将生成以下目录结构：

::

    perturb/
    ├── BaTiO3/                   # 按化学式分类
    │   ├── BaTiO3_mp-2998/       # 按结构名称分类
    │   │   ├── BaTiO3_mp-2998_supercell.vasp        # 扩胞后的结构
    │   │   ├── BaTiO3_mp-2998_supercell_perturb_0001.vasp  # 微扰结构1
    │   │   ├── BaTiO3_mp-2998_supercell_perturb_0002.vasp  # 微扰结构2
    │   │   └── ...
    │   └── ...
    ├── SrTiO3/
    └── ...

注意事项
--------

1. 需要先运行结构下载模块生成基础POSCAR文件
2. 依赖dpdata库进行微扰，备选使用pymatgen
3. 微扰结构按化学式和组织结构名称分类，便于管理
4. 每个原始结构生成的微扰结构数量由配置控制