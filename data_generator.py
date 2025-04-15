import random
import json
import os

class DataEngineeringDataGenerator:
    def __init__(self):
        self.course_name = "智能数据工程"
        self.course_description = "一门关于数据工程智能化的课程，涵盖数据采集、处理、存储、分析和可视化等全流程"
        
        # 课程章节数据
        self.chapters = [
            {
                "name": "数据采集与预处理",
                "description": "包括数据源识别、数据清洗、数据转换等内容",
                "order": 1,
                "topics": [
                    {
                        "name": "数据源类型",
                        "description": "结构化数据、半结构化数据、非结构化数据等不同类型数据源的特点和应用场景",
                        "resources": [
                            {"name": "数据源类型概述", "type": "文档", "url": "https://example.com/data-sources"},
                            {"name": "数据源类型视频教程", "type": "视频", "url": "https://example.com/data-sources-video"}
                        ]
                    },
                    {
                        "name": "数据清洗技术",
                        "description": "数据清洗的基本概念、方法和工具，包括处理缺失值、异常值、重复值等",
                        "resources": [
                            {"name": "数据清洗技术指南", "type": "文档", "url": "https://example.com/data-cleaning"},
                            {"name": "Python数据清洗实战", "type": "代码示例", "url": "https://example.com/data-cleaning-python"}
                        ]
                    },
                    {
                        "name": "ETL流程",
                        "description": "数据提取、转换和加载的完整流程，以及相关工具和最佳实践",
                        "resources": [
                            {"name": "ETL流程设计", "type": "文档", "url": "https://example.com/etl-process"},
                            {"name": "ETL工具比较", "type": "文档", "url": "https://example.com/etl-tools"}
                        ]
                    },
                    {
                        "name": "数据质量评估",
                        "description": "数据质量评估的标准、方法和工具，以及如何建立数据质量监控体系",
                        "resources": [
                            {"name": "数据质量评估框架", "type": "文档", "url": "https://example.com/data-quality"},
                            {"name": "数据质量监控系统设计", "type": "文档", "url": "https://example.com/data-quality-monitoring"}
                        ]
                    }
                ]
            },
            {
                "name": "数据存储与管理",
                "description": "包括数据库设计、数据仓库、数据湖等内容",
                "order": 2,
                "topics": [
                    {
                        "name": "关系型数据库",
                        "description": "关系型数据库的基本概念、设计原则和主流产品，如MySQL、PostgreSQL等",
                        "resources": [
                            {"name": "关系型数据库基础", "type": "文档", "url": "https://example.com/relational-db"},
                            {"name": "数据库设计最佳实践", "type": "文档", "url": "https://example.com/db-design"}
                        ]
                    },
                    {
                        "name": "NoSQL数据库",
                        "description": "NoSQL数据库的类型、特点和应用场景，包括文档型、键值型、列族型和图数据库",
                        "resources": [
                            {"name": "NoSQL数据库概述", "type": "文档", "url": "https://example.com/nosql"},
                            {"name": "MongoDB实战教程", "type": "视频", "url": "https://example.com/mongodb-tutorial"}
                        ]
                    },
                    {
                        "name": "数据仓库架构",
                        "description": "数据仓库的架构设计、ETL流程、OLAP分析等内容",
                        "resources": [
                            {"name": "数据仓库设计指南", "type": "文档", "url": "https://example.com/data-warehouse"},
                            {"name": "星型模式与雪花模式", "type": "文档", "url": "https://example.com/star-snowflake"}
                        ]
                    },
                    {
                        "name": "数据湖技术",
                        "description": "数据湖的概念、架构、存储格式和处理方法",
                        "resources": [
                            {"name": "数据湖与数据仓库对比", "type": "文档", "url": "https://example.com/data-lake-vs-warehouse"},
                            {"name": "Delta Lake实战", "type": "代码示例", "url": "https://example.com/delta-lake"}
                        ]
                    }
                ]
            },
            {
                "name": "数据处理与分析",
                "description": "包括批处理、流处理、数据分析方法等内容",
                "order": 3,
                "topics": [
                    {
                        "name": "批处理框架",
                        "description": "大数据批处理框架的原理和应用，如Hadoop、Spark等",
                        "resources": [
                            {"name": "Hadoop生态系统", "type": "文档", "url": "https://example.com/hadoop"},
                            {"name": "Spark核心概念", "type": "视频", "url": "https://example.com/spark-core"}
                        ]
                    },
                    {
                        "name": "流处理技术",
                        "description": "实时数据流处理的技术和框架，如Kafka、Flink等",
                        "resources": [
                            {"name": "流处理基础", "type": "文档", "url": "https://example.com/stream-processing"},
                            {"name": "Kafka入门教程", "type": "视频", "url": "https://example.com/kafka-tutorial"}
                        ]
                    },
                    {
                        "name": "机器学习算法",
                        "description": "常用机器学习算法在数据处理中的应用",
                        "resources": [
                            {"name": "机器学习算法概述", "type": "文档", "url": "https://example.com/ml-algorithms"},
                            {"name": "Scikit-learn实战", "type": "代码示例", "url": "https://example.com/scikit-learn"}
                        ]
                    },
                    {
                        "name": "数据挖掘方法",
                        "description": "数据挖掘的基本方法和技术，包括分类、聚类、关联规则等",
                        "resources": [
                            {"name": "数据挖掘技术", "type": "文档", "url": "https://example.com/data-mining"},
                            {"name": "数据挖掘案例分析", "type": "文档", "url": "https://example.com/data-mining-cases"}
                        ]
                    }
                ]
            },
            {
                "name": "数据可视化",
                "description": "包括可视化技术、交互式仪表板等内容",
                "order": 4,
                "topics": [
                    {
                        "name": "可视化工具",
                        "description": "常用数据可视化工具和库，如Matplotlib、Seaborn、Plotly等",
                        "resources": [
                            {"name": "Python可视化库比较", "type": "文档", "url": "https://example.com/visualization-libs"},
                            {"name": "Matplotlib基础教程", "type": "视频", "url": "https://example.com/matplotlib"}
                        ]
                    },
                    {
                        "name": "图表类型",
                        "description": "不同类型数据适合的图表类型和设计原则",
                        "resources": [
                            {"name": "图表类型选择指南", "type": "文档", "url": "https://example.com/chart-types"},
                            {"name": "数据可视化最佳实践", "type": "文档", "url": "https://example.com/visualization-best-practices"}
                        ]
                    },
                    {
                        "name": "交互式设计",
                        "description": "交互式数据可视化的设计原则和实现方法",
                        "resources": [
                            {"name": "交互式可视化设计", "type": "文档", "url": "https://example.com/interactive-viz"},
                            {"name": "D3.js入门教程", "type": "视频", "url": "https://example.com/d3js"}
                        ]
                    },
                    {
                        "name": "实时监控",
                        "description": "实时数据监控和可视化的实现方法",
                        "resources": [
                            {"name": "实时数据监控系统", "type": "文档", "url": "https://example.com/real-time-monitoring"},
                            {"name": "Grafana使用指南", "type": "文档", "url": "https://example.com/grafana"}
                        ]
                    }
                ]
            },
            {
                "name": "数据治理与安全",
                "description": "包括数据质量、数据安全、隐私保护等内容",
                "order": 5,
                "topics": [
                    {
                        "name": "数据质量管理",
                        "description": "数据质量管理的框架、方法和工具",
                        "resources": [
                            {"name": "数据质量管理框架", "type": "文档", "url": "https://example.com/data-quality-management"},
                            {"name": "数据质量监控工具", "type": "文档", "url": "https://example.com/data-quality-tools"}
                        ]
                    },
                    {
                        "name": "访问控制",
                        "description": "数据访问控制的方法和技术，包括身份认证和授权",
                        "resources": [
                            {"name": "数据访问控制模型", "type": "文档", "url": "https://example.com/access-control"},
                            {"name": "RBAC与ABAC比较", "type": "文档", "url": "https://example.com/rbac-vs-abac"}
                        ]
                    },
                    {
                        "name": "加密技术",
                        "description": "数据加密的技术和方法，包括对称加密、非对称加密等",
                        "resources": [
                            {"name": "数据加密基础", "type": "文档", "url": "https://example.com/data-encryption"},
                            {"name": "加密算法比较", "type": "文档", "url": "https://example.com/encryption-algorithms"}
                        ]
                    },
                    {
                        "name": "合规性要求",
                        "description": "数据合规性要求和标准，如GDPR、CCPA等",
                        "resources": [
                            {"name": "数据合规性指南", "type": "文档", "url": "https://example.com/data-compliance"},
                            {"name": "GDPR合规检查清单", "type": "文档", "url": "https://example.com/gdpr-checklist"}
                        ]
                    }
                ]
            }
        ]
        
    def generate_course_data(self):
        """Generate complete course data structure"""
        course_data = {
            "course": {
                "name": self.course_name,
                "description": self.course_description
            },
            "chapters": self.chapters
        }
        return course_data
        
    def save_to_json(self, file_path="data/course_data.json"):
        """Save course data to JSON file"""
        course_data = self.generate_course_data()
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(course_data, f, ensure_ascii=False, indent=2)
            
        print(f"Course data saved to {file_path}")
        return file_path
        
    def load_from_json(self, file_path="data/course_data.json"):
        """Load course data from JSON file"""
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist")
            return None
            
        with open(file_path, 'r', encoding='utf-8') as f:
            course_data = json.load(f)
            
        return course_data 