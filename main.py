import os
import argparse
from db_manager import MySQLManager
from data_generator import DataEngineeringDataGenerator
from knowledge_graph import KnowledgeGraph
from information_extraction import InformationExtractor

def setup_database():
    """Set up MySQL database and create necessary tables"""
    db_manager = MySQLManager()
    db_manager.connect()
    db_manager.create_course_tables()
    return db_manager

def generate_course_data():
    """Generate course data and save to JSON"""
    data_generator = DataEngineeringDataGenerator()
    json_file_path = data_generator.save_to_json()
    return json_file_path

def build_knowledge_graph(json_file_path):
    """Build knowledge graph from JSON data"""
    kg = KnowledgeGraph()
    kg.build_knowledge_graph_from_json(json_file_path)
    return kg

def populate_database(db_manager, json_file_path):
    """Populate MySQL database with course data"""
    with open(json_file_path, 'r', encoding='utf-8') as f:
        course_data = json.load(f)
        
    # Insert course data
    course_id = db_manager.insert_course_data(
        course_data["course"]["name"],
        course_data["course"]["description"]
    )
    
    # Insert chapter data
    for chapter in course_data["chapters"]:
        chapter_id = db_manager.insert_chapter_data(
            course_id,
            chapter["name"],
            chapter["description"],
            chapter["order"]
        )
        
        # Insert topic data
        for topic in chapter["topics"]:
            topic_id = db_manager.insert_topic_data(
                chapter_id,
                topic["name"],
                topic["description"]
            )
            
            # Insert resource data
            for resource in topic.get("resources", []):
                db_manager.insert_resource_data(
                    topic_id,
                    resource["name"],
                    resource["type"],
                    resource["url"]
                )
                
    print(f"Database populated with course data (Course ID: {course_id})")
    return course_id

def extract_information_from_text(text_file_path):
    """Extract information from text file"""
    if not os.path.exists(text_file_path):
        print(f"Text file {text_file_path} does not exist")
        return None
        
    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    extractor = InformationExtractor()
    extracted_data = extractor.process_text(text)
    json_file_path = extractor.save_extracted_data()
    
    return json_file_path

def interactive_qa(kg):
    """Interactive question answering session"""
    print("\n=== 智能数据工程课程问答系统 ===")
    print("您可以询问以下类型的问题：")
    print("1. 这门课程是什么？")
    print("2. 课程包含哪些章节？")
    print("3. 某个章节包含哪些知识点？")
    print("4. 某个知识点有哪些学习资源？")
    print("输入'退出'结束对话")
    
    while True:
        question = input("\n请输入您的问题：")
        if question == "退出":
            break
            
        answer = kg.answer_question(question)
        print("\n回答：", answer)

def main():
    parser = argparse.ArgumentParser(description="智能数据工程课程知识图谱系统")
    parser.add_argument("--setup", action="store_true", help="Set up database and create tables")
    parser.add_argument("--generate", action="store_true", help="Generate course data")
    parser.add_argument("--build-kg", action="store_true", help="Build knowledge graph")
    parser.add_argument("--populate-db", action="store_true", help="Populate database with course data")
    parser.add_argument("--extract", type=str, help="Extract information from text file")
    parser.add_argument("--qa", action="store_true", help="Start interactive question answering")
    parser.add_argument("--all", action="store_true", help="Run all steps")
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if not any(vars(args).values()):
        parser.print_help()
        return
        
    # Run all steps if --all is specified
    if args.all:
        args.setup = True
        args.generate = True
        args.build_kg = True
        args.populate_db = True
        args.qa = True
        
    json_file_path = "data/course_data.json"
    
    # Set up database
    if args.setup:
        print("\n=== 设置数据库 ===")
        db_manager = setup_database()
        
    # Generate course data
    if args.generate:
        print("\n=== 生成课程数据 ===")
        json_file_path = generate_course_data()
        
    # Build knowledge graph
    if args.build_kg:
        print("\n=== 构建知识图谱 ===")
        kg = build_knowledge_graph(json_file_path)
        
    # Populate database
    if args.populate_db:
        print("\n=== 填充数据库 ===")
        db_manager = MySQLManager()
        course_id = populate_database(db_manager, json_file_path)
        
    # Extract information from text
    if args.extract:
        print(f"\n=== 从文本文件提取信息: {args.extract} ===")
        extracted_json_path = extract_information_from_text(args.extract)
        if extracted_json_path:
            print(f"提取的信息已保存到: {extracted_json_path}")
            
    # Interactive question answering
    if args.qa:
        print("\n=== 启动问答系统 ===")
        kg = KnowledgeGraph()
        interactive_qa(kg)

if __name__ == "__main__":
    import json  # Import here to avoid circular import
    main() 