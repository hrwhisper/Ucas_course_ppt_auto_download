# UCAS 课件自动下载

## 使用方法

两种使用方法。

### 小白用户

该方法直接运行exe文件，exe文件可以在https://github.com/hrwhisper/Ucas_course_ppt_auto_download/releases 中下载

修改**private.txt**文件，然后运行main.exe即可(建议使用PowerShell运行)。

ps: 

- private.txt与main.exe在**同一目录**下即可



### 高级用户

修改根目录的private文件，然后python main.py即可。

需要全部的环境（包括python），见下方环境要求，以及参考对应的安装方法

> 可以设置alias实现快速调用，或者添加计划任务每天自动同步


### private文件说明

private中，各行表示意义如下：

1. 第一行为登录选课系统的账号
2. 第二行为密码
3. 第三行为要保存的路径
4. 第四行为当前的学期，如16-17春季（没有则全部下载）



##环境要求

- python 3.5.2
- requests 2.11
- BeautifulSoup
- 可选环境：
  - PIL
  - Tesseract-OCR

### 安装方法
- pip install beautifulsoup4
- pip install requests
- pip install Pillow
- 登录网址默认为 http://onestop.ucas.ac.cn/home/index ，如果为这个网站挂了，将使用sep.ucas.as.cn 登录，当你在校外的时候那么需要在安装如下环境以支持验证码识别：
  - Tesseract-OCR
    - windows下安装：http://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-3.05.00dev.exe
      - 安装时候勾选Registry settings
    - Linux  \  MAC OS X安装见 https://github.com/tesseract-ocr/tesseract/wiki




## 其它

- 暂时没有android / IOS的计划。
- 建议云盘如OneDrive连用，这样在电脑上下载到OneDrive文件夹中，手机上也可以收到。
- **觉得好用点个star吧~**

## 更新说明
- 更新适配到2019年秋季
- 新增登陆网址，不用验证码
- 修复因为微软CMD下编码不一致导致程序crash
- 支持最新验证码登录（校内校外不一致）
  - 校内不需要验证码，校外需要
- 多线程下载
- 自定义当前学期，只下载当前学期的课程PPT
- 修复文件夹判断问题（有的老师课件命名没有'.'）
- 添加EXE执行程序（使用 PyInstaller 打包）
- 修复课件名称含有空格导致解析失败问题
- 修复课件里文件夹没有遍历下载的问题
- 修复部分课程给出链接后下载失效(如计算机算法设计与分析,老师给出两个链接)


