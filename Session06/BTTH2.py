from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

app = FastAPI()

students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class StudentCreate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., gt=0)

class StudentUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    email: EmailStr
    age: int = Field(..., gt=0)

@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate):
    if any(s["code"].upper() == student.code.upper() for s in students):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student code already exists")
    
    new_student = {
        "id": max([s["id"] for s in students], default=0) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }
    students.append(new_student)
    return {"message": "Student created successfully", "data": new_student}

@app.get("/students")
def get_students(
    keyword: Optional[str] = Query(None),
    min_age: Optional[int] = Query(None, ge=1),
    max_age: Optional[int] = Query(None, ge=1)
):
    filtered_students = students.copy()
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_students = [
            s for s in filtered_students 
            if keyword_lower in s["name"].lower() 
            or keyword_lower in s["code"].lower() 
            or keyword_lower in s["email"].lower()
        ]
        
    if min_age is not None:
        filtered_students = [s for s in filtered_students if s["age"] >= min_age]
        
    if max_age is not None:
        filtered_students = [s for s in filtered_students if s["age"] <= max_age]
        
    return filtered_students

@app.get("/students/{student_id}")
def get_student_detail(student_id: int):
    target_student = next((s for s in students if s["id"] == student_id), None)
    if not target_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return target_student

@app.put("/students/{student_id}")
def update_student(student_id: int, payload: StudentUpdate):
    target_student = next((s for s in students if s["id"] == student_id), None)
    if not target_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
    if any(s["code"].upper() == payload.code.upper() and s["id"] != student_id for s in students):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student code already exists")
        
    target_student["code"] = payload.code
    target_student["name"] = payload.name
    target_student["email"] = payload.email
    target_student["age"] = payload.age
    
    return {"message": "Student updated successfully", "data": target_student}

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    target_student = next((s for s in students if s["id"] == student_id), None)
    if not target_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        
    students.remove(target_student)
    return {"message": f"Student with ID {student_id} deleted successfully"}