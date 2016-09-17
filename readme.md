#UCAS 课件自动下载

## 使用方法

两种使用方法。

### 小白用户

修改easy_use/private文件，然后运行main.exe即可

#### 环境要求
需要下载安装 python 3.5.2 https://www.python.org/ftp/python/3.5.2/python-3.5.2.exe

### 高级用户

修改根目录的private文件，然后python main.py即可。

#### 环境要求
- python 3.5.2
- requests 2.11
- BeautifulSoup

### private文件说明

private中，各行表示意义如下：

1. 第一行为登录选课系统的账号
2. 第二行为密码
3. 第三行为要保存的路径



## 更新说明
- 使用 cx-Freeze 打包成exe
- 修复课件名称含有空格导致解析失败问题
- 修复课件里文件夹没有遍历下载的问题
- 修复部分课程给出链接后下载失效(如计算机算法设计与分析,老师给出两个链接)
- 添加EXE执行程序

