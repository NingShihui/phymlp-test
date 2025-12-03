.. _split_set_module:

=========================
split_set 模块说明
=========================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``split_set.py`` 模块是 PhyMLP Kit 工具包中的关键数据处理工具，专门用于将 EXTXYZ 格式的原子结构数据集分割为训练集和验证集。该模块是机器学习势训练工作流中数据准备阶段的核心组件。

功能特性
========

.. list-table:: 主要功能特性
   :widths: 30 70
   :header-rows: 1

   * - 特性
     - 描述
   * - 随机分割
     - 完全随机打乱数据集，确保统计无偏性
   * - 比例可控
     - 可精确控制验证集比例（0.0-1.0）
   * - 格式保持
     - 保持 EXTXYZ 格式完整，不丢失任何元数据
   * - 高效处理
     - 支持处理包含数万结构的大型数据集
   * - 简单易用
     - 提供命令行和 Python API 两种使用方式

快速开始
========

基本使用方式
------------

.. code-block:: bash

   # 方式1：通过 phymlp-kit 命令行
   phymlp-kit split_set --input_file full.extxyz --val_ratio 0.2

   # 方式2：直接运行 Python 脚本
   python split_set.py --input full.extxyz --val_ratio 0.15

   # 方式3：在 Python 代码中导入
   from phymlp.tools.split_set import split_extxyz_structures
   split_extxyz_structures("full.extxyz", "train.extxyz", "val.extxyz", 0.1)

命令行参数详解
--------------

.. list-table:: 命令行参数说明
   :widths: 20 30 50
   :header-rows: 1

   * - 参数
     - 缩写
     - 描述
   * - ``--input_file``
     - ``-i``
     - 输入 EXTXYZ 文件路径（必需）
   * - ``--set_train``
     - ``-t``
     - 训练集输出文件名（默认: train.extxyz）
   * - ``--set_val``
     - ``-v``
     - 验证集输出文件名（默认: validation.extxyz）
   * - ``--val_ratio``
     - ``-r``
     - 验证集比例（默认: 0.1）
   * - ``--help``
     - ``-h``
     - 显示帮助信息

核心函数详解
============

split_extxyz_structures 函数
----------------------------

.. py:function:: split_extxyz_structures(input_file, train_file, validation_file, validation_ratio)

   主功能函数：分割 EXTXYZ 结构数据集

   :param str input_file: 输入 EXTXYZ 文件路径
   :param str train_file: 训练集输出文件路径
   :param str validation_file: 验证集输出文件路径
   :param float validation_ratio: 验证集比例（0.0 到 1.0 之间）
   :raises FileNotFoundError: 当输入文件不存在时
   :raises ValueError: 当验证集比例不在有效范围内时
   :returns: None

   **函数执行流程**：

   1. **文件读取与解析**

      .. code-block:: python

         structures = []          # 存储所有结构
         current_struct = []      # 当前正在读取的结构

         with open(input_file, 'r') as f:
             for line in f:
                 stripped = line.strip()
                 if stripped.isdigit():  # 检测结构开始（原子数行）
                     if current_struct:  # 保存前一个结构
                         structures.append(current_struct)
                         current_struct = []
                     current_struct.append(line)
                 else:  # 结构内容行
                     current_struct.append(line)

             # 保存最后一个结构
             if current_struct:
                 structures.append(current_struct)

   2. **随机化处理**

      .. code-block:: python

         import random
         random.shuffle(structures)  # 随机打乱结构顺序

   3. **比例计算与分割**

      .. math::

         N_{\text{total}} = \text{len(structures)} \\
         N_{\text{train}} = \lfloor N_{\text{total}} \times (1 - r_{\text{val}}) \rfloor \\
         N_{\text{val}} = N_{\text{total}} - N_{\text{train}}

         其中：\\
         r_{\text{val}} = \text{validation_ratio}

      .. code-block:: python

         split_idx = int(len(structures) * (1 - validation_ratio))
         train_set = structures[:split_idx]    # 训练集部分
         val_set = structures[split_idx:]      # 验证集部分

   4. **文件写入**

      .. code-block:: python

         # 写入训练集
         with open(train_file, 'w') as f:
             for struct in train_set:
                 f.write(''.join(struct))  # 合并结构行

         # 写入验证集
         with open(validation_file, 'w') as f:
             for struct in val_set:
                 f.write(''.join(struct))

         # 输出统计信息
         print(f"训练集写入完成，样本数量: {len(train_set)}")
         print(f"验证集写入完成，样本数量: {len(val_set)}")

EXTXYZ 格式详解
===============

格式概述
--------

EXTXYZ（Extended XYZ）格式是标准 XYZ 格式的扩展，支持存储丰富的计算数据：

