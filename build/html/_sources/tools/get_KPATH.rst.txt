.. _get_KPATH_module:

=========================
get_KPATH 模块说明
=========================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``get_KPATH.py`` 模块是 PhyMLP Kit 工具包中的一个核心工具，专门用于自动化生成布里渊区高对称点路径（KPATH）。该模块通过调用 VASPKIT 工具，为声子谱计算、能带结构计算等应用提供必需的高对称点路径信息。

功能特性
========

.. list-table:: 主要功能特性
   :widths: 30 70
   :header-rows: 1

   * - 特性
     - 描述
   * - 自动化交互
     - 完全自动化与 VASPKIT 的交互过程，无需用户手动输入
   * - 路径生成
     - 根据晶体结构自动计算并生成最优的高对称点路径
   * - 多格式输出
     - 生成 KPOINTS 文件、KPATH.in 文件等
   * - 错误处理
     - 完善的错误检测和处理机制
   * - 集群兼容
     - 适配各种计算集群环境

快速开始
========

基本使用方式
------------

.. code-block:: bash

   # 方式1：通过 phymlp-kit 命令行
   phymlp-kit generate_kpath --vaspkit_load /path/to/vaspkit

   # 方式2：直接运行 Python 脚本
   python get_KPATH.py /path/to/vaspkit

   # 方式3：在 Python 代码中导入
   from phymlp.tools.get_KPATH import generate_kpath
   generate_kpath("/path/to/vaspkit")

前置要求
--------

在使用本模块前，请确保：

1. **VASPKIT 已安装**：可以从 http://vaspkit.com 下载
2. **结构文件存在**：当前目录下需有 POSCAR 文件
3. **执行权限**：确保 VASPKIT 可执行文件具有执行权限

核心函数详解
============

generate_kpath 函数
-------------------

.. py:function:: generate_kpath(vaspkit_load)

   主功能函数：调用 VASPKIT 生成高对称点路径

   :param str vaspkit_load: VASPKIT 可执行文件的完整路径
   :raises PermissionError: 当 VASPKIT 文件没有执行权限时
   :raises FileNotFoundError: 当 VASPKIT 文件不存在时
   :returns: None

   **函数执行流程**：

   1. **路径验证阶段**

      .. code-block:: python

         vaspkit_load = os.path.abspath(vaspkit_load)  # 转换为绝对路径
         # 检查文件是否存在和权限

   2. **进程启动阶段**

      .. code-block:: python

         process = subprocess.Popen(
             [vaspkit_load],          # 执行 VASPKIT
             stdin=subprocess.PIPE,   # 准备输入管道
             stdout=subprocess.PIPE,  # 准备输出管道
             stderr=subprocess.PIPE,  # 准备错误管道
             text=True                # 文本模式
         )

   3. **自动化交互阶段**

      程序会按顺序向 VASPKIT 发送以下命令：

      .. code-block:: python

         options = ['03', '305', '3']  # VASPKIT 选项序列
         for opt in options:
             process.stdin.write(opt + '\\n')
             process.stdin.flush()
             time.sleep(1)  # 等待 VASPKIT 处理

   4. **进程清理阶段**

      .. code-block:: python

         # 发送退出命令
         process.stdin.write('q\\n')
         process.stdin.flush()
         process.stdin.close()
         process.wait()

   5. **结果输出阶段**

      .. code-block:: python

         print("Vaspkit标准输出:")
         print(process.stdout.read())
         print("Vaspkit标准错误:")
         print(process.stderr.read())

VASPKIT 交互选项详解
=======================

模块使用的 VASPKIT 选项序列：

.. list-table:: VASPKIT 选项说明
   :widths: 10 30 60
   :header-rows: 1

   * - 选项
     - 菜单层级
     - 功能描述
   * - '03'
     - 一级菜单
     - 选择"结构分析"功能
   * - '305'
     - 二级菜单
     - 选择"KPATH生成（2D/3D材料）"
   * - '3'
     - 三级菜单
     - 选择"自动模式"，由程序自动判断

输出文件说明
============

程序运行后会在当前目录生成以下文件：

KPOINTS 文件
------------

