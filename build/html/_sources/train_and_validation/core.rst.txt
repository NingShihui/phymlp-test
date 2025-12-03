.. _core_module:

=========================
训练与检验模块
=========================

.. contents:: 目录
   :depth: 3
   :local:

概述
====

``core.py`` 是 PhyMLP Kit 工具包的核心模块，提供配置文件读取、参数解析、作业提交、任务管理等核心功能。该模块包含两个主要类：``PUBLIC`` 和 ``RUN``，共同构成了整个系统的基础架构。

模块架构
========

模块架构图
----------

::

   core.py 核心模块
   ├── PUBLIC 类
   │   ├── 配置管理
   │   ├── 参数解析
   │   └── 格式处理
   └── RUN 类
       ├── 训练管理
       │   ├── 训练命令生成
       │   └── 训练执行
       ├── 计算管理
       │   ├── 计算目录管理
       │   ├── 输入文件重写
       │   └── 计算执行
       └── 作业调度
           ├── SLURM作业提交
           ├── 作业状态监控
           └── 后处理执行

PUBLIC 类详解
=============

类概述
------

``PUBLIC`` 类是公共配置管理器，负责：

1. **配置参数管理**：定义和维护所有配置参数
2. **配置文件解析**：读取和解析 ``Inputfile.txt`` 配置文件
3. **参数验证**：验证参数的有效性和完整性
4. **默认值设置**：提供合理的默认配置

初始化参数
----------

.. code-block:: python
   :caption: PUBLIC 类的初始化参数

   class PUBLIC:
       def __init__(self):
           self.current_path = os.getcwd()
           self.Inputfile = "Inputfile"

           # 所有允许的命令
           self.all_keys = [
               "PhyMLP_load", "lmp_mpi_load", 'train', 'extxyz_load',
               'init_PhyMLP', 'iteration_limit', 'al_mode', 'save_to',
               "pot_PhyMLP_load", 'calculate', 'properties', "crystal_structure",
               "lattice", "atomic_mass", "vaspkit_load"
           ]

           # 所有支持的计算属性
           self.all_properties = ["E-V", "Elastic", "phonon", "P-V"]

           # 设置默认参数
           self._set_default_parameters()

默认参数设置
------------

.. list-table:: PUBLIC 类的默认参数
   :widths: 25 35 40
   :header-rows: 1

   * - 参数名
     - 默认值
     - 描述
   * - ``vaspkit_load``
     - "./"
     - VASPKIT 工具路径
   * - ``PhyMLP_load``
     - "./"
     - PhyMLP 安装路径
   * - ``lmp_mpi_load``
     - "./lmp_mpi"
     - LAMMPS 可执行文件路径
   * - ``train``
     - "True"
     - 是否执行训练
   * - ``extxyz_load``
     - "./train.exyz"
     - 训练集文件路径
   * - ``init_PhyMLP``
     - "06.PhyMLP"
     - 初始势函数文件
   * - ``iteration_limit``
     - "5000"
     - 最大迭代次数
   * - ``al_mode``
     - "nbh"
     - 训练模式
   * - ``save_to``
     - "./pot.PhyMLP"
     - 势函数保存路径
   * - ``calculate``
     - "True"
     - 是否执行计算
   * - ``properties``
     - ["E-V"]
     - 计算性质列表
   * - ``crystal_structure``
     - "bcc"
     - 晶体结构类型
   * - ``lattice``
     - "1"
     - 晶格常数
   * - ``atomic_mass``
     - "1"
     - 原子质量

核心方法详解
------------

Read 方法
~~~~~~~~~

