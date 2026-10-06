import sys
from src.services.student_service import StudentService

def display_menu():
    print("\n" + "="*40)
    print("   STUDENT INFORMATION SYSTEM (SIS)   ")
    print("="*40)
    print("1. Add New Student")
    print("2. View All Students")
    print("3. Search Student by ID or Name")
    print("4. Update Student Information")
    print("5. Delete Student")
    print("6. Exit")
    print("="*40)

def main():
    service = StudentService()

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == '1':
            print("\n--- Add New Student ---")
            sid = input("Enter Student ID: ").strip()
            name = input("Enter Full Name: ").strip()
            
            try:
                age = int(input("Enter Age: ").strip())
            except ValueError:
                print("Error: Age must be an integer.")
                continue

            grade = input("Enter Grade/Class: ").strip()
            email = input("Enter Email Address: ").strip()

            if service.add_student(sid, name, age, grade, email):
                print("--> Student added successfully!")
            else:
                print("--> Error: Student ID already exists.")

        elif choice == '2':
            print("\n--- All Student Records ---")
            students = service.get_all_students()
            if not students:
                print("No student records found.")
            else:
                for s in students:
                    print(s)

        elif choice == '3':
            print("\n--- Search Students ---")
            query = input("Enter Student ID, Name, or Email: ").strip()
            results = service.search_students(query)
            if results:
                for s in results:
                    print(s)
            else:
                print("No matching students found.")

        elif choice == '4':
            print("\n--- Update Student Information ---")
            sid = input("Enter Student ID to update: ").strip()
            student = service.get_student_by_id(sid)
            
            if not student:
                print("--> Student not found.")
                continue

            print("Leave blank to keep current value.")
            name = input(f"New Name [{student.name}]: ").strip() or None
            
            age_input = input(f"New Age [{student.age}]: ").strip()
            age = int(age_input) if age_input.isdigit() else None
            
            grade = input(f"New Grade [{student.grade}]: ").strip() or None
            email = input(f"New Email [{student.email}]: ").strip() or None

            if service.update_student(sid, name, age, grade, email):
                print("--> Student updated successfully!")

        elif choice == '5':
            print("\n--- Delete Student ---")
            sid = input("Enter Student ID to delete: ").strip()
            confirm = input(f"Are you sure you want to delete {sid}? (y/n): ").strip().lower()
            if confirm == 'y':
                if service.delete_student(sid):
                    print("--> Student deleted successfully.")
                else:
                    print("--> Student ID not found.")

        elif choice == '6':
            print("\nExiting system. Goodbye!")
            sys.exit(0)

        else:
            print("Invalid choice! Please select a valid option (1-6).")

if __name__ == "__main__":
    main()