.. code-block:: text
   :caption: EXTXYZ 文件结构示例

   # 结构1
   2                                                                          # 原子数
   Lattice="5.0 0.0 0.0 0.0 5.0 0.0 0.0 0.0 5.0" Properties=species:S:1:pos:R:3 energy=-10.5 free_energy=-10.5
   W       0.000000       0.000000       0.000000                             # 原子1
   W       2.500000       2.500000       2.500000                             # 原子2

   # 结构2
   3                                                                          # 原子数
   Lattice="4.5 0.0 0.0 0.0 4.5 0.0 0.0 0.0 4.5" Properties=species:S:1:pos:R:3 energy=-15.2 free_energy=-15.2
   W       0.000000       0.000000       0.000000
   W       2.250000       2.250000       2.250000
   W       0.000000       2.250000       2.250000

关键字段说明
------------

.. list-table:: EXTXYZ 关键字段
   :widths: 25 75
   :header-rows: 1

   * - 字段
     - 说明
   * - 原子数行
     - 纯数字，表示该结构的原子总数
   * - 注释行
     - 包含丰富的元数据：
       - **Lattice**：晶格向量（9个数字）
       - **Properties**：属性定义（物种、坐标等）
       - **energy**：总能（eV）
       - **free_energy**：自由能（eV）
       - 其他自定义属性
   * - 原子行
     - 每行包含：元素符号 + X坐标 + Y坐标 + Z坐标

格式解析逻辑
------------

模块使用以下逻辑识别结构边界：

1. **结构开始**：遇到纯数字行（原子数）
2. **结构内容**：直到下一个纯数字行之前的所有行
3. **结构结束**：遇到下一个结构的开始或文件结束

使用示例
========

基础示例
--------

.. code-block:: python
   :caption: 基础数据集分割

   #!/usr/bin/env python3
   """基础数据集分割示例"""

   from phymlp.tools.split_set import split_extxyz_structures

   def main():
       # 输入文件
       input_file = "all_structures.extxyz"

       # 输出文件
       train_file = "training_set.extxyz"
       validation_file = "validation_set.extxyz"

       # 验证集比例（20%）
       validation_ratio = 0.2

       # 执行分割
       split_extxyz_structures(
           input_file=input_file,
           train_file=train_file,
           validation_file=validation_file,
           validation_ratio=validation_ratio
       )

       print("数据集分割完成！")
       print(f"训练集: {train_file}")
       print(f"验证集: {validation_file}")

   if __name__ == "__main__":
       main()

高级使用示例
------------

.. code-block:: python
   :caption: 多比例分割实验

   def experiment_with_different_ratios():
       """尝试不同的验证集比例"""

       input_file = "dataset.extxyz"
       ratios = [0.05, 0.1, 0.15, 0.2, 0.25]

       for ratio in ratios:
           # 生成文件名
           train_file = f"train_{int(ratio*100)}pct.extxyz"
           val_file = f"val_{int(ratio*100)}pct.extxyz"

           print(f"\n使用验证集比例: {ratio*100}%")

           # 执行分割
           split_extxyz_structures(
               input_file=input_file,
               train_file=train_file,
               validation_file=val_file,
               validation_ratio=ratio
           )

           # 统计信息
           count_structures(train_file, f"训练集 ({train_file})")
           count_structures(val_file, f"验证集 ({val_file})")

   def count_structures(filename, label):
       """统计EXTXYZ文件中的结构数"""
       count = 0
       with open(filename, 'r') as f:
           for line in f:
               if line.strip().isdigit():
                   count += 1
       print(f"  {label}: {count} 个结构")

集成到训练工作流
----------------

.. code-block:: python
   :caption: 完整的数据准备流程

   def prepare_training_data():
       """完整的训练数据准备流程"""

       print("=" * 50)
       print("数据准备流程开始")
       print("=" * 50)

       # 1. 收集原始数据
       print("\n步骤1: 收集原始计算数据...")
       raw_files = collect_vasp_results()

       # 2. 转换为EXTXYZ格式
       print("\n步骤2: 转换为EXTXYZ格式...")
       for vasp_dir in raw_files:
           convert_outcar_to_extxyz(vasp_dir)

       # 3. 合并所有数据
       print("\n步骤3: 合并数据集...")
       merge_extxyz_files("raw_data/", "combined.extxyz")

       # 4. 数据清洗
       print("\n步骤4: 数据清洗...")
       clean_dataset("combined.extxyz", "cleaned.extxyz")

       # 5. 数据集分割
       print("\n步骤5: 分割训练集和验证集...")
       split_extxyz_structures(
           input_file="cleaned.extxyz",
           train_file="final_train.extxyz",
           validation_file="final_validation.extxyz",
           validation_ratio=0.15  # 15%验证集
       )

       # 6. 最终验证
       print("\n步骤6: 验证数据集...")
       validate_datasets("final_train.extxyz", "final_validation.extxyz")

       print("\n" + "=" * 50)
       print("数据准备完成！")
       print("=" * 50)