.. py:method:: PUBLIC.Read(Inputfile)

   读取并解析配置文件

   :param str Inputfile: 配置文件路径
   :return: 解析后的配置信息列表
   :rtype: list
   :raises SystemExit: 当文件读取失败时

   **功能说明**：

   1. 打开指定配置文件
   2. 逐行读取内容
   3. 跳过注释行和空行
   4. 移除行内注释
   5. 返回有效配置行列表

   **代码实现**：

   .. code-block:: python

      def Read(self, Inputfile):
          input_informations = []
          try:
              with open(Inputfile, 'r', encoding='utf-8') as readfile:
                  read_informations = readfile.readlines()
                  for read_information in read_informations:
                      new_line = "".join(read_information.split())  # 移除空白字符
                      if new_line.startswith('#') or len(new_line) == 0:
                          continue  # 跳过注释行和空行
                      new_line = new_line.split("#")[0]  # 移除行内注释
                      input_informations.append(new_line)
                  return input_informations
          except Exception as e:
              print(f"文件读取错误: {e}")
              sys.exit(1)

Key_and_parament 方法
~~~~~~~~~~~~~~~~~~~~~

.. py:method:: PUBLIC.Key_and_parament(input_informations)

   解析配置信息并设置类属性

   :param list input_informations: 配置信息列表
   :raises SystemExit: 当配置错误时

   **解析逻辑**：

   1. **键名映射**：处理大小写和命名差异

      .. code-block:: python

         key_mapping = {
             'phymlp_load': 'PhyMLP_load',
             'lmp_mpi_load': 'lmp_mpi_load',
             'train': 'train',
             'extxyz_load': 'extxyz_load',
             'init_phymlp': 'init_PhyMLP',
             # ... 其他映射
         }

   2. **值解析**：支持多种值格式
      - 字符串（带引号）："path/to/file"
      - 数字：5000
      - 布尔值：True/False
      - 列表：["E-V", "Elastic"]

   3. **特殊处理**：``properties`` 参数的特殊解析

   4. **属性设置**：使用 ``setattr()`` 动态设置类属性

_parse_value 方法
~~~~~~~~~~~~~~~~~

.. py:method:: PUBLIC._parse_value(value_str)

   安全地解析配置值字符串

   :param str value_str: 原始值字符串
   :return: 解析后的值
   :rtype: any

   **解析策略**：

   1. **字符串检测**：检查是否被引号包围
   2. **字面量解析**：尝试使用 ``ast.literal_eval()`` 解析
   3. **回退机制**：解析失败时返回原始字符串

   **示例**：

   - 输入：``'"path/to/file"'`` → 输出：``"path/to/file"``
   - 输入：``'5000'`` → 输出：``5000``
   - 输入：``'["E-V", "Elastic"]'`` → 输出：``["E-V", "Elastic"]``
   - 输入：``'True'`` → 输出：``True``

Bool_commands 方法
~~~~~~~~~~~~~~~~~~

.. py:method:: PUBLIC.Bool_commands(bool_command)

   验证并转换布尔命令

   :param any bool_command: 布尔命令值
   :return: 转换后的布尔值
   :rtype: bool
   :raises SystemExit: 当值无效时

   **支持格式**：

   - Python 布尔值：``True``, ``False``
   - 字符串布尔值：``"true"``, ``"false"``（不区分大小写）
   - 其他值将引发错误

RUN 类详解
==========

类概述
------

``RUN`` 类继承自 ``PUBLIC``，负责：

1. **训练任务管理**：机器学习势的训练流程控制
2. **计算任务管理**：各种物性计算的执行控制
3. **作业调度**：SLURM 作业提交和监控
4. **后处理**：计算结果的处理和分析

作业调度系统
------------

SLURM 作业提交
~~~~~~~~~~~~~~

.. py:method:: RUN.slurm_sub(job_name, command="")

   提交作业到 SLURM 调度系统

   :param str job_name: 作业名称
   :param str command: 训练命令（仅训练作业需要）
   :raises subprocess.CalledProcessError: 作业提交失败时
   :raises RuntimeError: 作业监控过程中出错时

   **作业脚本生成**：

   根据作业类型生成不同的 SLURM 脚本：

   .. code-block:: bash

      # 训练作业脚本
      #!/bin/bash
      #SBATCH -J calculate_train
      #SBATCH -N 1
      #SBATCH -p xahcnormal
      #SBATCH --ntasks-per-node=32
      mpirun -n 32 {train_command} > train-output.log

      # 计算作业脚本
      #!/bin/bash
      #SBATCH -J calculate_{job_name}
      #SBATCH -N 1
      #SBATCH -p xahcnormal
      #SBATCH --ntasks-per-node=32
      mpirun -n 32 {lmp_mpi_load} -i {job_name}.in > output.log

   **执行流程**：

   1. 创建作业目录
   2. 生成 SLURM 脚本文件
   3. 提交作业到队列
   4. 获取作业 ID
   5. 启动作业监控

