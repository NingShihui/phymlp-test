VASP任务提交和管理模块
=====================

本模块用于批量提交、监控和管理VASP计算任务，支持SLURM作业系统。

模块概述
--------

该模块提供了一组函数，用于：

1. 自动发现和验证VASP计算目录
2. 批量提交SLURM作业
3. 监控作业运行状态
4. 检查计算完成情况和结果

主要函数说明
------------

check_job_status(job_id)
^^^^^^^^^^^^^^^^^^^^^^^^

检查作业状态。

**参数：**
- ``job_id``: 作业ID（字符串或数字）

**返回：**
- 作业状态字符串：'RUNNING'、'COMPLETED' 或 'UNKNOWN'

**作用：**
使用squeue命令查询指定作业的当前状态。

check_calculation_success(calc_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

检查计算是否成功完成。

**参数：**
- ``calc_dir``: 计算目录路径

**返回：**
- 布尔值，表示计算是否成功完成

**作用：**
通过检查OUTCAR文件中是否存在"Total CPU time used"标记来判断计算是否正常结束。

submit_job(calc_dir)
^^^^^^^^^^^^^^^^^^^^

提交单个作业。

**参数：**
- ``calc_dir``: 计算目录路径

**返回：**
- 作业ID（字符串）或None（提交失败时）

**作用：**
在指定计算目录中执行sbatch命令提交SLURM作业。

get_running_jobs()
^^^^^^^^^^^^^^^^^^

获取当前运行的作业列表。

**参数：**
- 无参数

**返回：**
- 当前用户运行的作业ID列表

**作用：**
查询当前用户在SLURM系统中所有正在运行的作业。

discover_vasp_calc_dirs(vasp_dir)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

自动发现vasp_calculations目录下的所有计算目录。

**参数：**
- ``vasp_dir``: VASP计算根目录路径

**返回：**
- 有效计算目录的路径列表

**作用：**
扫描目录结构，识别包含完整VASP输入文件（POSCAR、INCAR、submit.sh）的计算目录。

submit_vasp_calculations(config_file="input.yaml")
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

批量提交VASP计算。

**参数：**
- ``config_file``: 配置文件路径（默认"input.yaml"）

**返回：**
- 无返回值

**作用：**
主控制函数，管理整个批量提交流程：发现计算、提交作业、监控状态、处理结果。

工作流程
--------

1. **目录发现**：扫描``materials_project/vasp_calculations/``目录下的所有子目录
2. **状态检查**：检查哪些计算已经完成，哪些需要提交
3. **批量提交**：根据最大批处理数量限制提交作业
4. **状态监控**：定期检查作业运行状态
5. **结果验证**：确认计算成功完成

配置参数说明
------------

配置文件需要包含以下提交相关参数：

.. code-block:: yaml

    vasp:
        submission:
            max_batch_size: 50     # 最大同时运行作业数
            check_interval: 300    # 状态检查间隔（秒）

输出信息
--------

模块会提供详细的运行状态信息：

.. code-block:: text

    正在扫描VASP计算目录...
    发现计算类别: BaTiO3
      ✓ 有效计算目录: BaTiO3_mp-2998_supercell
    === 第1轮提交 ===
    当前运行作业: 0/50
    可提交 50 个新作业
      ✓ 已提交作业: 123456 - BaTiO3/BaTiO3_mp-2998_supercell

使用示例
--------

.. code-block:: bash

    # 直接运行模块
    python vasp_submit.py

    # 或在Python代码中调用
    from vasp_submit import submit_vasp_calculations
    submit_vasp_calculations("input.yaml")

注意事项
--------

1. 需要SLURM作业系统环境
2. 需要先运行vasp_setup.py生成计算目录
3. 提交脚本（submit.sh）需要针对具体的HPC环境配置
4. 最大批处理数量应根据队列资源合理设置
5. 计算完成判断基于OUTCAR文件中的特定标记