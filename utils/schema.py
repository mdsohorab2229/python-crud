from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class StudentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    age: int
    email: EmailStr
    roll: int
    session: str
    department: str
    english_score: int = Field(le=100, ge=0)
    math_score: int = Field(le=100, ge=0)
    history_score: int = Field(le=100, ge=0)

    def to_student_dict(self):
        return self.model_dump(exclude={"english_score", "math_score", "history_score"})


class StudentResponse(StudentCreate):
    id: int
    comment: Optional[str]

    class Config:
        from_attributes = True


class StudentUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    english_score: Optional[int] = None
    math_score: Optional[int] = None
    history_score: Optional[int] = None
