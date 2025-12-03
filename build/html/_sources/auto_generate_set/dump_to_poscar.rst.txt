LAMMPS转POSCAR模块
======================================

概述
----

LAMMPS转POSCAR模块是一个用于将LAMMPS的dump文件转换为VASP POSCAR格式的工具。该模块支持批量处理、自动文件检测和灵活的原子类型映射，为分子动力学模拟结果的后续分析提供便利。

主要功能
--------

- **文件格式转换**: 将LAMMPS dump文件转换为VASP POSCAR格式
- **批量处理**: 支持目录批量转换和单文件转换
- **原子类型映射**: 自定义LAMMPS原子类型到元素符号的映射
- **智能检测**: 自动检测LAMMPS dump文件格式
- **配置驱动**: 支持YAML配置文件管理转换任务

核心类与方法
------------

LammpsToPoscarConverter 类
~~~~~~~~~~~~~~~~~~~~~~~~~

主转换器类，提供完整的转换功能。

**初始化**:
.. code-block:: python

   converter = LammpsToPoscarConverter()

set_atom_types_mapping 方法
~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``set_atom_types_mapping(type_mapping)``

**功能说明**:
设置LAMMPS原子类型到元素符号的映射关系。

**参数**:
- ``type_mapping`` (dict): 原子类型映射字典，格式为 {原子类型编号: '元素符号'}

**示例**:
.. code-block:: python

   converter.set_atom_types_mapping({
       1: 'Fe',
       2: 'Ni',
       3: 'Cr'
   })

read_dump_file 方法
~~~~~~~~~~~~~~~~~~~

**函数签名**: ``read_dump_file(file_path)``

**功能说明**:
读取LAMMPS dump文件并解析其中的结构信息。

**参数**:
- ``file_path`` (str): LAMMPS dump文件路径

**返回值**:
- ``dict``: 包含结构信息的字典，包含以下键：
  - ``timestep``: 时间步数
  - ``num_atoms``: 原子总数
  - ``box_bounds``: 模拟盒子边界
  - ``atoms``: 原子坐标、类型等信息列表

calculate_lattice_vectors 方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``calculate_lattice_vectors(box_bounds)``

**功能说明**:
从LAMMPS的盒子边界信息计算晶格矢量。

**参数**:
- ``box_bounds`` (list): 盒子边界列表，每个元素为 [min, max] 对

**返回值**:
- ``list``: 晶格矢量列表，格式为 [[x,0,0], [0,y,0], [0,0,z]]

sort_atoms_by_type 方法
~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``sort_atoms_by_type(atoms)``

**功能说明**:
按原子类型对原子进行分类和排序。

**参数**:
- ``atoms`` (list): 原子数据列表

**返回值**:
- ``defaultdict``: 按原子类型分组的原子坐标字典

convert_to_poscar 方法
~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``convert_to_poscar(data, output_file)``

**功能说明**:
将解析的数据转换为POSCAR格式并保存。

**参数**:
- ``data`` (dict): read_dump_file返回的结构数据
- ``output_file`` (str): 输出POSCAR文件路径

is_lammps_dump_file 方法
~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``is_lammps_dump_file(file_path)``

**功能说明**:
检查文件是否为有效的LAMMPS dump文件。

**参数**:
- ``file_path`` (str): 待检查文件路径

**返回值**:
- ``bool``: 如果是LAMMPS dump文件返回True，否则False

find_dump_files 方法
~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``find_dump_files(directory_path)``

**功能说明**:
查找目录中的所有LAMMPS dump文件。

**参数**:
- ``directory_path`` (str): 要搜索的目录路径

**返回值**:
- ``list``: 找到的dump文件路径列表

process_input 方法
~~~~~~~~~~~~~~~~~~

**函数签名**: ``process_input(input_path, output_dir=None)``

**功能说明**:
智能处理输入，自动识别是文件还是目录。

**参数**:
- ``input_path`` (str): 输入路径（文件或目录）
- ``output_dir`` (str, 可选): 输出目录，默认为输入目录

process_single_file 方法
~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``process_single_file(input_file, output_dir=None)``

**功能说明**:
处理单个LAMMPS dump文件。

**参数**:
- ``input_file`` (str): 输入dump文件路径
- ``output_dir`` (str, 可选): 输出目录

process_directory 方法
~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``process_directory(directory_path, output_dir=None)``

**功能说明**:
批量处理目录中的所有dump文件。

**参数**:
- ``directory_path`` (str): 输入目录路径
- ``output_dir`` (str, 可选): 输出目录

工具函数
--------

load_config 函数
~~~~~~~~~~~~~~~~

**函数签名**: ``load_config(config_file="input.yaml")``

**功能说明**:
从YAML文件加载配置信息。如果配置文件不存在，会自动创建默认配置。