_wait_for_job_completion 方法
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: RUN._wait_for_job_completion(job_id, job_name, current_path, job_dir)

   监控作业状态并等待完成

   :param str job_id: SLURM 作业 ID
   :param str job_name: 作业名称
   :param str current_path: 当前工作目录
   :param str job_dir: 作业目录

   **监控机制**：

   1. 启动等待动画线程
   2. 定期使用 ``squeue -j {job_id}`` 检查作业状态
   3. 检测作业状态变化：
      - ``R``：运行中
      - ``PD``：排队中
      - 不存在：作业已完成
   4. 作业完成后执行后处理
   5. 清理临时文件

_post_process 方法
~~~~~~~~~~~~~~~~~~

.. py:method:: RUN._post_process(job_name, current_path)

   作业完成后执行相应的后处理

   :param str job_name: 作业名称
   :param str current_path: 当前工作目录

   **后处理类型**：

   .. list-table:: 不同作业的后处理
      :widths: 20 40 40
      :header-rows: 1

      * - 作业类型
        - 后处理命令
        - 说明
      * - E-V
        - ``python plot.py``
        - 绘制能量-体积曲线
      * - P-V
        - ``python plot.py``
        - 绘制压力-体积曲线
      * - phonon
        - 多步声子分析
        - 生成声子谱

_process_phonon 方法
~~~~~~~~~~~~~~~~~~~~

.. py:method:: RUN._process_phonon(current_path, job_name)

   声子计算的特殊后处理

   :param str current_path: 当前工作目录
   :param str job_name: 作业名称

   **处理流程**：

   .. code-block:: bash

      # 1. 运行 phonolammps
      phonolammps PHONON.in -c POSCAR --dim 2 2 2

      # 2. 生成 KPATH
      python get_KPATH.py >> PHONON.log
      rm ./get_KPATH.py

      # 3. 修改维度设置
      sed -i 's/DIM =/DIM = 2 2 2/' ./KPATH.phonopy

      # 4. 生成声子谱
      phonopy -c POSCAR -p -s KPATH.phonopy

训练管理方法
------------

Train_commands 方法
~~~~~~~~~~~~~~~~~~~

.. py:method:: RUN.Train_commands(drive)

   生成训练命令和准备训练目录

   :param bool drive: 是否执行训练
   :return: (训练目录路径, 训练命令) 或 ("No_path", "Skip_step")
   :rtype: tuple
   :raises SystemExit: 训练目录创建失败时

   **执行步骤**：

   1. 检查训练开关
   2. 创建训练目录
   3. 复制初始势函数和训练集
   4. 生成训练命令

   **训练命令格式**：

   .. code-block:: bash

      {PhyMLP_load}/bin/MLP train {init_PhyMLP} {extxyz_load} \
        --save_to={save_to} \
        --iteration_limit={iteration_limit} \
        --al_mode={al_mode}

Train 方法
~~~~~~~~~~

.. py:method:: RUN.Train(train_drive, train_dir, train_command)

   执行训练任务

   :param bool train_drive: 是否执行训练
   :param str train_dir: 训练目录路径
   :param str train_command: 训练命令

   **执行逻辑**：

   1. 检查训练开关
   2. 调用 ``slurm_sub()`` 提交训练作业
   3. 等待训练完成

计算管理方法
------------

Calculate_dir 方法
~~~~~~~~~~~~~~~~~~

.. py:method:: RUN.Calculate_dir(drive)

   创建计算目录并复制必要文件

   :param bool drive: 是否执行计算
   :raises SystemExit: 目录创建或文件复制失败时

   **执行步骤**：

   1. 检查计算开关
   2. 去重计算属性列表
   3. 为每个属性：
      - 从 PhyMLP 模板目录复制计算目录
      - 复制势函数文件到计算目录

