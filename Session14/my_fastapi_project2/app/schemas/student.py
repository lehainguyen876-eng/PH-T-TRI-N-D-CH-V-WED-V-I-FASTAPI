from pydantic import BaseModel

class StudentBase(BaseModel):
    full_name: str
    email: str
    major: str
    gpa: float

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int

    class Config:
        from_attributes = True