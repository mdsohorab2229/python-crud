from sqlalchemy.orm import Session
from sqlalchemy import delete

from db import session_local
from model.subject import Subjects

class SubjectRepository:

    def __init__(self):
        self.connection = session_local()

    def get_all_subject(self):
        self.connection.query(Subjects).all()

    def create_subject(self, subject: Subjects):
        self.connection.add(subject)
        self.connection.commit()        

    def get_subject_by_roll(self, roll: int ):
        subject_score = self.connection.query(Subjects).filter(Subjects.student_roll==roll).first()
        return subject_score    

    def delete_subject_score(self, student_roll: int):
        stmt = delete(Subjects).where(Subjects.student_roll== student_roll )
        self.connection.execute(stmt)
        self.connection.commit()

    def update_subject_score(self, subject: Subjects):
        self.connection.merge(subject)
        self.connection.commit()

