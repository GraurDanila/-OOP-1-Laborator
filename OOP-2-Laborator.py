from enum import Enum
from datetime import date
import pickle

class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.study_field = study_field

class FileManager:
    def save_data(self, faculties):
        with open("catalintop.txt", "w") as file:
            for faculty in faculties:
                file.write(f"{faculty.name},{faculty.abbreviation},{faculty.study_field}\n")
                for student in faculty.students:
                    file.write(f"{student.first_name},{student.last_name},{student.email},{student.enrollment_date},{student.date_of_birth}\n")

    def load_data(self):
        try:
            with open("catalintop.txt", "r") as file:
                faculties = []
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(",")
                    faculty = Faculty(data[0], data[1], data[2])
                    faculties.append(faculty)
                return faculties
        except FileNotFoundError:
            print("File 'catalintop.txt' not found. Creating empty list of faculties.")
            return []

class StudentManagementSystem:
    def __init__(self):
        self.faculties = []
        self.file_manager = FileManager()
        self.log_file = "skaaa.txt"

    def create_student(self, faculty, first_name, last_name, email, day, month, year):
        enrollment_date = date.today()
        date_of_birth = date(year, month, day)
        student = Student(first_name, last_name, email, enrollment_date, date_of_birth)
        self.assign_student_to_faculty(student, faculty)
        self.log_operation(f"Created student: {first_name} {last_name}, Email: {email}, Faculty: {faculty.name}")
        return student

    def assign_student_to_faculty(self, student, faculty):
        faculty.students.append(student)

    def graduate_student(self, student, faculty):
        if student in faculty.students:
            faculty.students.remove(student)
            self.log_operation(f"Graduated student: {student.first_name} {student.last_name}, Faculty: {faculty.name}")
        else:
            self.log_operation(f"Failed to graduate student: {student.first_name} {student.last_name}, Faculty: {faculty.name}")

    def display_current_students(self, faculty):
        print(f"Faculty: {faculty.name}")
        for student in faculty.students:
            print(f"{student.first_name} {student.last_name}")

    def display_alumni(self, faculty):
        print(f"Faculty: {faculty.name} - Alumni:")
        for student in faculty.students:
            print(f"{student.first_name} {student.last_name}")

    def check_student_belongs_to_faculty(self, student, faculty):
        return student in faculty.students

    def create_faculty(self, name, abbreviation, study_field):
        faculty = Faculty(name, abbreviation, study_field)
        self.faculties.append(faculty)
        self.log_operation(f"Created faculty: {name}, Abbreviation: {abbreviation}, Field: {study_field}")
        return faculty

    def search_faculty_by_student_id(self, student_id):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == student_id:
                    return faculty
        return None

    def display_all_faculties(self):
        print("All faculties:")
        for faculty in self.faculties:
            print(f"Faculty: {faculty.name}, Abbreviation: {faculty.abbreviation}, Field: {faculty.study_field}")

    def display_faculties_by_field(self, study_field):
        print(f"Faculties in field {study_field}:")
        for faculty in self.faculties:
            if faculty.study_field == study_field:
                print(f"Faculty: {faculty.name}, Abbreviation: {faculty.abbreviation}")

    def save_system_state(self):
        self.file_manager.save_data(self.faculties)
        self.log_operation("Saved system state.")

    def load_system_state(self):
        self.faculties = self.file_manager.load_data()
        self.log_operation("Loaded system state.")

    def log_operation(self, message):
        with open(self.log_file, "a") as file:
            file.write(f"{date.today()} - {message}\n")

    def register_students_from_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
            for line in lines:
                data = line.strip().split(",")
                self.create_student(*data)


class StudyField(Enum):
    Mechanical_Engineering = 1
    Software_Engineering = 2
    Food_Technology = 3
    Urbanism_Architecture = 4
    Veterinary_Medicine = 5


class Student:
    def __init__(self, firstname, lastname, email, enrollment_date, date_of_birth):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.enrollment_date = enrollment_date
        self.date_of_birth = date_of_birth
        self.faculty = None
        self.graduated = False

    def assign_to_faculty(self, faculty):
        self.faculty = faculty

    def graduate(self):
        self.graduated = True

class Faculty:
    def __init__(self, name, abbreviation, study_field):
        self.name = name
        self.abbreviation = abbreviation
        self.students = []
        self.study_field = study_field

    def add_student(self, student):
        self.students.append(student)

    def get_enrolled_students(self):
        return [student for student in self.students if not student.graduated]

    def get_graduates(self):
        return [student for student in self.students if student.graduated]

