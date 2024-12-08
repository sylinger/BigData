# README
## 实验：基于Spark的数据分析与处理
### 学生信息
#### **学院**: 数据学院
#### **年级**: 研一
| 姓名 | 学号 | 分工 |
|-----|-----|-----|
| 范心原 | 51275903091 | 统筹设计 github ppt 文档编写 答辩讲解 |
| 郑兴泽 | 51275903120 | 数据采集及处理 |
| 邵雅玲| 51275903102 | spark数据分析 |
| 陈冰鑫 | 51275903090 | 可视化展示 |
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
[六、补充说明](#六补充说明)  
[七、参考资料](#七参考资料)  

### 一、实验目的
Bilibili(简称b站) 是中国年轻人高度聚集的文化社区和视频平台，人们可以通过弹幕、评论、点赞或收藏等方式来与视频发布者(称为up主)来进行互动。《每周必看》是b站的一个栏目， b站会对新一周发布的视频根据不同条件进行筛选，将热门的、有趣的、有价值的视频收录在该栏目中推荐给用户观看。这次实验中，希望对被收录在b站《每周必看》视频与up主的数据信息进行研究，通过运用大数据处理框架 Spark、Hadoop 及数据可视化技术，对这些数据进行存储、处理和分析，并对每个收录视频能否进入热搜榜前10进行分类。具体来说本次作业实现功能如下：  
(1)采用爬虫技术，编写代码收集截止至5月20日b站所有《每周必看》栏目的数据；  
(2)对原始数据进行清洗，包括有价值字段的选择、异常数据的删除以及文本数据的修正等，最后数据保存为txt文件并上传至HDFS；  
(3)使用spark sql组件对HDFS的数据进行分析，主要统计各收录视频的基本播放情况以及up主的累计数据；  
(4)使用spark MLlib组件对HDFS的数据进行分析，研究视频点赞数、播放量、互动热度等之间的关系，并训练机器学习模型对视频能否进入热搜榜前十进行分类；  
(5)使用pyecharts工具对分析结果进行可视化。  
![每周必看](image/B站每周必看栏目.png)
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
```python
@retry(tries=5, delay=5)
def getWeek_json(url, json_path):
    print('正在爬取数据，url为：{}'.format(url))
    # headers信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 SLBrowser/9.0.5.9101 SLBChan/25 SLBVPV/64-bit",
        "Referer": "https://www.bilibili.com/",
        "Origin": "https://www.bilibili.com/",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "DedeUserID=253765121; DedeUserID__ckMd5=8b204e33e8749e9f; rpdid=|(J|YkuJ~mYl0J'uY)l))|k|); LIVE_BUVID=AUTO2216863966706138; buvid_fp_plain=undefined; enable_web_push=DISABLE; CURRENT_FNVAL=4048; home_feed_column=5; FEED_LIVE_VERSION=V_WATCHLATER_PIP_WINDOW3; PVID=1; buvid3=728C5EC6-5E1A-0716-F5E1-E908372396AC82000infoc; b_nut=1717491682; _uuid=96EC5CDB-7311-D6CA-36AC-745478634EAD83478infoc; header_theme_version=CLOSE; buvid4=310C4DC4-04D6-7F17-9640-8CB5C34DB30F75093-024110307-nNMmHe4Tv0n7wnXnmwBcgA%3D%3D; fingerprint=c9717eea2899312e53a904b9fa78e511; buvid_fp=c9717eea2899312e53a904b9fa78e511; bp_t_offset_253765121=1003208342056730624; match_float_version=ENABLE; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MzMzODYyMTgsImlhdCI6MTczMzEyNjk1OCwicGx0IjotMX0.2Ej8ERf0r5lOowDgICaAwPAIjZoTQvpBkh21impgr9w; bili_ticket_expires=1733386158; CURRENT_QUALITY=16; browser_resolution=1488-720; SESSDATA=e1daf441%2C1748836071%2C3dfa9%2Ac1CjBaHAY7ANkSx6gh-Lgfo9j_awxqTFnyx82H9BCSEVl6pU6XCa_XeRDmt2PIId1EqooSVnRzanZaUXJ0U2xWRjdjaExBTVN5ZnNELXRGdWlIOEhkeTF5MnVUcXU5Q1d3QjJJWThGSnc2dmdwamxoUjR1em9vX09ORlR3bW43N2h3QXlVWmRvZzVnIIEC; bili_jct=53c18dc5192ddb5318c6180ef74c9748; sid=dlppcwpv; b_lsid=99543F410_19390480EB7",
    }
    try:
        # 获取响应，转为json格式并保存
        response = requests.get(url=url, headers=headers, timeout=10)
        response.raise_for_status()
        response_data = response.json()
        if response_data.get("code") != 0:
            print(f"请求失败，code: {response_data.get('code')}, message: {response_data.get('message')}")
            return
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(response_data, f, ensure_ascii=False)
        print('数据爬取成功，保存到：{}'.format(json_path))
    except requests.exceptions.RequestException as e:
        print('请求失败：{}'.format(e))
        raise
    # 在请求结束后，增加随机的休眠时间，确保不会被反爬
    sleep_time = random.uniform(3, 7)  # 3 到 7 秒之间随机
    time.sleep(sleep_time)
```

爬取截止至 2024 年 12 月 4 日的 297 期视频数据，保存为 JSON 格式文件至当前目录的./data目录下。
```python
if __name__ == '__main__':
    # 官方api
    url = 'https://api.bilibili.com/x/web-interface/popular/series/one?number={}'
    # 爬虫数据存储路径
    data_folder = './data'
    os.makedirs(data_folder, exist_ok=True)
    # 开始爬虫
    for i in range(1, 298):
        print('开始爬取第{}期数据'.format(str(i)))
        URL = url.format(str(i))
        # 每周数据存储路径
        json_fpath = os.path.join(data_folder, 'week_{}.json'.format(str(i)))
        getWeek_json(URL, json_fpath)
```
![json保存2](image/fig_original/3.png)
#### 3.2 数据预处理
数据预处理阶段包括了有效数据的选择、异常数据与空白数据的处理、文本数据的处理，这一步的代码在data_preprocess.py中，可在Pycharm中直接执行。  
(1)数据选择：打开上一步爬虫得到的其中一个json数据文件，借助菜鸟工具提供的json格式化工具，查看爬取到的数据格式，返回的信息包含在data中：
使用文本数据处理，合并数据并上传至 HDFS，保存为 bilibili_week.txt。  
data包括3个部分的信息，其中config包括这一期视频栏目的整体信息，包括期数、时间、封面视屏内容等，其中config.name记录每一个视频的所属期数；list则是这一期栏目每一个收录视频的具体情况，包括视频的标题、描述以及推荐理由；发布者的信息则包含在元素的owner部分；视频的观看次数、弹幕数、转发数等则包含在stat中.
![保存有效信息1](image/fig_original/5标记.png)  
![保存有效信息2](image/fig_original/6标记.png)  
![保存有效信息3](image/fig_original/7标记.png)  
除了这些信息，其余数据在本项目中无意义，因此对单个json文件，选取上述几个字段，将有用的信息保存在dataframe。  

```python
key = ['up', 'time', 'title', 'desc', 'view', 'danmaku', 'reply', 'favorite', \
           'coin', 'share', 'like', 'dislike','rcmd_reason', 'tname', 'his_rank']
    _df = pd.DataFrame(columns=key)
    _week = pd.read_json(json_fpath)

    # 获取每个必看视频基础的信息
    _base_info = pd.DataFrame(_week['data']['list'])
    _df[['tname', 'title', 'desc', 'rcmd_reason']] = _base_info[['tname', 'title', 'desc', 'rcmd_reason']]
    # 获取up主的信息
    _owner = _base_info['owner'].values.tolist()
    _owner = pd.DataFrame(_owner)
    _df['up'] = _owner['name']
    # 获取视频的播放信息
    _stat = _base_info['stat'].values.tolist()
    _stat = pd.DataFrame(_stat)
    _df[['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'his_rank', 'like', 'dislike']] = \
        _stat[['view', 'danmaku', 'reply', 'favorite', 'coin', 'share', 'his_rank', 'like', 'dislike']]
    _df['time'] = _week['data']['config']['name']
```


(2)异常数据的处理：
首先删除包含空值和重复的数据，其中当up主名字和视频标题相同视为重复；认为观看数view、弹幕数danmaku、评论数reply、收藏数favorite、投币数coin、分享次数share、点赞人数like、历史排名his_rank小于或等于0，不喜欢的人数dislike超过0的数据为异常数据，一并删除。上述数据删除之后，dislike字段也无意义，同样删除。这一步骤的代码如下：  
```python
 dataframe.dropna(how='any', axis=0, inplace=True)
    # 删除掉重复的数据，其中当视频标题与作者名称相同认为数据重复
    dataframe = dataframe.drop_duplicates(subset=['title', 'up'])
    # 删除掉异常的数据，认为观看数、弹幕数、回复、喜欢、投币、分享、收藏数小于或等于0，不喜欢的人数超过0则认为数据异常
    incorrect_df = dataframe.loc[(dataframe['view'] <= 0) \
                                 | (dataframe['danmaku'] <= 0) \
                                 | (dataframe['reply'] <= 0) \
                                 | (dataframe['favorite'] <= 0) \
                                 | (dataframe['coin'] <= 0) \
                                 | (dataframe['share'] <= 0) \
                                 | (dataframe['like'] <= 0) \
                                 | (dataframe['dislike'] > 0) \
                                 | (dataframe['his_rank'] <= 0)]
    # 丢弃异常数据
    dataframe = dataframe.drop(incorrect_df.index)
    # dislike数据无意义，丢弃
    dataframe = dataframe.drop(columns=['dislike'])
```
(3)文本数据的处理：
入选栏目的某些视频描述desc和推荐理由rcmd_reason为空，使用视频的标题对其进行填充，并且为了最后数据保存的规范性，对一些特殊符号例如换行符、Tab等进行处理：  
```python
# 处理描述为空的数据，使用该视频的标题进行填充
    desc_none = dataframe.loc[(dataframe['desc'] == '') | (dataframe['desc'] == '-')]
    for i in range(desc_none.shape[0]):
        dataframe.loc[desc_none.index[i], 'desc'] = dataframe.loc[desc_none.index[i], 'title']
    # 处理推荐理由为空的数据，使用该视频的标题进行填充
    rcmd_reason_none = dataframe.loc[(dataframe['rcmd_reason'] == '') | (dataframe['rcmd_reason'] == '-')]
    for i in range(rcmd_reason_none.shape[0]):
        dataframe.loc[rcmd_reason_none.index[i], 'rcmd_reason'] = dataframe.loc[rcmd_reason_none.index[i], 'title']
    # 对长文本进行处理
    dataframe['title'] = dataframe['title'].map(lambda x: x.replace(",", " "))
    dataframe['desc'] = dataframe['desc'].map(lambda x: x.replace(",", " "))
    dataframe['rcmd_reason'] = dataframe['rcmd_reason'].map(lambda x: x.replace(",", " "))
    dataframe['title'] = dataframe['title'].map(lambda x: x.replace(";", " "))
    dataframe['desc'] = dataframe['desc'].map(lambda x: x.replace(";", " "))
    dataframe['rcmd_reason'] = dataframe['rcmd_reason'].map(lambda x: x.replace(";", " "))
    dataframe['title'] = dataframe['title'].map(lambda x: x.replace("\n"," "))
    dataframe['desc'] = dataframe['desc'].map(lambda x: x.replace("\n"," "))
    dataframe['rcmd_reason'] = dataframe['rcmd_reason'].map(lambda x: x.replace("\n"," "))
    dataframe['title'] = dataframe['title'].map(lambda x: x.replace("\r"," "))
    dataframe['desc'] = dataframe['desc'].map(lambda x: x.replace("\r"," "))
    dataframe['rcmd_reason'] = dataframe['rcmd_reason'].map(lambda x: x.replace("\r"," "))
    dataframe['title'] = dataframe['title'].map(lambda x: x.replace("\t"," "))
    dataframe['desc'] = dataframe['desc'].map(lambda x: x.replace("\t"," "))
    dataframe['rcmd_reason'] = dataframe['rcmd_reason'].map(lambda x: x.replace("\t"," "))
    return dataframe
```


(4)数据合并与上传
    对每一个文件重复进行上述操作，并不断合并得到的dataframe，最后将数据去除表头，保存为文本文件，命名bilibili_week.txt.在Linux 终端输入./bin/hdfs dfs -put /home/Hadoop/PycharmProjects/BigData/bilibili_week.txt  /user/hadoop，将该文件上传至HDFS，通过ls命令和网页浏览，可以验证数据成功上传。  
```python
# 合并所有的json
def merge_data(json_data, save_path):
    key = ['up', 'time', 'title', 'desc', 'view', 'danmaku', 'reply', 'favorite', \
           'coin', 'share', 'like', 'dislike','rcmd_reason', 'tname', 'his_rank']
    df = pd.DataFrame(columns=key)
    # 依次处理每周的数据并进行合并
    for each_json in json_data:
        _df = select_data(each_json)
        df = pd.concat([df, _df], ignore_index=True)
    # 进行数据处理
    df = clean_data(df)
    # 保存为txt文件
    df.to_csv(save_path, header=None, index=None, sep='\t', mode='w')

if __name__ == '__main__':
    # 读取所有的json数据
    json_data = glob(os.path.join('./data', '*.json'))
    #最后的数据保存路径
    save_dir = 'bilibili_week.txt'
    # 进行数据合并并存储为txt文件
    merge_data(json_data, save_dir)
```
#### 3.3 数据分析
进行数据分析前，需要将HDFS上的数据加载成RDD，然后再由RDD转为Dataframe。这一步的实现步骤为：  
①创建SparkSession和SparkContext对象，并用textFile函数读取HDFS上的文本数据，并将其存储为RDD；  
②用map函数对RDD的每个元素进行切割并转化为包含多个字段的Row对象；  
③定义数据集的结构schema，为Dataframe建立表头，将RDD转化为一个Dataframe。  
④在使用sql组件的时候还需要将DataFrame注册为Spark SQL中的临时视图。  
以上操作对应的代码如下：
```python
def initialize(txt_file):
    # 创建SparkContext和SparkSession对象
#     sc = SparkContext('local', 'spark_project')
#     sc.setLogLevel('WARN')
    spark = SparkSession.builder.getOrCreate()
    # 把数据加载为RDD，并且对每一行数据进行切割，转为Row对象
    rdd = spark.sparkContext.textFile(txt_file)\
        .map(lambda x: x.split("\t")).map(lambda x:Row(x[0],x[1],x[2],x[3],int(x[4]),int(x[5]),int(x[6]),\
                                                        int(x[7]),int(x[8]),int(x[9]),int(x[10]),x[11],x[12],int(x[13])))
    # 定义数据集结构
    fields = [StructField("up", StringType(), False), StructField("time", StringType(), False),
              StructField("title", StringType(), False),StructField("desc", StringType(), False),
              StructField("view", IntegerType(), False), StructField("danmaku", IntegerType(), False),
              StructField("reply", IntegerType(), False), StructField("favorite", IntegerType(), False),
              StructField("coin", IntegerType(), False), StructField("share", IntegerType(), False),
              StructField("like", IntegerType(), False), StructField("rcmd_reason", StringType(), False),
              StructField("tname", StringType(), False), StructField("his_rank", IntegerType(), False), ]
    schema = StructType(fields)
    # 将RDD转为Dataframe
    data = spark.createDataFrame(rdd, schema)
    # 注册sql临时视图
    data.createOrReplaceTempView("data")
    return spark
```
(1)基于spark sql组件的分析
这一部分的代码都在data_analysize1.py文件中，通过spark-submit data_analysize1.py 执行代码。
①统计视频收录次数最多的up主
b站up主的名字不可以重复，因此每个up主由字段’up’唯一标识，数据中up主视频被收录的总次数为count(up)，要求得到的结果根据名字up分组并按照入选的次数降序排序，筛选出10个视频入选次数最多的up，得到的popular_up为spark.DataFrame类型，再使用toPandas将其转为pandas.Dataframe并通过to_csv函数把结果保存在csv文件中。这一过程的代码如下：
```python
# 入选次数最多的10个up主
def top_popular_up(spark,base_dir):
    popular_up = spark.sql(
        "SELECT up,COUNT(up) AS popular_up_times FROM data GROUP BY up ORDER BY popular_up_times DESC LIMIT 10")
    data = popular_up.toPandas()
    save_dir = os.path.join(base_dir,'top_popular_up.csv')
    data.to_csv(save_dir,index=False)
```
②统计入选次数最多的视频分类
与①类似，tname表示入选视频的视频分区，count(tname)表示属于该种分区视频的收录次数，要求得到的结果根据tname分组并按照入选的次数降序排序，筛选出10个收录次数最多的视频分区，得到的popular_subject用toPandas将其转为pandas.Dataframe并通过to_csv函数把结果保存在csv文件中。这一过程代码如下：
```python
# 入选次数最多的10个主题
def top_popular_subject(spark,base_dir):
    popular_subject = spark.sql(
        "SELECT tname,COUNT(tname) AS popular_subject_times FROM data GROUP BY tname ORDER BY popular_subject_times DESC LIMIT 10")
    data = popular_subject.toPandas()
    save_dir = os.path.join(base_dir,'top_popular_subject.csv')
    data.to_csv(save_dir, index=False)
```
③播放量数据统计
对于视频播放量的统计，选取视频标题title和播放量view的字段，对查询结果按照view字段进行降序排序并筛选播放量最多的10个视频，将其转为Pandas.dataframe并保存在csv文件中，对应代码如下：
```python
def top_popular_view(spark,base_dir):
    view_data = spark.sql(
        "SELECT title,view AS view_data FROM data ORDER BY view DESC LIMIT 10")
    data = view_data.toPandas()
    save_dir = os.path.join(base_dir, 'video_view_data.csv')
    data.to_csv(save_dir,index=False)
```
对于up主所有收录视频的累计播放量统计，选取up主名字up并计算每个up主的总播放量sum(view)，对查询结果按照up的名称进行分组，并按照总播放量sum(view)降序排序并筛选总次数最多的10个up主名字，查询结果同样通过toPandas()和to_csv()保存在csv文件中，代码如下：
```python
 view_data = spark.sql(
        "SELECT up,sum(view) AS view_data FROM data GROUP BY up ORDER BY sum(view) DESC LIMIT 10")
    data = view_data.toPandas()
    save_dir = os.path.join(base_dir, 'up_view_data.csv')
    data.to_csv(save_dir,index=False)
```
弹幕数、视频回复量、收藏次数、投币数、分享次数和点赞次数最多的前10个视频和up主的数据统计与上述操作类似，只需要修改sql语句中select相应的字段，这里就不再展开。
④词频统计
为了研究标题、视频简介、推荐理由等常用词，需要进行词频统计，以视频标题分析为例，对视频标题的词频分析步骤如下：
```python
def word_count(spark, base_dir):
    # 统计标题所有词的词频
    wordCount_title = spark.sql("SELECT title as title from data").rdd.flatMap(
        lambda line: pretty_cut(line['title'])).map(lambda word: (word, 1)).reduceByKey(
        lambda a, b: a + b).repartition(1).sortBy(lambda x: x[1], False)
```
```python
def pretty_cut(sentence):
    cut_list = jieba.lcut(''.join(re.findall('[\u4e00-\u9fa5]', sentence)), cut_all=False)
    for i in range(len(cut_list) - 1, -1, -1):
        if cut_list[i] in stopwords:
            del cut_list[i]
    return cut_list
```
每一行数据分词之后，再通过map(lambda word: (word, 1)) 将每个词映射为一个键值对，key是单词，1表示单词出现的次数是1，reduceByKey(lambda a, b: a + b)则对RDD中的每个键值对进行聚合，将相同键的值相加，得到每个单词出现的总次数。repartition将RDD的分区数设置为1， sortBy会按照每个单词出现的次数进行降序排序，得到出现频率最高的单词。  
简单起见，在将RDD转为Dataframe后，只选取词频前300且不为空的词语，保存为csv文件。最后main函数依次执行上述等函数。  
(2)基于spark MLlib组件的分析
这一部分的代码都在data_analysize2.py文件中，通过spark-submit data_analysize2.py 执行代码。  
①数据处理  
读取到HDFS数据之后，选择其中几组字段：['view','danmaku','reply','favorite','coin','share','like']进行分析，研究这几组变量与当周历史排名his_rank之间的关系。通常情况下人们比较关心热搜榜前10的数据，因此将数据划分为两类并新增label标签：1说明该条视频曾经进入b站热搜榜前10，0说明该视频不曾进入热搜榜前十。数据筛选和新增对应代码如下：
```python
def transform_data(df):
    # 删除掉无用的数据
    df = df.drop('up')
    df = df.drop('time')
    df = df.drop('title')
    df = df.drop('desc')
    df = df.drop('rcmd_reason')
    df = df.drop('tname')
    # 根据历史排名his_rank，新增类别标签label
    df = df.withColumn('label', when(df.his_rank <= 10, 1).otherwise(0))
```
为了方便后续使用机器学习模型进行训练和验证，使用VectorAssembler类将数据转化为特征向量：
```python
    required_features = ['view','danmaku','reply','favorite','coin','share','like']
    assembler = VectorAssembler(
        inputCols=required_features,
        outputCol='features')
    transformed_data = assembler.transform(df)
```
最后对数据按照8:2划分训练集和验证集：
```python
 #对数据进行划分
    (training_data, test_data) = transformed_data.randomSplit([0.8, 0.2], seed=2023)
    print("训练数据集总数: " + str(training_data.count()))
    print("测试数据集总数: " + str(test_data.count()))
    return transformed_data,training_data,test_data
```
②变量的相关性  
使用pyspark.ml.stat中的Correlation，计算特征之间的斯皮尔曼系数，并将结果保存在csv文件中：  
```python
def corr_matrix(df,cor_save_dir):
    cor_mat = Correlation.corr(df, "features", "spearman").head()[0]
    cor_df = pd.DataFrame(cor_mat.toArray())
    cor_df.columns = ['view','danmaku','reply','favorite','coin','share','like']
    cor_df.to_csv(cor_save_dir, index=False)
```
③分类器的训练  
根据['view','danmaku','reply','favorite','coin','share','like']和label标签，训练分类器，让分类器根据视频的播放量、评论数等判断它是否可以进入热搜榜前10。pyspark.ml.classification提供多种封装好的分类模型，在这次实验中选择逻辑回归、决策树、随机森林和GBT进行实验。
以逻辑回归分类器为例，首先定义分类器：设置标签列为label，特征列为features，并且逻辑回归最大迭代15次。  
为了研究分类器的性能，使用MulticlassClassificationEvaluator统计模型在验证集上的分类正确率，使用BinaryClassificationEvaluator得到模型二分类的auc。这两个数值越高，说明模型性能越好。  
```python
def LogisticReg(training_data,test_data):
    # 实例化逻辑回归算法
    lr = LogisticRegression(labelCol='label',featuresCol='features',maxIter=15)
    # 进行模型训练
    model = lr.fit(training_data)
    # 进行模型验证
    lr_predictions = model.transform(test_data)
    # 计算分类acc
    multi_evaluator = MulticlassClassificationEvaluator(
        labelCol='label', metricName='accuracy')
    acc = multi_evaluator.evaluate(lr_predictions)
    print('LogisticRegression classifier Accuracy:{:.4f}'.format(acc))
    # 计算模型auc
    binary_evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction", labelCol="label",
        metricName="areaUnderROC")
    auc = binary_evaluator.evaluate(lr_predictions)
    print('LogisticRegression classifier Auc:{:.4f}'.format(auc))
    return ['LogisticRegression',acc,auc]
```
其余三种分类器(决策树算法、随机森林算法和GBT)的训练与验证过程和上述操作类似，这里不再赘述。这四种分类器依次训练：各自正确率和AUC的结果如下，该数据也会保存在csv文件中：
![数据结果](image/1.png)  

#### 3.4 可视化
使用 vue3 和 echarts 对分析结果进行可视化，包括柱状图、词云图及热力图。  
如下图给出部分示例。  
![每周必看](image/show2.png)
![每周必看](image/show3.png)
![每周必看](image/show1.png)
![每周必看](image/show4.png)
![每周必看](image/show5.png)
![每周必看](image/show6.png)
![每周必看](image/show7.png)
![每周必看](image/show8.png)

### 四、结果与讨论
通过数据分析，发现搞笑、明星、游戏类视频受欢迎，同时生活类视频也能引起共鸣。
可视化结果展示了不同维度数据的分析情况，助于更好理解用户偏好。
### 五、遇到的问题与解决方案
b站每个视频的数据，比如播放量、评论数、弹幕数等等都是会不断更新的，因此每一次运行代码得到的结果例如播放量、转发次数等都会不同，报告及可视化中的结果显示的是截止至12月4日各个视频的数据情况。但就整体而言，短时间内微小的变化量不影响整体的分析结果。

### 六、补充说明
代码文件目录为BigData，数据集也包含在其中。文件目录格式如下：  
data：存放爬虫得到json文件的路径；  
bilibilishow：数据可视化前端代码；  
static：使用spark得到的分析结果；  
bilibili_week.txt：对爬虫数据清洗后的数据集，也是最终上传到HDFS的数据集；  
bilibili_weekly.py：爬虫代码；  
chineseStopWords.txt：中文停用词，用于对文本进行分词；  
data_analysize1.py：使用spark sql组件分析的代码；  
data_analysize2.py：使用spark MLlib组件分析的代码；  
data_process.py：数据处理代码；  
requirements.txt：代码所需的第三方库。  
image：readme中使用的图库。  

### 七、参考资料
(1)b站爬虫代码参考：
https://www.heywhale.com/mw/project/6059c0f0c910a9001581c98b  
(2)python spark数据分析案例：https://dblab.xmu.edu.cn/blog/2738/  
(3)vue文档：[https://pyecharts.org/#/zh-cn/intro  ](https://cn.vuejs.org/guide/introduction.html)
(4)echarts文档：https://echarts.apache.org/handbook/zh/get-started/
感谢您查看本文档。如有任何问题，请随时联系我。