带随机种子的分割
----------------

.. code-block:: python
   :caption: 可重复的数据分割

   import random

   def split_with_random_seed(input_file, train_file, val_file, val_ratio, seed=42):
       """带随机种子的可重复分割"""

       # 设置随机种子
       random.seed(seed)

       # 读取结构
       structures = []
       current_struct = []

       with open(input_file, 'r') as f:
           for line in f:
               stripped = line.strip()
               if stripped.isdigit():
                   if current_struct:
                       structures.append(current_struct)
                       current_struct = []
                   current_struct.append(line)
               else:
                   current_struct.append(line)

           if current_struct:
               structures.append(current_struct)

       # 打乱顺序（受随机种子控制）
       random.shuffle(structures)

       # 分割
       split_idx = int(len(structures) * (1 - val_ratio))
       train_set = structures[:split_idx]
       val_set = structures[split_idx:]

       # 写入文件
       with open(train_file, 'w') as f:
           for struct in train_set:
               f.write(''.join(struct))

       with open(val_file, 'w') as f:
           for struct in val_set:
               f.write(''.join(struct))

       print(f"使用随机种子: {seed}")
       print(f"训练集: {len(train_set)} 个结构")
       print(f"验证集: {len(val_set)} 个结构")

       return len(train_set), len(val_set)

错误处理机制
============

输入文件检查
------------

.. code-block:: python

   import os

   def validate_input_file(input_file):
       """验证输入文件"""

       if not os.path.exists(input_file):
           raise FileNotFoundError(f"输入文件不存在: {input_file}")

       if not os.path.isfile(input_file):
           raise ValueError(f"输入路径不是文件: {input_file}")

       if os.path.getsize(input_file) == 0:
           raise ValueError(f"输入文件为空: {input_file}")

比例参数验证
------------

.. code-block:: python

   def validate_ratio(validation_ratio):
       """验证比例参数"""

       if not isinstance(validation_ratio, (int, float)):
           raise TypeError(f"验证集比例必须是数字，得到: {type(validation_ratio)}")

       if validation_ratio < 0 or validation_ratio > 1:
           raise ValueError(f"验证集比例必须在0和1之间，得到: {validation_ratio}")

       if validation_ratio == 0 or validation_ratio == 1:
           print(f"警告: 验证集比例为 {validation_ratio}，将导致一个集合为空")

格式验证
--------

.. code-block:: python

   def validate_extxyz_format(filename):
       """验证EXTXYZ文件格式"""

       structure_count = 0
       line_count = 0

       with open(filename, 'r') as f:
           for line in f:
               line_count += 1
               stripped = line.strip()

               if stripped.isdigit():
                   structure_count += 1
                   atom_count = int(stripped)
                   # 这里可以添加更多验证逻辑

       print(f"文件包含 {structure_count} 个结构，共 {line_count} 行")

       if structure_count == 0:
           raise ValueError("文件不包含任何有效结构")

性能优化
========

内存优化策略
------------

对于大型数据集，可以使用流式处理方法：

.. code-block:: python

   def stream_split_extxyz(input_file, train_file, val_file, val_ratio, seed=None):
       """流式处理大型EXTXYZ文件"""

       if seed is not None:
           random.seed(seed)

       # 第一步：扫描文件，记录每个结构的起始位置和大小
       structure_info = []
       current_pos = 0
       current_size = 0

       with open(input_file, 'r') as f:
           for line in f:
               if line.strip().isdigit():
                   if current_size > 0:
                       structure_info.append((current_pos, current_size))
                   current_pos = f.tell() - len(line)
                   current_size = len(line)
               else:
                   current_size += len(line)

           if current_size > 0:
               structure_info.append((current_pos, current_size))

       # 第二步：随机选择验证集
       total_structures = len(structure_info)
       val_count = int(total_structures * val_ratio)
       val_indices = random.sample(range(total_structures), val_count)
       val_indices_set = set(val_indices)

       # 第三步：流式写入
       with open(input_file, 'r') as infile, \
            open(train_file, 'w') as train_out, \
            open(val_file, 'w') as val_out:

           for i, (pos, size) in enumerate(structure_info):
               infile.seek(pos)
               structure_content = infile.read(size)

               if i in val_indices_set:
                   val_out.write(structure_content)
               else:
                   train_out.write(structure_content)

       return total_structures - val_count, val_count

并行处理优化
------------

.. code-block:: python

   from concurrent.futures import ProcessPoolExecutor

   def parallel_structure_processing(structures, n_workers=4):
       """并行处理结构数据"""

       def process_structure(struct):
           # 处理单个结构的函数
           # 这里可以添加能量计算、特征提取等
           return processed_struct

       with ProcessPoolExecutor(max_workers=n_workers) as executor:
           processed_structures = list(executor.map(process_structure, structures))

       return processed_structures

