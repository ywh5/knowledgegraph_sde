import mysql.connector
from mysql.connector import Error
import pandas as pd

class MySQLManager:
    def __init__(self, host="localhost", user="root", password="1234", database="mysql80"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Establish connection to MySQL database"""
        try:
            # First connect without specifying database
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            if self.connection.is_connected():
                cursor = self.connection.cursor()
                
                # Create database if it doesn't exist
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
                cursor.close()
                
                # Close the initial connection
                self.connection.close()
                
                # Reconnect with the database specified
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
                
                if self.connection.is_connected():
                    print(f"Successfully connected to MySQL database: {self.database}")
                    return True
                    
        except Error as e:
            print(f"Error connecting to MySQL database: {e}")
            return False
            
    def disconnect(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")
            
    def create_course_tables(self):
        """Create necessary tables for the course data"""
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                print("Failed to establish database connection")
                return False
            
        try:
            cursor = self.connection.cursor()
            
            # Create courses table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                course_id INT AUTO_INCREMENT PRIMARY KEY,
                course_name VARCHAR(100) NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            
            # Create chapters table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS chapters (
                chapter_id INT AUTO_INCREMENT PRIMARY KEY,
                course_id INT,
                chapter_name VARCHAR(100) NOT NULL,
                description TEXT,
                chapter_order INT,
                FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
            )
            """)
            
            # Create topics table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS topics (
                topic_id INT AUTO_INCREMENT PRIMARY KEY,
                chapter_id INT,
                topic_name VARCHAR(100) NOT NULL,
                description TEXT,
                FOREIGN KEY (chapter_id) REFERENCES chapters(chapter_id) ON DELETE CASCADE
            )
            """)
            
            # Create resources table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                resource_id INT AUTO_INCREMENT PRIMARY KEY,
                topic_id INT,
                resource_name VARCHAR(100) NOT NULL,
                resource_type VARCHAR(50),
                resource_url TEXT,
                FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
            )
            """)
            
            self.connection.commit()
            cursor.close()
            print("Course tables created successfully")
            return True
            
        except Error as e:
            print(f"Error creating course tables: {e}")
            return False
        
    def insert_course_data(self, course_name, description):
        """Insert a new course into the database"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO courses (course_name, description) VALUES (%s, %s)",
            (course_name, description)
        )
        self.connection.commit()
        course_id = cursor.lastrowid
        cursor.close()
        return course_id
        
    def insert_chapter_data(self, course_id, chapter_name, description, chapter_order):
        """Insert a new chapter into the database"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO chapters (course_id, chapter_name, description, chapter_order) VALUES (%s, %s, %s, %s)",
            (course_id, chapter_name, description, chapter_order)
        )
        self.connection.commit()
        chapter_id = cursor.lastrowid
        cursor.close()
        return chapter_id
        
    def insert_topic_data(self, chapter_id, topic_name, description):
        """Insert a new topic into the database"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO topics (chapter_id, topic_name, description) VALUES (%s, %s, %s)",
            (chapter_id, topic_name, description)
        )
        self.connection.commit()
        topic_id = cursor.lastrowid
        cursor.close()
        return topic_id
        
    def insert_resource_data(self, topic_id, resource_name, resource_type, resource_url):
        """Insert a new resource into the database"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO resources (topic_id, resource_name, resource_type, resource_url) VALUES (%s, %s, %s, %s)",
            (topic_id, resource_name, resource_type, resource_url)
        )
        self.connection.commit()
        resource_id = cursor.lastrowid
        cursor.close()
        return resource_id
        
    def get_course_data(self, course_id=None):
        """Retrieve course data from the database"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        
        if course_id:
            cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
        else:
            cursor.execute("SELECT * FROM courses")
            
        courses = cursor.fetchall()
        cursor.close()
        return courses
        
    def get_chapters_by_course(self, course_id):
        """Retrieve chapters for a specific course"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM chapters WHERE course_id = %s ORDER BY chapter_order",
            (course_id,)
        )
        chapters = cursor.fetchall()
        cursor.close()
        return chapters
        
    def get_topics_by_chapter(self, chapter_id):
        """Retrieve topics for a specific chapter"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM topics WHERE chapter_id = %s",
            (chapter_id,)
        )
        topics = cursor.fetchall()
        cursor.close()
        return topics
        
    def get_resources_by_topic(self, topic_id):
        """Retrieve resources for a specific topic"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM resources WHERE topic_id = %s",
            (topic_id,)
        )
        resources = cursor.fetchall()
        cursor.close()
        return resources
        
    def export_to_dataframe(self, query):
        """Export query results to a pandas DataFrame"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
            
        return pd.read_sql_query(query, self.connection) 