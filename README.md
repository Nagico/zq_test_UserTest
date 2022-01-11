## zq_UserTest

该项目仅供测试，请勿用于生产环境。

### 本地使用

请确保安装 python 3.8 及以上的版本，并进行虚拟环境配置。推荐使用 conda 进行虚拟环境管理。

#### 虚拟环境

- 使用 Conda（推荐）

事先安装好 conda，并将其设置为环境变量。

```shell
conda create -n zq_UserTest_dev python=3.8
conda activate zq_UserTest_dev
```

- 使用 python 默认 venv（方便）

具体的激活路径请参考使用的终端类型以及 `\venv\Scripts\` 目录。

```shell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

- 直接使用 python（也可以）

### 安装依赖

```shell
pip install -r requirements.txt
```

### 迁移数据库

```shell
python manage.py migrate
```

### 启动服务

```shell
python manage.py runserver
```