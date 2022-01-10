# fastmysql
![](https://img.shields.io/badge/Python-3.8.6-green.svg)

#### 介绍
简单快速的使用mysql

#### 软件架构
软件架构说明


#### 安装教程

1.  pip安装
```shell script
pip install fastmysql
```
2.  pip安装（使用淘宝镜像加速）
```shell script
pip install fastmysql -i https://mirrors.aliyun.com/pypi/simple
```

#### 使用说明

1.  demo
```python
import fastmysql
query_res = fastmysql.query_table_all_data(db_name='test', tb_name='test')
```
