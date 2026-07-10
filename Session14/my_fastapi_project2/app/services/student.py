from sqlalchemy.orm import Session
from app.models.student import StudentModel
from app.schemas.student import StudentCreate

class StudentService:
    @staticmethod
    def get_all(db: Session):
        return db.query(StudentModel).all()

    @staticmethod
    def get_by_id(db: Session, student_id: int):
        return db.query(StudentModel).filter(StudentModel.id == student_id).first()

    @staticmethod
    def create(db: Session, student_data: StudentCreate):
        db_student = StudentModel(
            full_name=student_data.full_name,
            email=student_data.email,
            major=student_data.major,
            gpa=student_data.gpa
        )
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def update(db: Session, student_id: int, student_data: StudentCreate):
        db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if not db_student:
            return None
        
        db_student.full_name = student_data.full_name
        db_student.email = student_data.email
        db_student.major = student_data.major
        db_student.gpa = student_data.gpa
        
        db.commit()
        db.refresh(db_student)
        return db_student

    @staticmethod
    def delete(db: Session, student_id: int):
        db_student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if not db_student:
            return False
        
        db.delete(db_student)
        db.commit()
        return True