Rewrite_lammps_in 方法
~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: RUN.Rewrite_lammps_in(drive)

   根据配置重写 LAMMPS 输入文件

   :param bool drive: 是否执行计算任务

   **修改逻辑**：

   根据不同的计算属性，调用相应的修改方法：

   - ``_modify_ev_in()``：修改 E-V 计算输入文件
   - ``_modify_elastic_in()``：修改弹性常数计算输入文件
   - ``_modify_pv_in()``：修改 P-V 计算输入文件
   - ``_modify_phonon_in()``：修改声子计算输入文件

输入文件修改方法
~~~~~~~~~~~~~~~~

E-V 计算修改
^^^^^^^^^^^^

.. code-block:: python

   def _modify_ev_in(self):
       lattice_min = '%.2f' % (float(self.lattice) - float(self.lattice) * 0.3)
       interval = '%.2f' % (2 * float(self.lattice) * 0.3 / 100)

       commands = [
           f"sed -i 's/define_mass/mass 1 {self.atomic_mass}/' ./E-V/E-V.in",
           f"sed -i 's/crystal_structure/{self.crystal_structure}/' ./E-V/E-V.in",
           f"sed -i 's/lattice_constant/{lattice_min}+{interval}*$i/' ./E-V/E-V.in"
       ]

P-V 计算修改
^^^^^^^^^^^^

.. code-block:: python

   def _modify_pv_in(self):
       interval = '%.6f' % (float(self.lattice) * 0.1 / 50)
       basis_volume = float(self.lattice) ** 3

       commands = [
           f"sed -i 's/define_mass/mass 1 {self.atomic_mass}/' ./P-V/P-V.in",
           f"sed -i 's/crystal_structure/{self.crystal_structure}/' ./P-V/P-V.in",
           f"sed -i 's/lattice_constant/{self.lattice}-{interval}*$i/' ./P-V/P-V.in",
           f"sed -i 's/basis_volume/{basis_volume}/' ./P-V/P-V.in"
       ]

Execute 方法
~~~~~~~~~~~~

.. py:method:: RUN.Execute(drive)

   执行所有计算任务

   :param bool drive: 是否执行计算任务

   **执行逻辑**：

   1. 检查计算开关
   2. 遍历所有计算属性
   3. 为每个属性提交计算作业
   4. 等待所有作业完成

使用示例
========

基本使用流程
------------

.. code-block:: python
   :caption: 基本使用示例

   #!/usr/bin/env python3
   """core.py 模块使用示例"""

   import os
   import sys

   # 导入核心模块
   from phymlp.utils.core import RUN

   def main():
       # 1. 创建 RUN 实例
       run = RUN()

       # 2. 读取配置文件
       print("步骤1: 读取配置文件...")
       input_info = run.Read("Inputfile.txt")

       # 3. 解析配置参数
       print("步骤2: 解析配置参数...")
       run.Key_and_parament(input_info)

       # 4. 执行训练（如果需要）
       print("步骤3: 准备训练...")
       train_drive = run.Bool_commands(run.train)
       train_dir, train_cmd = run.Train_commands(train_drive)

       print("步骤4: 执行训练...")
       run.Train(train_drive, train_dir, train_cmd)

       # 5. 执行计算（如果需要）
       print("步骤5: 准备计算...")
       calc_drive = run.Bool_commands(run.calculate)
       run.Calculate_dir(calc_drive)
       run.Rewrite_lammps_in(calc_drive)

       print("步骤6: 执行计算...")
       run.Execute(calc_drive)

       print("所有任务完成！")

   if __name__ == "__main__":
       main()

自定义配置示例
--------------

