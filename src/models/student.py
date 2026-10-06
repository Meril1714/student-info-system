class Student:
    def __init__(self, student_id: str, name: str, age: int, grade: str, email: str):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.grade = grade
        self.email = email

    def to_dict(self) -> dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "email": self.email
        }

    @staticmethod
    def from_dict(data: dict):
        return Student(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            grade=data["grade"],
            email=data["email"]
        )

    def __str__(self) -> str:
        return f"ID: {self.student_id} | Name: {self.name} | Age: {self.age} | Grade: {self.grade} | Email: {self.email}"