from py2neo import Graph, Node, Relationship
import re

class IntelligentDataEngineeringKG:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "1"))
        
    def clear_database(self):
        self.g.delete_all()
        
    def create_knowledge_graph(self):
        # 创建课程节点
        course = Node("Course", name="智能数据工程", description="一门关于数据工程智能化的课程")
        self.g.create(course)
        
        # 创建主要章节节点
        chapters = [
            Node("Chapter", name="数据采集与预处理", description="包括数据源识别、数据清洗、数据转换等内容"),
            Node("Chapter", name="数据存储与管理", description="包括数据库设计、数据仓库、数据湖等内容"),
            Node("Chapter", name="数据处理与分析", description="包括批处理、流处理、数据分析方法等内容"),
            Node("Chapter", name="数据可视化", description="包括可视化技术、交互式仪表板等内容"),
            Node("Chapter", name="数据治理与安全", description="包括数据质量、数据安全、隐私保护等内容")
        ]
        
        # 创建章节与课程的关系
        for chapter in chapters:
            self.g.create(chapter)
            self.g.create(Relationship(course, "包含", chapter))
            
        # 为每个章节添加具体知识点
        topics = {
            "数据采集与预处理": [
                "数据源类型",
                "数据清洗技术",
                "ETL流程",
                "数据质量评估"
            ],
            "数据存储与管理": [
                "关系型数据库",
                "NoSQL数据库",
                "数据仓库架构",
                "数据湖技术"
            ],
            "数据处理与分析": [
                "批处理框架",
                "流处理技术",
                "机器学习算法",
                "数据挖掘方法"
            ],
            "数据可视化": [
                "可视化工具",
                "图表类型",
                "交互式设计",
                "实时监控"
            ],
            "数据治理与安全": [
                "数据质量管理",
                "访问控制",
                "加密技术",
                "合规性要求"
            ]
        }
        
        # 创建知识点节点并建立关系
        for chapter_name, chapter_topics in topics.items():
            chapter_node = self.g.nodes.match("Chapter", name=chapter_name).first()
            for topic in chapter_topics:
                topic_node = Node("Topic", name=topic)
                self.g.create(topic_node)
                self.g.create(Relationship(chapter_node, "包含", topic_node))
                
    def answer_question(self, question):
        # 简单的关键词匹配问答系统
        question = question.lower()
        
        if "课程" in question or "智能数据工程" in question:
            course = self.g.nodes.match("Course").first()
            return f"智能数据工程是{course['description']}"
            
        if "章节" in question or "内容" in question:
            chapters = self.g.nodes.match("Chapter").all()
            response = "课程包含以下章节：\n"
            for chapter in chapters:
                response += f"- {chapter['name']}: {chapter['description']}\n"
            return response
            
        # 查找特定章节的知识点
        for chapter in self.g.nodes.match("Chapter").all():
            if chapter['name'] in question:
                topics = self.g.nodes.match("Topic").where(f"MATCH (c:Chapter)-[:包含]->(t:Topic) WHERE c.name = '{chapter['name']}' RETURN t")
                response = f"{chapter['name']}章节包含以下知识点：\n"
                for topic in topics:
                    response += f"- {topic['name']}\n"
                return response
                
        return "抱歉，我无法理解您的问题。请尝试询问关于课程内容、章节或具体知识点的问题。"

def main():
    kg = IntelligentDataEngineeringKG()
    kg.clear_database()
    kg.create_knowledge_graph()
    
    print("知识图谱已创建完成！")
    print("您可以询问以下类型的问题：")
    print("1. 这门课程是什么？")
    print("2. 课程包含哪些章节？")
    print("3. 某个章节包含哪些知识点？")
    print("输入'退出'结束对话")
    
    while True:
        question = input("\n请输入您的问题：")
        if question == "退出":
            break
        answer = kg.answer_question(question)
        print("\n回答：", answer)

if __name__ == "__main__":
    main() 