## zq_UserTest

该项目仅供测试，请勿用于生产环境。

## 本地使用

请确保安装 python 3.8 及以上的版本。

### Windows

打开 `start.cmd` 即可

### Linux / OSX

安装 python3 及其 venv 包

使用 `python3 -m venv venv` 创建 venv 环境，并执行 `source venv/bin/activate` 进入依赖环境

执行 `python3 -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple` 安装依赖

执行 `python3 manage.py migrate` 创建数据库表

执行 `python3 manage.py runserver` 启动服务

**以后使用时只需要执行最后一行命令启动服务即可**

## 重置数据

文件夹根目录下 `db.sqlite3` 文件是后台数据库，如需重置数据，请删除该文件。

- windows 下重新打开 `start.cmd` 即可
- 其他系统需要执行 `python3 manage.py migrate` 创建数据库表，再执行 `python3 manage.py runserver` 启动服务