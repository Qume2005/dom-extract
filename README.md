# Dom-extract

> 一个简单易用的html清洗器，提取出干净的html文本

## 安装*poetry*

> 官网教程

### *pipx*（推荐）

#### 安装*pipx*

> 官网教程 https://pipx.pypa.io/stable/

#### 安装*poetry*

```bash
pipx install poetry
```

## 快速使用dom-extract

> 确保已经安装*poetry*

```bash
git clone https://github.com/Qume2005/dom-extract.git
cd ./dom-extract
```



### 依赖安装&*poetry*初始化

```bash
poetry install
```

### 默认参数（input = ./texts output = ./output）

```bash
poetry run extract
```

### 自定义参数

```bash
poetry run extract --input ./texts --output ./output
```

# 简易文档

## input参数

> 示例：poetry run extract --input ./costumed_input

input参数指定输入文件夹目录，该文件夹中存放待清洗文件，清洗后以html标题重命名文件名

## output参数

> 示例：poetry run extract --output ./customed_output

output参数指定输出文件夹目录，是清洗结果的保存目录

