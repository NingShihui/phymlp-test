POTCAR生成器模块
===============

本模块用于自动生成VASP计算所需的POTCAR（赝势）文件，支持多种生成方法。

模块概述
--------

该模块提供了一组函数，用于：

1. 从POSCAR文件中正确读取元素种类和顺序
2. 查找各个元素对应的赝势文件
3. 拼接多个元素的POTCAR文件
4. 支持多种POTCAR生成方法（自动、pymatgen、手动）

主要函数说明
------------

read_poscar_elements(poscar_path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

读取POSCAR文件中的元素种类和顺序。

**参数：**
- ``poscar_path``: POSCAR文件路径

**返回：**
- 元素符号列表，如 ['Ba', 'Ti', 'O']

**作用：**
正确解析POSCAR格式，提取元素顺序信息，用于后续POTCAR文件查找。

find_potcar_files(potcar_base_dir, functional, elements, potcar_variants=None)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

查找每个元素对应的POTCAR文件路径。

**参数：**
- ``potcar_base_dir``: 赝势文件基础目录
- ``functional``: 泛函类型，如 'PBE'
- ``elements``: 元素符号列表
- ``potcar_variants``: 赝势变体字典（可选）

**返回：**
- POTCAR文件路径列表，按元素顺序排列

**作用：**
根据元素类型和泛函，在指定目录中查找对应的POTCAR文件，支持变体选择。

concatenate_potcar_files(potcar_paths, output_path)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

拼接多个POTCAR文件。

**参数：**
- ``potcar_paths``: 各个元素的POTCAR文件路径列表
- ``output_path``: 输出POTCAR文件路径

**返回：**
- 布尔值，表示是否成功

**作用：**
将多个元素的POTCAR文件按顺序拼接成一个完整的POTCAR文件。

generate_potcar_auto(poscar_path, config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

自动生成POTCAR文件。

**参数：**
- ``poscar_path``: POSCAR文件路径
- ``config``: 配置字典

**返回：**
- 布尔值，表示是否成功

**作用：**
整合读取元素、查找赝势、拼接文件的全过程，生成最终的POTCAR。

generate_potcar_pymatgen(structure, config)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

使用pymatgen生成POTCAR。

**参数：**
- ``structure``: pymatgen的Structure对象
- ``config``: 配置字典

**返回：**
- Potcar对象或None（失败时）

**作用：**
使用pymatgen库的Potcar类生成POTCAR文件。

generate_potcar(poscar_path, structure, config, output_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

主POTCAR生成函数。

**参数：**
- ``poscar_path``: POSCAR文件路径
- ``structure``: pymatgen的Structure对象
- ``config``: 配置字典
- ``output_dir``: 输出目录

**返回：**
- 布尔值，表示是否成功

**作用：**
根据配置选择不同的POTCAR生成方法，在指定目录中生成POTCAR文件。

配置参数说明
------------

配置文件需要包含以下POTCAR相关参数：

.. code-block:: yaml

    vasp:
        potcar:
            method: 'auto'           # 生成方法：auto, pymatgen, manual
            potcar_base_dir: '/path/to/potcar'  # 赝势文件基础目录
            functional: 'PBE'        # 泛函类型
            potcar_variants:         # 赝势变体设置
                O: 'O'               # 氧元素的赝势变体

使用方法
--------

.. code-block:: bash

    # 作为模块导入使用
    from potcar_generator import generate_potcar

    success = generate_potcar('POSCAR', structure, config, './output')

**自动模式（推荐）:**
1. 读取POSCAR中的元素
2. 在指定目录中查找对应的赝势文件
3. 按元素顺序拼接成POTCAR

**pymatgen模式:**
1. 使用pymatgen库生成POTCAR
2. 需要pymatgen正确配置赝势路径

**手动模式:**
1. 用户需提前准备好POTCAR文件
2. 程序仅验证文件是否存在

输出文件
--------

模块将在指定目录中生成：

- ``POTCAR``: 完整的赝势文件

注意事项
--------

1. 确保赝势文件目录结构正确
2. 元素顺序必须与POSCAR中的顺序一致
3. 自动模式需要完整的VASP赝势库
4. 使用绝对路径可避免文件查找问题