.. code-block:: text
   :caption: KPOINTS 文件示例

   K-Points for Bandstructure
   0              ! 0表示能带计算模式
   Line           ! 线段模式
   100            ! 每条路径的采样点数
   Reciprocal     ! 倒空间坐标
   0.0 0.0 0.0 G  ! 高对称点：Γ点
   0.5 0.0 0.0 X  ! 高对称点：X点
   0.5 0.5 0.0 M  ! 高对称点：M点
   0.0 0.0 0.0 G  ! 返回Γ点

关键参数说明：

- **采样点数**：决定能带计算的精度
- **高对称点**：由 VASPKIT 根据晶体对称性自动确定
- **路径顺序**：优化的路径顺序，覆盖重要对称点

KPATH.in 文件
---------------------

.. code-block:: text
   :caption: KPATH.in 文件示例

   K-Path in Reciprocal Lattice:
   G    0.00000 0.00000 0.00000
   X    0.50000 0.00000 0.00000
   M    0.50000 0.50000 0.00000
   G    0.00000 0.00000 0.00000

SYMMETRY 文件
------------------

包含空间群对称性信息，用于验证路径选择的正确性。

错误处理机制
============

权限错误处理
------------------

.. code-block:: python

   try:
       process = subprocess.Popen([vaspkit_load], ...)
   except PermissionError:
       print(f"权限错误: 无法执行Vaspkit at {vaspkit_load}")
       sys.exit(1)  # 优雅退出

管道错误处理
--------------

.. code-block:: python

   try:
       process.stdin.write(opt + '\\n')
       process.stdin.flush()
   except BrokenPipeError:
       print("Vaspkit已关闭标准输入管道")
       break  # 继续其他处理

文件存在性检查
---------------

建议在使用前手动检查：

.. code-block:: python

   import os

   def check_vaspkit_path(vaspkit_path):
       if not os.path.exists(vaspkit_path):
           raise FileNotFoundError(f"VASPKIT文件不存在: {vaspkit_path}")
       if not os.access(vaspkit_path, os.X_OK):
           raise PermissionError(f"VASPKIT没有执行权限: {vaspkit_path}")

使用示例
========

基本示例
-------------

.. code-block:: python
   :caption: 基本使用示例

   #!/usr/bin/env python3
   """使用 get_KPATH 模块的完整示例"""

   import sys
   from phymlp.tools.get_KPATH import generate_kpath

   def main():
       # 配置 VASPKIT 路径
       vaspkit_path = "/work/home/user/software/vaspkit.1.5.1/bin/vaspkit"

       try:
           # 生成 KPATH
           generate_kpath(vaspkit_path)
           print("KPATH 生成成功！")

           # 验证生成的文件
           if os.path.exists("KPOINTS"):
               print("已生成 KPOINTS 文件")
           if os.path.exists("KPATH.in"):
               print("已生成 KPATH.in 文件")

       except Exception as e:
           print(f"KPATH 生成失败: {e}")
           sys.exit(1)

   if __name__ == "__main__":
       main()

集成到工作流
------------

.. code-block:: python
   :caption: 集成到声子计算工作流

   def setup_phonon_calculation(structure_file, vaspkit_path):
       """设置完整的声子计算"""

       # 1. 准备结构
       print("步骤1: 准备晶体结构...")
       prepare_poscar(structure_file)

       # 2. 生成 KPATH
       print("步骤2: 生成高对称点路径...")
       generate_kpath(vaspkit_path)

       # 3. 准备 VASP 输入文件
       print("步骤3: 准备 VASP 输入文件...")
       prepare_incar_for_phonon()
       prepare_potcar()

       # 4. 验证设置
       print("步骤4: 验证计算设置...")
       validate_setup()

       print("声子计算设置完成！")
       print("请提交 VASP 计算任务。")

批量处理示例
------------

.. code-block:: python
   :caption: 批量处理多个结构

   import os
   from pathlib import Path

   def batch_generate_kpath(structures_dir, vaspkit_path):
       """为目录中的所有结构生成 KPATH"""

       structures = Path(structures_dir).glob("POSCAR_*")

       for poscar_file in structures:
           # 切换到结构目录
           original_dir = os.getcwd()
           structure_dir = poscar_file.parent

           os.chdir(structure_dir)

           try:
               print(f"处理结构: {poscar_file.name}")
               generate_kpath(vaspkit_path)
               print(f"  ✓ 成功生成 KPATH")

           except Exception as e:
               print(f"  ✗ 处理失败: {e}")

           finally:
               # 返回原始目录
               os.chdir(original_dir)

       print("批量处理完成！")

