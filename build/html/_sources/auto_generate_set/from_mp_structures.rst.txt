Materials Project结构获取模块
==================================================

概述
----

Materials Project结构获取模块用于从Materials Project数据库中检索和下载晶体结构数据。该模块支持批量下载体相结构和表面结构，并自动进行格式转换和元素排序，为后续的机器学习势训练提供高质量的初始结构数据。

主要功能
--------

- **Materials Project API访问**: 通过API密钥访问Materials Project数据库
- **多元素组合检索**: 自动生成所有可能的元素组合进行搜索
- **体相结构下载**: 下载材料的体相晶体结构
- **表面结构生成**: 自动生成对称性不同的表面结构
- **格式转换**: 将结构转换为CIF和POSCAR格式
- **元素排序**: 自动对POSCAR文件中的元素进行排序和合并

核心函数
--------

write_poscar_grouped_by_element 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``write_poscar_grouped_by_element(structure, filepath)``

**功能说明**:
将晶体结构按元素种类排序并写入POSCAR文件，合并相同的元素行。

**参数**:
- ``structure`` (pymatgen.Structure): 输入的晶体结构对象
- ``filepath`` (str): 输出POSCAR文件路径

**处理流程**:
1. 对结构中的原子按元素种类排序
2. 统计每种元素的数量
3. 生成合并后的元素符号行和数量行
4. 写入格式化的POSCAR文件

copy_user_poscars 函数
~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``copy_user_poscars(source_dir, target_dir, elements)``

**功能说明**:
复制用户自定义的POSCAR文件到目标目录，并检查文件是否包含指定元素。

**参数**:
- ``source_dir`` (str): 用户自定义POSCAR源目录
- ``target_dir`` (str): 目标目录
- ``elements`` (list): 需要检查的元素列表

**返回值**:
- ``int``: 复制的文件数量

search_with_retry 函数
~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``search_with_retry(mpr, chemsys, max_retries=3, delay=5)``

**功能说明**:
带重试机制的Materials Project搜索函数，处理网络连接问题。

**参数**:
- ``mpr`` (MPRester): Materials Project客户端对象
- ``chemsys`` (str): 化学体系字符串（如"Fe-O"）
- ``max_retries`` (int): 最大重试次数，默认3
- ``delay`` (int): 重试延迟时间（秒），默认5

**返回值**:
- ``list``: 搜索到的材料文档列表

get_available_surface_structures 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``get_available_surface_structures(mpr, material_id)``

**功能说明**:
从Materials Project获取材料的表面结构数据。

**参数**:
- ``mpr`` (MPRester): Materials Project客户端对象
- ``material_id`` (str): 材料ID（如"mp-12345"）

**返回值**:
- ``list``: 表面结构对象列表

generate_basic_surfaces 函数
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**函数签名**: ``generate_basic_surfaces(material_id, mpr)``

**功能说明**:
当Materials Project没有表面结构数据时，自动生成基本的表面结构。

**参数**:
- ``material_id`` (str): 材料ID
- ``mpr`` (MPRester): Materials Project客户端对象

**返回值**:
- ``list``: 生成的表面结构列表

**生成方法**:
使用pymatgen的SlabGenerator生成对称性不同的米勒指数表面

main 函数
~~~~~~~~~

**函数签名**: ``main(config_file="input.yaml")``

**功能说明**:
模块主函数，执行完整的Materials Project结构获取流程。

**参数**:
- ``config_file`` (str): 配置文件路径，默认"input.yaml"

**执行流程**:
1. 加载配置文件
2. 创建目录结构
3. 遍历所有元素组合
4. 下载体相和表面结构
5. 转换为CIF和POSCAR格式
6. 复制用户自定义POSCAR文件
7. 生成总结报告

配置参数
--------

主要配置参数位于配置文件中：