**参数**:
- ``config_file`` (str): 配置文件路径，默认 "input.yaml"

**返回值**:
- ``dict`` 或 ``None``: 配置字典，如果创建了默认配置则返回None

convert_single_file 函数
~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``convert_single_file(input_file, output_file, atom_type_mapping=None)``

**功能说明**:
兼容性接口，转换单个文件。

**参数**:
- ``input_file`` (str): 输入文件路径
- ``output_file`` (str): 输出文件路径
- ``atom_type_mapping`` (dict, 可选): 原子类型映射

process_directory 函数
~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``process_directory(directory_path, output_dir=None)``

**功能说明**:
兼容性接口，批量处理目录。

**参数**:
- ``directory_path`` (str): 输入目录路径
- ``output_dir`` (str, 可选): 输出目录

parse_arguments 函数
~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``parse_arguments()``

**功能说明**:
解析命令行参数。

**返回值**:
- ``argparse.Namespace``: 解析后的参数对象

create_default_config 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``create_default_config(config_file="input.yaml")``

**功能说明**:
创建默认配置文件。

**参数**:
- ``config_file`` (str): 配置文件路径

配置文件结构
------------

配置文件采用YAML格式，包含以下主要部分：

.. code-block:: yaml

   # 原子类型映射
   atom_type_mapping:
     1: 'Fe'    # 类型1对应铁元素
     2: 'Ni'    # 类型2对应镍元素
     3: 'Cr'    # 类型3对应铬元素

   # 转换任务列表
   conversion_tasks:
     - input_path: './md_simulation'  # 输入路径（文件或目录）
       output_dir: './output_poscar'  # 输出目录
       description: '批量转换MD模拟结果'  # 任务描述

输出文件命名
------------

转换生成的POSCAR文件按以下规则命名：

.. code-block:: text

   POSCAR_{原始文件名}.vasp

例如，输入文件 ``npt.dump`` 会生成 ``POSCAR_npt.vasp``。

使用方式
--------

命令行使用
~~~~~~~~~~

.. code-block:: bash

   # 使用默认配置文件
   phymlp-kit dump_to_poscar --input_file config.yaml

   # 创建默认配置文件
   phymlp-kit dump_to_poscar --create_config

   # 指定自定义配置文件
   phymlp-kit dump_to_poscar --input_file my_config.yaml

Python脚本调用
~~~~~~~~~~~~~~

.. code-block:: python

   import dump_to_poscar

   # 方式1：直接运行（使用命令行参数）
   dump_to_poscar.main()

   # 方式2：指定配置文件运行
   dump_to_poscar.run_with_config("my_config.yaml")

   # 方式3：使用转换器对象
   converter = dump_to_poscar.LammpsToPoscarConverter()
   converter.set_atom_types_mapping({1: 'Fe', 2: 'Ni'})
   converter.process_directory("./md_results", "./poscar_output")

支持的文件格式
--------------

模块会自动检测以下扩展名的文件：

- ``*.dump``
- ``*.lammpstrj``
- ``*.lmp``
- ``*.dat``
- ``npt.*``
- ``*.txt``

注意事项
--------

1. **原子类型映射**: 必须正确设置原子类型到元素符号的映射
2. **盒子边界**: 仅支持正交盒子（orthogonal box）
3. **坐标格式**: 仅支持笛卡尔坐标
4. **时间步**: 每个dump文件只转换一个时间步的结构

常见问题
--------

Q1: 转换后的POSCAR元素符号不正确
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**解决方案**: 检查配置文件中的 ``atom_type_mapping`` 是否正确设置了原子类型编号与元素符号的对应关系。

Q2: 没有找到任何dump文件
~~~~~~~~~~~~~~~~~~~~~~~~

**解决方案**:
1. 确认文件扩展名是否被支持
2. 使用 ``is_lammps_dump_file`` 方法检查文件格式
3. 检查文件内容是否包含 "ITEM: TIMESTEP" 和 "ITEM: NUMBER OF ATOMS" 关键字

Q3: 盒子边界转换错误
~~~~~~~~~~~~~~~~~~~~

**解决方案**: 目前仅支持正交盒子（orthogonal box）。对于非正交盒子，需要先进行坐标变换。

依赖关系
--------

- **Python包**:
  - PyYAML: YAML配置文件解析
  - argparse: 命令行参数解析

- **文件格式**:
  - LAMMPS dump文件格式
  - VASP POSCAR文件格式

相关模块
--------

- :doc:`/phymlp/auto_generate_set/config` - 配置管理模块
- :doc:`/phymlp/converters/cfg2extxyz` - CFG到EXTXYZ转换器
- :doc:`/phymlp/converters/outcar_converter` - OUTCAR转换器