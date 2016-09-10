#UCAS 课件自动下载

## 使用方法

两种使用方法。

### 小白用户

修改easy_use/private文件，然后运行main.exe即可

### 高级用户

修改根目录的private文件，然后python main.py即可。

### private文件说明

private中，各行表示意义如下：

1. 第一行为登录选课系统的账号
2. 第二行为密码
3. 第三行为要保存的路径（请提前建立好）



## 环境说明
- python 3.5.2
- requests 2.11
- BeautifulSoup
- 使用 cx-Freeze 打包成exe

## 更新说明

- 修复部分课程给出链接后下载失效(如计算机算法设计与分析,老师给出两个链接)
- 添加EXE执行程序