.. code-block:: yaml

   # API配置
   api:
     key: "your_materials_project_api_key"  # Materials Project API密钥

   # 元素列表
   elements: ["Fe", "Ni", "Cr"]  # 要搜索的元素

   # 用户自定义POSCAR配置
   user_poscar:
     enabled: true  # 是否启用用户自定义POSCAR
     source_dir: "./user_structures"  # 用户自定义结构源目录

目录结构
--------

模块运行后创建以下目录结构：

.. code-block:: text

   materials_project/
   ├── base/
   │   ├── dir_CIF/
   │   │   └── [化学式]/
   │   │       └── [材料]-[mp_id].cif
   │   └── dir_POSCAR/
   │       └── [化学式]/
   │           └── [材料]-[mp_id].vasp
   ├── surface/
   │   ├── dir_CIF/
   │   └── dir_POSCAR/
   ├── user_poscar/
   │   └── dir_POSCAR/
   └── summary.txt

文件名格式
----------

生成的POSCAR文件遵循以下命名规则：

- **体相结构**: ``{formula}-{material_id}.vasp``
  例如: ``Fe2O3-mp-12345.vasp``

- **表面结构**: ``{formula}-{material_id}_surface_{index}.vasp``
  例如: ``Fe2O3-mp-12345_surface_1.vasp``

使用方式
--------

命令行调用
~~~~~~~~~~

.. code-block:: bash

   # 通过phymlp-kit调用
   phymlp-kit from_mp_structures --input_file config.yaml

Python脚本调用
~~~~~~~~~~~~~~

.. code-block:: python

   import from_mp_structures

   # 直接运行
   from_mp_structures.main("my_config.yaml")

   # 或分步处理
   from config import load_config
   config = load_config("my_config.yaml")
   API_KEY = config['api']['key']
   elements = config['elements']

API密钥获取
-----------

1. 访问 https://materialsproject.org
2. 注册账户并登录
3. 在个人设置中生成API密钥
4. 在配置文件中配置API密钥

输出文件说明
------------

1. **summary.txt**: 总结文件
   - 格式：化学式 | 基础结构数量 | 表面结构数量

2. **CIF文件**: 晶体信息文件
   - 用于结构可视化和分析

3. **POSCAR文件**: VASP输入文件
   - 已按元素排序和合并
   - 可直接用于第一性原理计算

依赖关系
--------

- **Python包**:
  - mp-api: Materials Project API客户端
  - pymatgen: 材料结构处理
  - requests: HTTP请求库

- **外部依赖**:
  - 有效的Materials Project API密钥
  - 互联网连接

常见问题
--------

Q1: API密钥无效或过期
~~~~~~~~~~~~~~~~~~~~~

**解决方案**:
1. 检查API密钥是否正确配置
2. 在Materials Project网站上重新生成API密钥
3. 确认账户是否有效

Q2: 网络连接失败
~~~~~~~~~~~~~~~~

**解决方案**:
1. 检查网络连接
2. 函数内置重试机制会自动重试
3. 调整配置文件中的网络参数

Q3: 元素组合太多导致超时
~~~~~~~~~~~~~~~~~~~~~~~~

**解决方案**:
1. 减少元素列表中的元素数量
2. 分批处理不同的元素组合
3. 增加网络请求的超时时间

Q4: 表面结构生成失败
~~~~~~~~~~~~~~~~~~~~

**解决方案**:
1. 检查pymatgen的surface模块是否可用
2. 简化表面生成参数
3. 使用已有的表面结构数据

注意事项
--------

1. **API限制**: Materials Project API有使用限制，请合理使用
2. **文件组织**: 结构按化学式组织，便于管理和查找
3. **格式兼容**: 生成的POSCAR文件已优化格式，兼容VASP
4. **数据更新**: Materials Project数据库定期更新，结构可能变化

相关模块
--------

- :doc:`/phymlp/auto_generate_set/config` - 配置管理模块
- :doc:`/phymlp/auto_generate_set/deform_structures` - 形变结构生成
- :doc:`/phymlp/auto_generate_set/perturb_structures` - 微扰结构生成