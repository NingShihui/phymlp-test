phymlp简介
==============

快速开始指南
----------

本指南将帮助您快速掌握 PhyMLP Kit 的核心功能，从自动训练集生成到机器学习势函数训练与验证的完整流程。我们将按照以下步骤进行：

1. 配置文件说明
2. 自动训练集生成流程
3. 机器学习势函数训练
4. 性质计算与验证

.. toctree::
   :maxdepth: 4

   quickstart

配置文件说明
------------

PhyMLP Kit 使用两个主要配置文件：``input.yaml`` 用于控制自动训练集生成，``Inputfile.txt`` 用于控制训练和性质计算。

自动采样配置参数
~~~~~~~~~~~~~

这是自动化获取训练集的的配置文件，在案例中以input.yaml文件呈现：

.. toctree::
   :maxdepth: 4

   input_files/auto_trainset_input

自动训练及检验配置
~~~~~~~~~~~~~~~

这是机器学习势函数自动化训练和检验的配置文件，在案例中以inputfile文件呈现：

.. toctree::
   :maxdepth: 4

   input_files/train_input

