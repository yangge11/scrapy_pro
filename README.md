# scrapy_pro

#### 项目背景   
做了挺久爬虫开发，接过各种各样的站点爬虫处理，过程中也遇到过各种各样的问题；
偶尔会逛逛社区和群，依旧会看到各种各样的小白在上面问些简单问题，却陷入无人回答的尴尬境地，原因有两种：
1. 问问题不懂怎么问，导致有些大咖看到了不知道咋回你
2. 问题问的还可以，但是毕竟大家都忙，有时候想回你，但是手上有事，等到没事了，也忘了
所以，我希望这个项目，能涉及到爬虫里面的各个技术点（详见技术点），让大家进行一个毕竟好的归纳总结
关于项目名称scrapy_auto的由来：
scrapy自动化，不得不说scrapy是个非常高效实用的框架，因此，本项目初衷是站在scrapy的角度，追求更高效，更快捷，更实用，针对使用scrapy的各种问题，针对性解决

#### Version
1. 基本架构搭建，jieba分词处理，数据标签属性清洗 
2. Version1.0. 
新增boss直聘爬虫，抓取boss各类别岗位，并进行词云统计；
新增岗位搜索词轮询接口，接口暂时只抓取固定岗位词；
3. Version1.0.1. 
boss直聘爬虫完成，采用定页面层级的方式减少访问次数，提高性能
4. Version1.0.2. 
数据入库存储；
数据更新功能由于时间有限，暂时做全量更新（最好的方式是根据url对应的待抓取内容，进行和原来的抓取内容的md5比较）
5. Version1.0.3. 
增加数据的可视化分析
6. Version1.0.4. 
增加可視化html頁面
7. Version1.0.5. 
重大改动：鉴于py2编码的麻烦以及py2官方维护截止到2020年元旦，本项目由py2=》py3进行转换
8. Version1.0.6. 
新增头条号文章抓取的增量和全量抓取,对接scrapy-splash
9. Version1.0.7. 
新增蓝奏云盘数据采集
Version1.0.8. 安装启动教程

#TODO:
1. 根据不同的岗位，生成对应的分布图及对应的词库（时间有限目前暂时是几个demo数据）——
2. scrapy=>scrapy-redis的转换、代理设置——

#### 相关爬虫技术点
本站点作为开源项目，希望针对各类不同的网站抓取的实例分析，能让大家在爬虫技术上能有更大的发展
1. 爬虫系统架构搭建（目前采用scrapy系统）
2. 分布式爬虫系统搭建（scrapy-redis）
3. 各种站点的反爬处理（包括登录、cookie验证、UA、请求数据加密计算、页面数据加密破解、js破解、js动态加载、ajax加载数据、ip封禁、多层数据加密计算、验证码等）
4. 日志监控系统
5. 爬虫性能优化
6. 存储数据的方式及性能优化
7. 广度优先和深度优先的抓取
8. 爬虫运行状态及相应抓取数据监控

#### 可能遇到的问题及解决方式

q：ImportError: No module named win32api
a：pip install pypiwin32

q: error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
a：https://segmentfault.com/a/1190000014782698

q: AttributeError: module 'pip' has no attribute 'main'
a: python -m pip install --upgrade pip==9.0.3

q: python进行批量的py2=>py3转换
a: https://blog.csdn.net/u012211419/article/details/51136232

q: jinja2.exceptions.TemplateSyntaxError: unexpected char '\x9d' at 734926
a: 时间有限,暂时无太好的方式,参照:https://blog.csdn.net/qq_39241986/article/details/80680392

q: distutils.errors.DistutilsError: Could not find suitable distribution for Requirement.parse('pytest-runner')
a: pip install pytest-runner

### 需求背景： 
1. 抓取招聘网站数据，用于统计各个岗位薪资、地域分布、技能关键词排名、==》demo_spider.py
2. 抓取头条号文章数据：
    1）时效性：尝试5分钟进行一次目录轮巡的数据抓取，以文章url作为唯一区分标准
    2）抓取字段内容（待定）：

### 技术点
解决js加载问题：
无头浏览器（性能差）；scrapy-splash


### 安装启动
以蓝奏云盘为例：
cd 你的code目录/scrapy_pro/
pip install -r requirements.txt
scrapy crawl lanzhou_spider -o items.json
程序跑完后可以在项目目录下查看items.json数据

