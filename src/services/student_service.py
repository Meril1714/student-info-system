import json
import os
from src.models.student import Student
from src.utils.logger import logger

class StudentService:
    def __init__(self, config_path="config/config.json"):
        self.config_path = config_path
        self.data_file = self._load_config()
        self.students = []
        self.load_data()

    def _load_config(self) -> str:
        try:
            with open(self.config_path, "r") as f:
                config = json.load(f)
                return config.get("data_file_path", "data/students.json")
        except Exception as e:
            logger.error(f"Error loading config file: {e}")
            return "data/students.json"

    def load_data(self):
        if not os.path.exists(self.data_file):
            self.students = []
            self.save_data()
            return

        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                self.students = [Student.from_dict(item) for item in data]
                logger.info("Student data successfully loaded.")
        except json.JSONDecodeError:
            logger.error("Corrupted JSON data file. Initializing empty list.")
            self.students = []
        except Exception as e:
            logger.error(f"Unexpected error loading data: {e}")
            self.students = []

    def save_data(self):
        try:
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            with open(self.data_file, "w") as f:
                json.dump([s.to_dict() for s in self.students], f, indent=4)
            logger.info("Student data successfully saved.")
        except Exception as e:
            logger.error(f"Failed to save student data: {e}")

    def add_student(self, student_id: str, name: str, age: int, grade: str, email: str) -> bool:
        if self.get_student_by_id(student_id):
            logger.warning(f"Add failed: Student ID {student_id} already exists.")
            return False
        
        new_student = Student(student_id, name, age, grade, email)
        self.students.append(new_student)
        self.save_data()
        logger.info(f"Student {student_id} added successfully.")
        return True

    def get_all_students(self) -> list:
        return self.students

    def get_student_by_id(self, student_id: str):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def update_student(self, student_id: str, name=None, age=None, grade=None, email=None) -> bool:
        student = self.get_student_by_id(student_id)
        if not student:
            logger.warning(f"Update failed: Student ID {student_id} not found.")
            return False

        if name: student.name = name
        if age: student.age = age
        if grade: student.grade = grade
        if email: student.email = email

        self.save_data()
        logger.info(f"Student {student_id} updated successfully.")
        return True

    def delete_student(self, student_id: str) -> bool:
        student = self.get_student_by_id(student_id)
        if not student:
            logger.warning(f"Delete failed: Student ID {student_id} not found.")
            return False

        self.students.remove(student)
        self.save_data()
        logger.info(f"Student {student_id} deleted successfully.")
        return True

    def search_students(self, keyword: str) -> list:
        keyword = keyword.lower()
        return [
            s for s in self.students 
            if keyword in s.name.lower() or keyword in s.student_id.lower() or keyword in s.email.lower()
        ]