最佳实践建议
============

数据集比例选择
--------------

.. list-table:: 验证集比例建议
   :widths: 20 40 40
   :header-rows: 1

   * - 数据集大小
     - 建议比例
     - 说明
   * - 小型（< 1000）
     - 20%-30%
     - 需要更多验证数据
   * - 中型（1000-10000）
     - 15%-20%
     - 平衡训练和验证
   * - 大型（> 10000）
     - 5%-10%
     - 训练数据更重要
   * - 超大型（> 100000）
     - 1%-5%
     - 最小化验证损失

数据质量检查
------------

分割前建议进行以下检查：

1. **完整性检查**：确保所有结构格式正确
2. **能量范围**：检查能量值是否在合理范围
3. **力收敛**：确认原子力已收敛
4. **重复结构**：移除高度相似的结构
5. **异常检测**：识别并处理异常值

随机性保证
----------

为了确保可重复性：

1. **固定随机种子**：在科学研究中很重要
2. **记录分割信息**：保存分割日志
3. **版本控制**：数据集版本管理

常见问题解答
============

Q1: 分割时提示 "输入文件不存在"
--------------------------------

**解决方案**：

.. code-block:: bash

   # 检查文件路径
   ls -la your_file.extxyz

   # 使用绝对路径
   python split_set.py --input /absolute/path/to/file.extxyz

Q2: 验证集比例设置错误
----------------------

**有效范围**：0.0 到 1.0 之间的小数。

**正确示例**：

.. code-block:: bash

   # 正确：10%验证集
   phymlp-kit split_set --val_ratio 0.1

   # 错误：百分比形式
   phymlp-kit split_set --val_ratio 10  # 错误！

Q3: 分割后文件为空
------------------

**可能原因**：

1. 输入文件为空
2. 验证集比例为 0 或 1
3. 文件格式不正确

**检查方法**：

.. code-block:: python

   def check_file_content(filename):
       with open(filename, 'r') as f:
           lines = f.readlines()
           print(f"文件 {filename} 有 {len(lines)} 行")

           # 显示前几行
           for i, line in enumerate(lines[:5]):
               print(f"行 {i+1}: {line.strip()}")

Q4: 需要按能量分层抽样
----------------------

**解决方案**：修改分割函数，实现分层抽样：

.. code-block:: python

   def stratified_split_by_energy(input_file, train_file, val_file, val_ratio):
       """按能量分层抽样"""

       # 1. 按能量分组结构
       energy_groups = group_structures_by_energy(input_file)

       train_structures = []
       val_structures = []

       # 2. 在每个能量组内按比例抽样
       for energy, structures in energy_groups.items():
           n_val = max(1, int(len(structures) * val_ratio))
           val_indices = random.sample(range(len(structures)), n_val)

           for i, struct in enumerate(structures):
               if i in val_indices:
                   val_structures.append(struct)
               else:
                   train_structures.append(struct)

       # 3. 写入文件
       write_structures(train_structures, train_file)
       write_structures(val_structures, val_file)

API 参考
========

函数列表
--------

.. py:function:: split_extxyz_structures(input_file, train_file, validation_file, validation_ratio)

   （详见上文）

异常列表
--------

.. py:exception:: FileNotFoundError

   当输入文件不存在时抛出。

.. py:exception:: ValueError

   当验证集比例不在有效范围内时抛出。

.. py:exception:: TypeError

   当参数类型不正确时抛出。

相关链接
========

- :ref:`quickstart` - 快速开始指南
- :ref:`main_py` - 主模块说明
- :ref:`get_kpath_module` - KPATH生成模块说明
- `EXTXYZ 格式规范 <https://libatoms.github.io/QUIP/io.html#extendedxyz>`_
- `机器学习数据集分割最佳实践 <https://scikit-learn.org/stable/modules/cross_validation.html>`_

更新日志
========

版本历史
--------

.. list-table:: 版本更新历史
   :widths: 20 80
   :header-rows: 1

   * - 版本
     - 更新内容
   * - v1.0.0
     - 初始版本，基本分割功能
   * - v1.1.0
     - 添加命令行参数支持
   * - v1.2.0
     - 改进错误处理和格式验证
   * - v1.3.0
     - 添加性能优化选项
   * - v1.4.0
     - 支持随机种子设置

计划功能
--------

1. **智能分割**：基于结构特征的智能分割策略
2. **交叉验证**：自动生成K折交叉验证数据集
3. **数据增强**：集成数据增强功能
4. **可视化**：数据集分布可视化工具
5. **质量评估**：数据集质量自动评估

.. note::

   欢迎提交功能建议和改进意见！