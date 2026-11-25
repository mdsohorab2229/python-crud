from model.student import Students
from model.subject import Subjects
from repository.course_repository import SubjectRepository
from repository.student_repository import StudentRepository
from utils.schema import StudentCreate, StudentResponse , StudentUpdate


class StudentService:
    def __init__(self):
        self.repository = StudentRepository()
        self.subject_repository = SubjectRepository()

    def get_all_student(self):
        students = self.repository.get_all_student()
        student_list = []
        for student in students:
            subject_score: Subjects = self.subject_repository.get_subject_by_roll(
                student.roll
            )

            average = (
                subject_score.english_score
                + subject_score.math_score
                + subject_score.history_score
            ) / 3

            if average >=90:
                comment ="Excellent"
            elif average >= 80:
                comment ="Better"
            elif average >= 70:
                comment= "Good"
            else:
                comment ="Need Improved"    

            student_response = StudentResponse(
                id=student.id,
                name=student.name,
                age=student.age,
                email=student.email,
                roll=student.roll,
                session=student.session,
                department=student.department,
                english_score=subject_score.english_score,
                math_score=subject_score.math_score,
                history_score=subject_score.history_score,
                comment=comment
            )

            student_list.append(student_response)

        return student_list

    def add_student(self, student_payload: StudentCreate):
        student = Students(**student_payload.to_student_dict())
        self.repository.create_student(student)

        subject = Subjects(
            student_roll=student_payload.roll,
            english_score=student_payload.english_score,
            math_score=student_payload.math_score,
            history_score=student_payload.history_score,
        )
        self.subject_repository.create_subject(subject)

    def delete_student(self,student_roll:int):
        self.subject_repository.delete_subject_score(student_roll)
        self.repository.delete_student(student_roll)

    def update_student(self, roll:int, update_payload: StudentUpdate):
        student = self.repository.get_student_by_roll(roll)

        if student is None:
            return
        if update_payload.name is not None:
            student.name =update_payload.name
        if update_payload.email is not None:
            student.email = update_payload.email
        self.repository.update_student(student)


        subject_score = self.subject_repository.get_subject_by_roll(roll)

        if subject_score is None:
            return
        if update_payload.english_score is not None:
            subject_score.english_score = update_payload.english_score
        if update_payload.math_score is not None:
            subject_score.math_score = update_payload.math_score
        if update_payload.history_score is not None:
            subject_score.history_score = update_payload.history_score

        self.subject_repository.update_subject_score(subject_score)
