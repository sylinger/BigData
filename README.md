# README
## 实验：基于Spark的数据分析与处理
### 学生信息
#### **学号**: 
#### **姓名**: 
#### **学院**: 数据学院
#### **年级**: 研一
### 目录
1. [实验目的](#实验目的)
2. [实验环境](#实验环境)
3. [操作流程](#操作流程)
- [数据集收集](#数据集收集)
- [数据预处理](#数据预处理)
- [数据分析](#数据分析)
- [可视化](#可视化)
4. [结果与讨论](#结果与讨论)
5. [遇到的问题与解决方案](#遇到的问题与解决方案)
6. [实验总结](#实验总结)
7. [参考资料](#参考资料)

### 实验目的
本实验旨在研究 Bilibili（简称 b 站）《每周必看》栏目中视频与 UP 主的数据，通过大数据处理框架 Spark、Hadoop 及数据可视化技术，对数据进行存储、处理和分析，分类是否能进入热搜榜前10。

### 实验环境
**操作系统**: Ubuntu 22.04.2 LTS
**Python**: 3.8.16
**Hadoop**: 3.1.3
**Spark**: 3.2.0
**Anaconda**: 4.10.1
**vue**: 3.0.0

### 操作流程
#### 数据集收集
使用爬虫技术，通过 Bilibili API 收集数据。
爬取截止至 2024 年 12 月 4 日的 297 期视频数据，保存为 JSON 格式文件。
#### 数据预处理
选择有效数据，处理异常数据与空值。
使用文本数据处理，合并数据并上传至 HDFS，保存为 bilibili_week.txt。
#### 数据分析
使用 Spark SQL 分析数据，统计 UP 主的入选次数及播放量等。
使用 Spark MLlib 训练机器学习模型，分析互动数据与热搜排名的关系。
#### 可视化
使用 vue3和 echarts 对分析结果进行可视化，包括柱状图、词云图及热力图。
### 结果与讨论
通过数据分析，发现搞笑、明星、游戏类视频受欢迎，同时生活类视频也能引起共鸣。
可视化结果展示了不同维度数据的分析情况，助于更好理解用户偏好。
### 遇到的问题与解决方案

### 实验总结


### 参考资料
爬虫代码参考: 
Python Spark 数据分析案例: 
echarts 可视化文档: 
感谢您查看本文档。如有任何问题，请随时联系我。