.. code-block:: python
   :caption: 自定义配置和使用

   def custom_training_workflow():
       """自定义训练工作流"""

       # 创建配置管理器
       config = PUBLIC()

       # 手动设置参数
       config.PhyMLP_load = "/opt/phymlp"
       config.lmp_mpi_load = "/usr/local/bin/lmp_mpi"
       config.train = True
       config.extxyz_load = "./data/training_set.extxyz"
       config.init_PhyMLP = "10.PhyMLP"
       config.iteration_limit = 10000
       config.al_mode = "nbh"

       # 创建运行管理器
       runner = RUN()

       # 继承配置
       for attr in dir(config):
           if not attr.startswith('_'):
               setattr(runner, attr, getattr(config, attr))

       # 执行训练
       train_dir, train_cmd = runner.Train_commands(True)
       runner.Train(True, train_dir, train_cmd)

       print("自定义训练完成！")

批量计算示例
------------

.. code-block:: python
   :caption: 批量执行多种计算

   def batch_property_calculation():
       """批量执行多种物性计算"""

       # 初始化
       runner = RUN()

       # 设置计算参数
       runner.calculate = True
       runner.properties = ["E-V", "Elastic", "P-V", "phonon"]
       runner.crystal_structure = "fcc"
       runner.lattice = "3.615"  # 铜的晶格常数
       runner.atomic_mass = "63.546"
       runner.pot_PhyMLP_load = "./train/pot.PhyMLP"

       # 准备计算
       runner.Calculate_dir(True)
       runner.Rewrite_lammps_in(True)

       # 执行计算
       runner.Execute(True)

       print("批量计算完成！")

错误处理机制
============

配置文件错误
------------

**常见错误**：
- 文件不存在
- 格式错误
- 参数无效

**处理方式**：

.. code-block:: python

   try:
       input_info = run.Read("Inputfile.txt")
       run.Key_and_parament(input_info)
   except SystemExit as e:
       print(f"配置文件错误: {e}")
       # 提供修复建议
       print("请检查 Inputfile.txt 文件格式和内容")
   except Exception as e:
       print(f"未知错误: {e}")

作业提交错误
------------

**常见错误**：
- SLURM 命令不存在
- 权限不足
- 队列不可用

**处理方式**：

.. code-block:: python

   def safe_slurm_sub(runner, job_name, command=""):
       """安全的作业提交"""
       try:
           runner.slurm_sub(job_name, command)
       except subprocess.CalledProcessError as e:
           print(f"作业提交失败: {e}")
           print(f"返回码: {e.returncode}")
           print(f"输出: {e.output}")
       except Exception as e:
           print(f"作业执行错误: {e}")

参数验证
--------

**验证函数示例**：

.. code-block:: python

   def validate_parameters(runner):
       """验证核心参数"""

       errors = []

       # 检查必要路径
       if not os.path.exists(runner.PhyMLP_load):
           errors.append(f"PhyMLP路径不存在: {runner.PhyMLP_load}")

       if not os.path.exists(runner.lmp_mpi_load):
           errors.append(f"LAMMPS路径不存在: {runner.lmp_mpi_load}")

       # 检查训练集
       if runner.train and not os.path.exists(runner.extxyz_load):
           errors.append(f"训练集文件不存在: {runner.extxyz_load}")

       # 检查势函数
       if runner.calculate and not os.path.exists(runner.pot_PhyMLP_load):
           errors.append(f"势函数文件不存在: {runner.pot_PhyMLP_load}")

       # 返回错误列表
       return errors

性能优化建议
============

并发作业提交
------------

对于多个计算任务，可以优化提交策略：

.. code-block:: python

   def parallel_execute(runner, max_concurrent=2):
       """并行执行计算任务"""

       import threading
       from queue import Queue

       def worker():
           while True:
               job_name = job_queue.get()
               if job_name is None:
                   break
               runner.slurm_sub(job_name)
               job_queue.task_done()

       # 创建作业队列
       job_queue = Queue()
       for prop in runner.properties:
           job_queue.put(prop.upper())

       # 创建工作线程
       threads = []
       for _ in range(min(max_concurrent, len(runner.properties))):
           t = threading.Thread(target=worker)
           t.start()
           threads.append(t)

       # 等待所有作业完成
       job_queue.join()

       # 停止工作线程
       for _ in range(len(threads)):
           job_queue.put(None)
       for t in threads:
           t.join()

