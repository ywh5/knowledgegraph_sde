import re
import json
import os
from collections import defaultdict

class InformationExtractor:
    def __init__(self):
        self.entities = defaultdict(list)
        self.relationships = []
        
    def extract_entities(self, text, entity_type):
        """Extract entities of a specific type from text"""
        # This is a simple implementation that can be enhanced with NLP libraries
        # For now, we'll use basic pattern matching
        
        if entity_type == "Course":
            # Extract course name and description
            course_pattern = r"课程名称[:：]\s*([^\n]+)"
            desc_pattern = r"课程描述[:：]\s*([^\n]+)"
            
            course_match = re.search(course_pattern, text)
            desc_match = re.search(desc_pattern, text)
            
            if course_match:
                self.entities["Course"].append({
                    "name": course_match.group(1).strip(),
                    "description": desc_match.group(1).strip() if desc_match else ""
                })
                
        elif entity_type == "Chapter":
            # Extract chapter information
            chapter_pattern = r"第(\d+)章\s*([^\n]+)[:：]\s*([^\n]+)"
            
            for match in re.finditer(chapter_pattern, text):
                chapter_num = int(match.group(1))
                chapter_name = match.group(2).strip()
                chapter_desc = match.group(3).strip()
                
                self.entities["Chapter"].append({
                    "name": chapter_name,
                    "description": chapter_desc,
                    "order": chapter_num
                })
                
        elif entity_type == "Topic":
            # Extract topic information
            topic_pattern = r"(\d+\.\d+)\s*([^\n]+)[:：]\s*([^\n]+)"
            
            for match in re.finditer(topic_pattern, text):
                topic_num = match.group(1)
                topic_name = match.group(2).strip()
                topic_desc = match.group(3).strip()
                
                self.entities["Topic"].append({
                    "name": topic_name,
                    "description": topic_desc,
                    "number": topic_num
                })
                
        elif entity_type == "Resource":
            # Extract resource information
            resource_pattern = r"资源[:：]\s*([^\n]+)\s*类型[:：]\s*([^\n]+)\s*链接[:：]\s*([^\n]+)"
            
            for match in re.finditer(resource_pattern, text):
                resource_name = match.group(1).strip()
                resource_type = match.group(2).strip()
                resource_url = match.group(3).strip()
                
                self.entities["Resource"].append({
                    "name": resource_name,
                    "type": resource_type,
                    "url": resource_url
                })
                
    def extract_relationships(self, text):
        """Extract relationships between entities from text"""
        # Extract course-chapter relationships
        course_chapter_pattern = r"课程\s*([^\n]+)\s*包含\s*章节\s*([^\n]+)"
        
        for match in re.finditer(course_chapter_pattern, text):
            course_name = match.group(1).strip()
            chapter_name = match.group(2).strip()
            
            self.relationships.append({
                "source": course_name,
                "target": chapter_name,
                "type": "CONTAINS"
            })
            
        # Extract chapter-topic relationships
        chapter_topic_pattern = r"章节\s*([^\n]+)\s*包含\s*知识点\s*([^\n]+)"
        
        for match in re.finditer(chapter_topic_pattern, text):
            chapter_name = match.group(1).strip()
            topic_name = match.group(2).strip()
            
            self.relationships.append({
                "source": chapter_name,
                "target": topic_name,
                "type": "CONTAINS"
            })
            
        # Extract topic-resource relationships
        topic_resource_pattern = r"知识点\s*([^\n]+)\s*有\s*资源\s*([^\n]+)"
        
        for match in re.finditer(topic_resource_pattern, text):
            topic_name = match.group(1).strip()
            resource_name = match.group(2).strip()
            
            self.relationships.append({
                "source": topic_name,
                "target": resource_name,
                "type": "HAS_RESOURCE"
            })
            
    def process_text(self, text):
        """Process text to extract entities and relationships"""
        # Extract all entity types
        self.extract_entities(text, "Course")
        self.extract_entities(text, "Chapter")
        self.extract_entities(text, "Topic")
        self.extract_entities(text, "Resource")
        
        # Extract relationships
        self.extract_relationships(text)
        
        return {
            "entities": self.entities,
            "relationships": self.relationships
        }
        
    def save_extracted_data(self, output_file="data/extracted_data.json"):
        """Save extracted data to JSON file"""
        extracted_data = {
            "entities": self.entities,
            "relationships": self.relationships
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_data, f, ensure_ascii=False, indent=2)
            
        print(f"Extracted data saved to {output_file}")
        return output_file
        
    def load_extracted_data(self, input_file="data/extracted_data.json"):
        """Load extracted data from JSON file"""
        if not os.path.exists(input_file):
            print(f"File {input_file} does not exist")
            return None
            
        with open(input_file, 'r', encoding='utf-8') as f:
            extracted_data = json.load(f)
            
        self.entities = defaultdict(list, extracted_data["entities"])
        self.relationships = extracted_data["relationships"]
        
        return extracted_data
        
    def convert_to_knowledge_graph_format(self):
        """Convert extracted data to knowledge graph format"""
        knowledge_graph_data = {
            "course": {
                "name": self.entities["Course"][0]["name"] if self.entities["Course"] else "",
                "description": self.entities["Course"][0]["description"] if self.entities["Course"] else ""
            },
            "chapters": []
        }
        
        # Process chapters
        for chapter in self.entities["Chapter"]:
            chapter_data = {
                "name": chapter["name"],
                "description": chapter["description"],
                "order": chapter["order"],
                "topics": []
            }
            
            # Find topics for this chapter
            chapter_topics = [t for t in self.entities["Topic"] if t.get("chapter") == chapter["name"]]
            
            for topic in chapter_topics:
                topic_data = {
                    "name": topic["name"],
                    "description": topic["description"],
                    "resources": []
                }
                
                # Find resources for this topic
                topic_resources = [r for r in self.entities["Resource"] if r.get("topic") == topic["name"]]
                
                for resource in topic_resources:
                    resource_data = {
                        "name": resource["name"],
                        "type": resource["type"],
                        "url": resource["url"]
                    }
                    topic_data["resources"].append(resource_data)
                    
                chapter_data["topics"].append(topic_data)
                
            knowledge_graph_data["chapters"].append(chapter_data)
            
        return knowledge_graph_data 