# 智能数据工程课程知识图谱系统

这个系统用于构建"智能数据工程"课程的知识图谱，包括数据生成、存储、知识图谱构建、信息抽取和问答功能。

## 系统架构

系统由以下模块组成：

1. 数据库管理模块 (db_manager.py)**: 负责MySQL数据库的连接、表创建和数据操作
2. 数据生成模块 (data_generator.py)**: 生成课程相关的结构化数据
3. 知识图谱模块 (knowledge_graph.py)**: 负责Neo4j知识图谱的构建和查询
4. 信息抽取模块 (information_extraction.py)**: 从文本中提取结构化信息
5. 主应用程序 (main.py)**: 整合所有模块，提供命令行接口

## 安装要求

- Python 3.7+
- MySQL 8.0+
- Neo4j 4.0+

## 安装步骤

1. 克隆仓库：
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

3. 确保MySQL服务已启动，并创建数据库：
   ```
   CREATE DATABASE MySQL80;
   ```

4. 确保Neo4j服务已启动，默认端口为7474，用户名和密码分别为neo4j和1

## 使用方法

系统提供命令行接口，可以通过以下参数控制不同的功能：

```
python main.py [options]
```

可用选项：

- `--setup`: 设置数据库并创建必要的表
- `--generate`: 生成课程数据
- `--build-kg`: 构建知识图谱
- `--populate-db`: 用课程数据填充数据库
- `--extract <file>`: 从文本文件提取信息
- `--qa`: 启动交互式问答系统
- `--all`: 运行所有步骤

### 示例

1. 运行完整流程：
   ```
   python main.py --all
   ```

2. 仅设置数据库：
   ```
   python main.py --setup
   ```

3. 仅启动问答系统：
   ```
   python main.py --qa
   ```

4. 从文本文件提取信息：
   ```
   python main.py --extract data/course_text.txt
   ```


## 问答系统

可以询问以下类型的问题：

1. 这门课程是什么？
2. 课程包含哪些章节？
3. 某个章节包含哪些知识点？
4. 某个知识点有哪些学习资源？

## 贡献

欢迎提交问题和改进建议！
