from py2neo import Graph, Node, Relationship
import json
import os

class KnowledgeGraph:
    def __init__(self, uri="http://localhost:7474", username="neo4j", password="1"):
        """Initialize connection to Neo4j database"""
        self.g = Graph(uri, auth=(username, password))
        print(f"Connected to Neo4j database at {uri}")
        
    def clear_database(self):
        """Clear all nodes and relationships in the database"""
        self.g.delete_all()
        print("Neo4j database cleared")
        
    def create_course_node(self, course_name, course_description):
        """Create a course node in the knowledge graph"""
        course = Node("Course", name=course_name, description=course_description)
        self.g.create(course)
        print(f"Created course node: {course_name}")
        return course
        
    def create_chapter_node(self, chapter_name, chapter_description, chapter_order):
        """Create a chapter node in the knowledge graph"""
        chapter = Node("Chapter", name=chapter_name, description=chapter_description, order=chapter_order)
        self.g.create(chapter)
        print(f"Created chapter node: {chapter_name}")
        return chapter
        
    def create_topic_node(self, topic_name, topic_description):
        """Create a topic node in the knowledge graph"""
        topic = Node("Topic", name=topic_name, description=topic_description)
        self.g.create(topic)
        print(f"Created topic node: {topic_name}")
        return topic
        
    def create_resource_node(self, resource_name, resource_type, resource_url):
        """Create a resource node in the knowledge graph"""
        resource = Node("Resource", name=resource_name, type=resource_type, url=resource_url)
        self.g.create(resource)
        print(f"Created resource node: {resource_name}")
        return resource
        
    def create_relationship(self, start_node, relationship_type, end_node):
        """Create a relationship between two nodes"""
        rel = Relationship(start_node, relationship_type, end_node)
        self.g.create(rel)
        print(f"Created relationship: {start_node['name']} -{relationship_type}-> {end_node['name']}")
        return rel
        
    def build_knowledge_graph_from_json(self, json_file_path):
        """Build knowledge graph from JSON data"""
        if not os.path.exists(json_file_path):
            print(f"File {json_file_path} does not exist")
            return False
            
        with open(json_file_path, 'r', encoding='utf-8') as f:
            course_data = json.load(f)
            
        # Clear existing database
        self.clear_database()
        
        # Create course node
        course = self.create_course_node(
            course_data["course"]["name"],
            course_data["course"]["description"]
        )
        
        # Create chapter nodes and relationships
        for chapter_data in course_data["chapters"]:
            chapter = self.create_chapter_node(
                chapter_data["name"],
                chapter_data["description"],
                chapter_data["order"]
            )
            
            # Create relationship between course and chapter
            self.create_relationship(course, "CONTAINS", chapter)
            
            # Create topic nodes and relationships
            for topic_data in chapter_data["topics"]:
                topic = self.create_topic_node(
                    topic_data["name"],
                    topic_data["description"]
                )
                
                # Create relationship between chapter and topic
                self.create_relationship(chapter, "CONTAINS", topic)
                
                # Create resource nodes and relationships
                for resource_data in topic_data.get("resources", []):
                    resource = self.create_resource_node(
                        resource_data["name"],
                        resource_data["type"],
                        resource_data["url"]
                    )
                    
                    # Create relationship between topic and resource
                    self.create_relationship(topic, "HAS_RESOURCE", resource)
                    
        print("Knowledge graph built successfully from JSON data")
        return True
        
    def query_course_info(self):
        """Query basic course information"""
        query = """
        MATCH (c:Course)
        RETURN c.name AS course_name, c.description AS course_description
        """
        result = self.g.run(query).data()
        return result[0] if result else None
        
    def query_chapters(self):
        """Query all chapters with their descriptions"""
        query = """
        MATCH (c:Chapter)
        RETURN c.name AS chapter_name, c.description AS chapter_description, c.order AS chapter_order
        ORDER BY c.order
        """
        return self.g.run(query).data()
        
    def query_topics_by_chapter(self, chapter_name):
        """Query all topics for a specific chapter"""
        query = """
        MATCH (c:Chapter {name: $chapter_name})-[:CONTAINS]->(t:Topic)
        RETURN t.name AS topic_name, t.description AS topic_description
        """
        return self.g.run(query, chapter_name=chapter_name).data()
        
    def query_resources_by_topic(self, topic_name):
        """Query all resources for a specific topic"""
        query = """
        MATCH (t:Topic {name: $topic_name})-[:HAS_RESOURCE]->(r:Resource)
        RETURN r.name AS resource_name, r.type AS resource_type, r.url AS resource_url
        """
        return self.g.run(query, topic_name=topic_name).data()
        
    def answer_question(self, question):
        """Simple question answering based on the knowledge graph"""
        question = question.lower()
        
        # Course information
        if "课程" in question or "智能数据工程" in question:
            course_info = self.query_course_info()
            if course_info:
                return f"智能数据工程是一门{course_info['course_description']}"
                
        # Chapter information
        if "章节" in question or "内容" in question:
            chapters = self.query_chapters()
            if chapters:
                response = "课程包含以下章节：\n"
                for chapter in chapters:
                    response += f"- {chapter['chapter_name']}: {chapter['chapter_description']}\n"
                return response
                
        # Topic information for a specific chapter
        for chapter in self.query_chapters():
            if chapter['chapter_name'] in question:
                topics = self.query_topics_by_chapter(chapter['chapter_name'])
                if topics:
                    response = f"{chapter['chapter_name']}章节包含以下知识点：\n"
                    for topic in topics:
                        response += f"- {topic['topic_name']}: {topic['topic_description']}\n"
                    return response
                    
        # Resource information for a specific topic
        for chapter in self.query_chapters():
            for topic in self.query_topics_by_chapter(chapter['chapter_name']):
                if topic['topic_name'] in question:
                    resources = self.query_resources_by_topic(topic['topic_name'])
                    if resources:
                        response = f"{topic['topic_name']}的学习资源包括：\n"
                        for resource in resources:
                            response += f"- {resource['resource_name']} ({resource['resource_type']}): {resource['resource_url']}\n"
                        return response
                        
        return "抱歉，我无法理解您的问题。请尝试询问关于课程内容、章节或具体知识点的问题。" 