常见问题解答
============

Q1: 运行时提示 "权限错误: 无法执行Vaspkit"
-------------------------------------------------

**原因**：VASPKIT 可执行文件没有执行权限。

**解决方案**：

.. code-block:: bash

   chmod +x /path/to/your/vaspkit

Q2: VASPKIT 启动后立即退出，没有生成文件
--------------------------------------------------

**原因**：当前目录缺少 POSCAR 文件。

**解决方案**：

1. 确认当前目录有 POSCAR 文件

   .. code-block:: bash

      ls POSCAR

2. 如果 POSCAR 在其他位置，创建软链接：

   .. code-block:: bash

      ln -s /path/to/your/POSCAR .

Q3: 生成的 KPOINTS 文件采样点数不合适
----------------------------------------------

**原因**：VASPKIT 默认设置可能不适合特定体系。

**解决方案**：

1. 手动修改 KPOINTS 文件：

   .. code-block:: bash

      # 修改采样点数（如改为200）
      sed -i 's/^[0-9]\\+/200/' KPOINTS

2. 自定义 VASPKIT 选项序列：

   .. code-block:: python

      # 修改 get_KPATH.py 中的 options 列表
      options = ['03', '305', '1']  # 选择手动模式

Q4: 需要为不同精度生成多个 KPATH
---------------------------------------------

**解决方案**：封装不同精度的生成函数

.. code-block:: python

   def generate_kpath_with_precision(vaspkit_path, precision='high'):
       """根据精度要求生成 KPATH"""

       precision_settings = {
           'low': {'03', '305', '1', '50'},   # 50个采样点
           'medium': {'03', '305', '1', '100'}, # 100个采样点
           'high': {'03', '305', '1', '200'}   # 200个采样点
       }

       # 根据精度选择设置
       options = precision_settings.get(precision, precision_settings['medium'])

       # 执行生成...

性能优化建议
============

1. **并行处理**

   对于大量结构，可以使用并行处理：

   .. code-block:: python

      from concurrent.futures import ThreadPoolExecutor

      def parallel_generate_kpath(structure_list, vaspkit_path, max_workers=4):
          with ThreadPoolExecutor(max_workers=max_workers) as executor:
              futures = []
              for structure in structure_list:
                  future = executor.submit(generate_kpath_for_structure,
                                          structure, vaspkit_path)
                  futures.append(future)

              # 等待所有任务完成
              for future in futures:
                  future.result()

2. **缓存机制**

   对于相同结构，可以缓存 KPATH 结果：

   .. code-block:: python

      import hashlib
      import json

      class KpathCache:
          def __init__(self, cache_file=".kpath_cache.json"):
              self.cache_file = cache_file
              self.cache = self.load_cache()

          def get_hash(self, poscar_content):
              return hashlib.md5(poscar_content.encode()).hexdigest()

          def get_cached_kpath(self, poscar_file):
              with open(poscar_file, 'r') as f:
                  content = f.read()
              file_hash = self.get_hash(content)

              return self.cache.get(file_hash)

          # 其他缓存方法...

API 参考
========

函数列表
--------

.. py:function:: generate_kpath(vaspkit_load)

   （详见上文）

异常列表
--------

.. py:exception:: PermissionError

   当 VASPKIT 文件没有执行权限时抛出。

.. py:exception:: FileNotFoundError

   当 VASPKIT 文件不存在时抛出。

相关链接
========

- :ref:`quickstart` - 快速开始指南
- :ref:`main_py` - 主模块说明
- `VASPKIT 官方网站 <http://vaspkit.com/>`_
- `VASP 能带计算教程 <https://www.vasp.at/wiki/index.php/Bandstructure_calculations>`_
- `布里渊区与高对称点 <https://en.wikipedia.org/wiki/Brillouin_zone>`_

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
     - 初始版本，基本功能实现
   * - v1.1.0
     - 添加错误处理和权限检查
   * - v1.2.0
     - 改进进程管理和输出处理
   * - v1.3.0
     - 添加独立运行模式支持

计划功能
--------

1. **自定义选项**：支持用户自定义 VASPKIT 选项序列
2. **格式转换**：支持不同格式的输出
3. **图形界面**：提供简单的图形界面
4. **批量处理**：增强批量处理功能

.. note::

   如果你发现 bug 或有功能建议，请在项目 issue 页面提交。