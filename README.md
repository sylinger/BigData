# README
## 实验：基于Spark的数据分析与处理
### 学生信息
#### **学号**: 
#### **姓名**: 
#### **学院**: 数据学院
#### **年级**: 研一
### 目录
[一、实验目的](#一实验目的)  
[二、实验环境](#二实验环境)  
[三、操作流程](#三操作流程)  
[3.1 数据集收集](#31-数据集收集)  
[3.2 数据预处理](#32-数据预处理)  
[3.3 数据分析](#33-数据分析)  
[3.4 可视化](#34-可视化)  
[四、结果与讨论](#四结果与讨论)  
[五、遇到的问题与解决方案](#五遇到的问题与解决方案)  
[六、实验总结](#六实验总结)  
[七、参考资料](#七参考资料)  

### 一、实验目的
Bilibili(简称b站) 是中国年轻人高度聚集的文化社区和视频平台，人们可以通过弹幕、评论、点赞或收藏等方式来与视频发布者(称为up主)来进行互动。《每周必看》是b站的一个栏目， b站会对新一周发布的视频根据不同条件进行筛选，将热门的、有趣的、有价值的视频收录在该栏目中推荐给用户观看。这次实验中，希望对被收录在b站《每周必看》视频与up主的数据信息进行研究，通过运用大数据处理框架 Spark、Hadoop 及数据可视化技术，对这些数据进行存储、处理和分析，并对每个收录视频能否进入热搜榜前10进行分类。具体来说本次作业实现功能如下：  
(1)采用爬虫技术，编写代码收集截止至5月20日b站所有《每周必看》栏目的数据；  
(2)对原始数据进行清洗，包括有价值字段的选择、异常数据的删除以及文本数据的修正等，最后数据保存为txt文件并上传至HDFS；  
(3)使用spark sql组件对HDFS的数据进行分析，主要统计各收录视频的基本播放情况以及up主的累计数据；  
(4)使用spark MLlib组件对HDFS的数据进行分析，研究视频点赞数、播放量、互动热度等之间的关系，并训练机器学习模型对视频能否进入热搜榜前十进行分类；  
(5)使用pyecharts工具对分析结果进行可视化。  

### 二、实验环境
**操作系统**: Linux release 7.5.1804 (Core)
**Python**: 3.8.8
**Hadoop**: 3.1.3
**Spark**: 3.2.0
**Anaconda**: 4.10.1
**vue**: 3.0.0

### 三、操作流程
#### 3.1 数据集收集
爬虫代码在bilibili_week.py文件中，可在Pycharm中直接执行。b站提供了API接口以便开发者获得每一期《每周必看》的视频数据(https://api.bilibili.com/x/web-interface/popular/series/one?number={},花括号内填入要收集数据的期数)，直接使用requests库发送请求并将得到的响应进行保存即可，在发送请求时还添加了headers将其伪装为浏览器访问。
但是重复使用相同的user-agent很容易被网站识别为爬虫程序，借助python中fake_useragent第三方模块，在每一次发送请求时随机使用一个UA，并且设置retry让每一次的代码等到成功运行当前数据的爬虫后才能进行下一步操作。爬取后的数据直接转为json格式并保存下来，最终的爬虫主要代码如下：

爬取截止至 2024 年 12 月 4 日的 297 期视频数据，保存为 JSON 格式文件。
#### 3.2 数据预处理
选择有效数据，处理异常数据与空值。
使用文本数据处理，合并数据并上传至 HDFS，保存为 bilibili_week.txt。
#### 3.3 数据分析
使用 Spark SQL 分析数据，统计 UP 主的入选次数及播放量等。
使用 Spark MLlib 训练机器学习模型，分析互动数据与热搜排名的关系。
#### 3.4 可视化
使用 vue3 和 echarts 对分析结果进行可视化，包括柱状图、词云图及热力图。
### 四、结果与讨论
通过数据分析，发现搞笑、明星、游戏类视频受欢迎，同时生活类视频也能引起共鸣。
可视化结果展示了不同维度数据的分析情况，助于更好理解用户偏好。
### 五、遇到的问题与解决方案

### 六、实验总结


### 七、参考资料
爬虫代码参考: 
Python Spark 数据分析案例: 
echarts 可视化文档: 
感谢您查看本文档。如有任何问题，请随时联系我。