资源监控
--------

监控系统资源使用情况：

.. code-block:: python

   def monitor_resources(job_id):
       """监控作业资源使用"""

       import time

       while True:
           # 使用 sacct 命令获取资源信息
           cmd = f"sacct -j {job_id} --format=JobID,State,CPUTime,MaxRSS,NodeList"
           result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

           if result.returncode == 0:
               print(f"资源监控: {result.stdout}")

           # 等待一段时间
           time.sleep(30)

常见问题解答
============

Q1: 配置文件读取失败，提示编码错误
-----------------------------------

**解决方案**：指定正确的文件编码

.. code-block:: python

   # 修改 Read 方法中的文件打开方式
   with open(Inputfile, 'r', encoding='utf-8-sig') as readfile:

Q2: SLURM 作业提交后立即失败
----------------------------

**可能原因**：
1. LAMMPS 可执行文件路径错误
2. 势函数文件不存在
3. 输入文件格式错误

**检查步骤**：
1. 验证 ``lmp_mpi_load`` 路径
2. 检查计算目录中的势函数文件
3. 查看生成的输入文件

Q3: 训练过程中出现 "参数不正确" 错误
------------------------------------

**解决方案**：
1. 检查 ``Inputfile.txt`` 中的参数拼写
2. 确保值格式正确
3. 查看 ``Key_and_parament`` 方法的输出

Q4: 如何自定义后处理脚本
------------------------

**扩展方法**：

.. code-block:: python

   class CustomRUN(RUN):
       def _post_process(self, job_name, current_path):
           """自定义后处理"""

           # 调用父类方法
           super()._post_process(job_name, current_path)

           # 添加自定义处理
           if job_name.lower() == "e-v":
               self._custom_ev_analysis(current_path, job_name)

       def _custom_ev_analysis(self, current_path, job_name):
           """自定义 E-V 分析"""
           custom_cmd = f"cd {current_path}/{job_name} && python custom_analysis.py"
           subprocess.Popen(custom_cmd, shell=True).wait()

API 参考
========

类列表
------

.. py:class:: PUBLIC()

   公共配置管理器

   **主要方法**：

   - ``Read(Inputfile)``：读取配置文件
   - ``Key_and_parament(input_informations)``：解析配置
   - ``Bool_commands(bool_command)``：验证布尔命令

.. py:class:: RUN()

   运行管理器（继承自 PUBLIC）

   **主要方法**：

   - ``slurm_sub(job_name, command="")``：提交 SLURM 作业
   - ``Train_commands(drive)``：生成训练命令
   - ``Train(train_drive, train_dir, train_command)``：执行训练
   - ``Calculate_dir(drive)``：准备计算目录
   - ``Rewrite_lammps_in(drive)``：重写输入文件
   - ``Execute(drive)``：执行计算任务

异常列表
--------

.. py:exception:: SystemExit

   当配置错误或执行失败时抛出。

相关链接
========

- :ref:`quickstart` - 快速开始指南
- :ref:`cli/main_py` - 主模块说明
- :ref:`input_files/train_input` - Inputfile.txt 配置说明
- `SLURM 文档 <https://slurm.schedmd.com/documentation.html>`_
- `LAMMPS 文档 <https://docs.lammps.org/>`_
- `PhyMLP 文档 <https://phymlp.org/>`_

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
     - 初始版本，基础功能实现
   * - v1.1.0
     - 添加配置解析和验证
   * - v1.2.0
     - 集成 SLURM 作业调度
   * - v1.3.0
     - 改进错误处理和日志
   * - v1.4.0
     - 添加多种计算类型支持

计划功能
--------

1. **更多调度器支持**：支持 PBS、LSF 等其他作业调度系统
2. **资源自适应**：根据可用资源自动调整计算参数
3. **进度报告**：实时训练和计算进度报告
4. **结果分析**：集成自动化结果分析工具
5. **Web 界面**：提供 Web 管理界面

.. note::

   如果你在使用过程中遇到问题或有改进建议，请在项目仓库提交 Issue。