<<<<<<< HEAD
PhyMLP 使用文档
==================

欢迎来到 **PhyMLP Kit** 的官方文档。
PhyMLP Kit 是一个用于材料性质预测与机器学习势函数开发的集成工具包，支持从结构生成、数据转换、自动训练集构建到模型部署的全流程。

快速导航
--------

.. toctree::
   :maxdepth: 2
   :caption: PhyMLP快速开始

   phymlp

.. toctree::
   :maxdepth: 2
   :caption: 命令行工具模块（开发者模块）

   cli/main

.. toctree::
   :maxdepth: 2
   :caption: LAMMPS计算工具模块

   tools/get_KPATH

.. toctree::
   :maxdepth: 2
   :caption: 数据集处理模块

   tools/split_set

.. toctree::
   :maxdepth: 2
   :caption: 训练及检验模块

   train_and_validation/core

.. toctree::
   :maxdepth: 2
   :caption: 自动化训练集生成模块

   auto_generate_set/auto_generate_set
   auto_generate_set/birch_murnaghan_fitting
   auto_generate_set/config
   auto_generate_set/deform_structures
   auto_generate_set/exp_pv_structures
   auto_generate_set/from_mp_structures
   auto_generate_set/generate_extxyz_dataset
   auto_generate_set/perturb_structures
   auto_generate_set/potcar_generator
   auto_generate_set/process_deform_results
   auto_generate_set/utils
   auto_generate_set/vasp_setup
   auto_generate_set/vasp_submit

.. toctree::
   :maxdepth: 2
   :caption: 训练集格式转换模块

   auto_generate_set/dump_to_poscar
   converters/cfg2extxyz
   converters/outcar_converter

进阶使用
--------

- 如果你是开发者，可以深入了解 :doc:`phymlp.converters` 和 :doc:`phymlp.utils`
- 如需扩展功能，请在 `modules.rst` 中添加自定义模块

相关资源
--------

- `GitHub 仓库 <https://github.com/your-repo/phymlp>`_
- `问题反馈 <https://github.com/your-repo/phymlp/issues>`_
- `示例与教程 <https://github.com/your-repo/phymlp-examples>`_

.. note::
   如需添加新的模块文档，请在联系我们ningshihui@hnu.edu.cn或者b240700371@hnu.edu.cn

.. tip::
   文档支持中文阅读，若需切换语言，请在 `conf.py` 中修改 `language` 设置

索引与搜索
----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
=======
.. NSH documentation master file, created by
   sphinx-quickstart on Sun Oct 19 14:33:48 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

PhyMLP documentation
=====================

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

欢迎查看 PhyMLP 文档！
========================

快速开始
--------
.. code-block:: bash

   pip install phymlp

.. toctree::
   :maxdepth: 2
   :caption: 目录：

   quickstart
   modules
>>>>>>> 7a6a5473e5cf811ab04cbe26f0f092ca4909e88c
