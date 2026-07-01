from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

enrollments = [
    {
        "id": 1,
        "student_id": "SV001",
        "course_id": 1
    },
    {
        "id": 2,
        "student_id": "SV002",
        "course_id": 1
    }
]

class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: int

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(enrollment: EnrollmentCreate):
    for e in enrollments:
        if e["student_id"] == enrollment.student_id and e["course_id"] == enrollment.course_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Học viên '{enrollment.student_id}' đã đăng ký khóa học id {enrollment.course_id} trước đó rồi."
            )
            
    new_enrollment = {
        "id": len(enrollments) + 1,
        "student_id": enrollment.student_id,
        "course_id": enrollment.course_id
    }
    
    enrollments.append(new_enrollment)
    return {
        "message": "Enroll successfully",
        "data": new_enrollment
    }

"""
BẢNG PHÂN TÍCH TEST CASE CHỨNG MINH API CŨ BỊ SAI LOGIC NGHIỆP VỤ:

STT | Dữ liệu gửi lên (Body)                  | Kết quả hiện tại (Cũ)           | Kết quả đúng mong muốn             | Lỗi phát hiện

1   | {"student_id": "SV001", "course_id": 1} | Vẫn đăng ký được (HTTP 200)     | Báo lỗi đã đăng ký (HTTP 400)      | Không kiểm tra trùng cặp trùng student_id và course_id.
2   | {"student_id": "SV002", "course_id": 1} | Vẫn đăng ký được (HTTP 200)     | Báo lỗi đã đăng ký (HTTP 400)      | Cho phép một học viên đăng ký một khóa học nhiều lần.
"""