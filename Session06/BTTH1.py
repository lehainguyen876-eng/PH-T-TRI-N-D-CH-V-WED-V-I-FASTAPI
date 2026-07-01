from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

courses = [
    {"id": 1, "code": "PY101", "name": "Python Basic", "duration": 30, "fee": 3000000},
    {"id": 2, "code": "API101", "name": "FastAPI Basic", "duration": 24, "fee": 2500000},
    {"id": 3, "code": "JV101", "name": "Java Basic", "duration": 40, "fee": 4000000}
]

class CourseCreate(BaseModel):
    code: str = Field(..., min_length=1, description="Mã khóa học không được trống")
    name: str = Field(..., min_length=1, description="Tên khóa học không được rỗng")
    duration: int = Field(..., gt=0, description="Thời lượng phải lớn hơn 0")
    fee: float = Field(..., ge=0, description="Học phí phải lớn hơn hoặc bằng 0")

class CourseUpdate(BaseModel):
    code: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    duration: int = Field(..., gt=0)
    fee: float = Field(..., ge=0)

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate):
    if any(c["code"].upper() == course.code.upper() for c in courses):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
    
    new_course = {
        "id": max([c["id"] for c in courses], default=0) + 1,
        "code": course.code,
        "name": course.name,
        "duration": course.duration,
        "fee": course.fee
    }
    courses.append(new_course)
    return {"message": "Course created successfully", "data": new_course}


@app.get("/courses")
def get_courses(
    keyword: Optional[str] = Query(None, description="Tìm theo name hoặc code"),
    min_fee: Optional[float] = Query(None, ge=0, description="Học phí tối thiểu"),
    max_fee: Optional[float] = Query(None, ge=0, description="Học phí tối đa")
):
    filtered_courses = courses.copy()
    
    if keyword:
        keyword_lower = keyword.lower()
        filtered_courses = [
            c for c in filtered_courses 
            if keyword_lower in c["name"].lower() or keyword_lower in c["code"].lower()
        ]
        
    if min_fee is not None:
        filtered_courses = [c for c in filtered_courses if c["fee"] >= min_fee]
    
    if max_fee is not None:
        filtered_courses = [c for c in filtered_courses if c["fee"] <= max_fee]
        
    return filtered_courses


@app.get("/courses/{course_id}")
def get_course_detail(course_id: int):
    target_course = next((c for c in courses if c["id"] == course_id), None)
    if not target_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    return target_course

@app.put("/courses/{course_id}")
def update_course(course_id: int, payload: CourseUpdate):
    target_course = next((c for c in courses if c["id"] == course_id), None)
    if not target_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    if any(c["code"].upper() == payload.code.upper() and c["id"] != course_id for c in courses):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course code already exists"
        )
        
    target_course["code"] = payload.code
    target_course["name"] = payload.name
    target_course["duration"] = payload.duration
    target_course["fee"] = payload.fee
    
    return {"message": "Course updated successfully", "data": target_course}


@app.delete("/courses/{course_id}")
def delete_course(course_id: int):
    target_course = next((c for c in courses if c["id"] == course_id), None)
    if not target_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    courses.remove(target_course)
    return {"message": f"Course with ID {course_id} deleted successfully"}