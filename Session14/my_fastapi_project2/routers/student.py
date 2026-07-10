from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student import StudentService

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)

@router.get("/", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return StudentService.get_all(db)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = StudentService.get_by_id(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student_in: StudentCreate, db: Session = Depends(get_db)):
    return StudentService.create(db, student_in)

@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student_in: StudentCreate, db: Session = Depends(get_db)):
    student = StudentService.update(db, student_id, student_in)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    success = StudentService.delete(db, student_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return None