class University:
    def __init__(self):
        self.faculties = []

    def create_faculty(self, name, abbreviation, study_field):
        new_faculty = Faculty(name, abbreviation, study_field)
        self.faculties.append(new_faculty)

    def assign_student_to_faculty(self, student, faculty_name):
        for faculty in self.faculties:
            if faculty.name == faculty_name:
                student.assign_to_faculty(faculty)
                faculty.add_student(student)
                break

    def graduate_student(self, student):
        student.graduate()

    def display_enrolled_students(self, faculty_name):
        for faculty in self.faculties:
            if faculty.name == faculty_name:
                enrolled_students = faculty.get_enrolled_students()
                print("Enrolled students in", faculty_name, ":")
                for student in enrolled_students:
                    print(student.firstname, student.lastname)
                break

    def display_graduates(self, faculty_name):
        for faculty in self.faculties:
            if faculty.name == faculty_name:
                graduates = faculty.get_graduates()
                print("Graduates from", faculty_name, ":")
                for student in graduates:
                    print(student.firstname, student.lastname)
                break

    def tell_student_belonging(self, student_email, faculty_name):
        for faculty in self.faculties:
            if faculty.name == faculty_name:
                for student in faculty.students:
                    if student.email == student_email:
                        print(student.firstname, student.lastname, "belongs to", faculty_name)
                        return
                print("Student with email", student_email, "not found in", faculty_name)
                return
        print("Faculty", faculty_name, "not found.")

    def get_faculty_by_student_email(self, student_email):
        for faculty in self.faculties:
            for student in faculty.students:
                if student.email == student_email:
                    return faculty.name
        return None

    def display_all_faculties(self):
        print("University faculties:")
        for faculty in self.faculties:
            print(faculty.name)

    def display_faculties_by_field(self, study_field):
        print("Faculties belonging to", study_field, ":")
        for faculty in self.faculties:
            if faculty.study_field == study_field:
                print(faculty.name)


def main():
    system = StudentManagementSystem()

    while True:
        print("\nOptions:")
        print("1. Faculty Operations")
        print("2. General Operations")
        print("3. Exit")
        option = input("Select an option: ")

        if option == "1":
            print("\nFaculty Operations:")
            print("1. Create and assign a student to a faculty")
            print("2. Graduate a student from a faculty")
            print("3. Display current enrolled students")
            print("4. Display graduates")
            print("5. Tell if a student belongs to this faculty")
            faculty_option = input("Select an option: ")

            if faculty_option == "1":
                firstname = input("Enter student's first name: ")
                lastname = input("Enter student's last name: ")
                email = input("Enter student's email: ")
                enrollment_date = input("Enter student's enrollment date (YYYY-MM-DD): ")
                date_of_birth = input("Enter student's date of birth (YYYY-MM-DD): ")
                faculty_name = input("Enter faculty's name: ")
                for faculty in system.faculties:
                    if faculty.name == faculty_name:
                        student = Student(firstname, lastname, email, enrollment_date, date_of_birth)
                        faculty.add_student(student)
                        student.assign_to_faculty(faculty)
                        print(f"{firstname} {lastname} assigned to {faculty_name}")
                        break    
                else:
                    print("Faculty not found.")

            elif faculty_option == "2":
                email = input("Enter student's email: ")
                faculty_name = system.get_faculty_by_student_email(email)
                if faculty_name:
                    system.display_enrolled_students(faculty_name)
                    firstname = input("Enter student's first name: ")
                    lastname = input("Enter student's last name: ")
                    for faculty in system.faculties:
                        if faculty.name == faculty_name:
                            for student in faculty.students:
                                if student.firstname == firstname and student.lastname == lastname and student.email == email:
                                    student.graduate()
                                    print(student.firstname, student.lastname, "graduated from", faculty_name)
                                    break
                            else:
                                print("Student not found in", faculty_name)
                                break
                    else:
                        print("Student with email", email, "not found.")

            elif faculty_option == "3":
                faculty_name = input("Enter faculty's name: ")
                system.display_enrolled_students(faculty_name)

            elif faculty_option == "4":
                faculty_name = input("Enter faculty's name: ")
                system.display_graduates(faculty_name)

            elif faculty_option == "5":
                email = input("Enter student's email: ")
                faculty_name = input("Enter faculty's name: ")
                system.tell_student_belonging(email, faculty_name)

            else:
                print("Invalid option.")

        elif option == "2":
            print("\nGeneral Operations:")
            print("1. Create a new faculty")
            print("2. Search what faculty a student belongs to by email")
            print("3. Display University faculties")
            print("4. Display all faculties belonging to a field")
            general_option = input("Select an option: ")

            if general_option == "1":
                name = input("Enter faculty's name: ")
                abbreviation = input("Enter faculty's abbreviation: ")
                study_field = input("Enter faculty's study field: ")
                system.create_faculty(name, abbreviation, study_field)
                print("Faculty", name, "created.")

            elif general_option == "2":
                email = input("Enter student's email: ")
                faculty_name = system.get_faculty_by_student_id(email)
                if faculty_name:
                    print("Student with email", email, "belongs to", faculty_name)
                else:
                    print("Student with email", email, "not found.")

            elif general_option == "3":
                system.display_all_faculties()

            elif general_option == "4":
                field = input("Enter field: ")
                system.display_faculties_by_field(field)

            else:
                print("Invalid option.")

        elif option == "3":
            system.save_system_state()
            print("Exiting...")
            break

        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()