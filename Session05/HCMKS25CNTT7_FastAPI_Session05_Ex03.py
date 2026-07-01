from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class RegistrationCreate(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=status.HTTP_201_CREATED)
def create_registration(registration: RegistrationCreate):
    if not any(s["id"] == registration.student_id for s in students):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    target_course = next((c for c in courses if c["id"] == registration.course_id), None)
    if not target_course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
        
    if any(r["student_id"] == registration.student_id and r["course_id"] == registration.course_id for r in registrations):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Student already registered this course")
            
    current_enrolled = sum(1 for r in registrations if r["course_id"] == registration.course_id)
    if current_enrolled >= target_course["capacity"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course is full")
        
    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }
    registrations.append(new_registration)
    return {"message": "Registration created successfully", "data": new_registration}

"""
1. PHÂN TÍCH BÀI TOÁN
   - Input: JSON Body gồm `student_id` (int) và `course_id` (int).
   - Output thành công: HTTP 201 Created kèm thông tin phiếu đăng ký mới.
   - Output thất bại: HTTP 400 (Trùng bài/Đầy lớp) hoặc HTTP 404 (Không tìm thấy ID) kèm thông báo {"detail": "..."}.

2. ĐỀ XUẤT GIẢI PHÁP (Luồng xử lý)
   - Bước 1: Validate đầu vào bằng Pydantic.
   - Bước 2: Kiểm tra thực thể -> Đảm bảo `student_id` và `course_id` có thật trong hệ thống.
   - Bước 3: Chặn bẫy 1 -> Duyệt `registrations`, nếu cặp (student_id, course_id) đã tồn tại -> Báo lỗi trùng.
   - Bước 4: Chặn bẫy 2 -> Đếm số học viên hiện tại của khóa học, nếu >= `capacity` -> Báo lỗi đầy lớp.
   - Bước 5: Thêm dữ liệu vào mảng và phản hồi HTTP 201.
"""