"""Lỗi 2: Vượt quá số lượng sinh viên tối đa
Dữ liệu test: Thêm vào lớp có id: 1 (đã có 2 sinh viên, max_students: 2).

Kết quả thực tế: Trả về 201 Created và vẫn thêm được sinh viên thứ 3.

Kết quả mong đợi: Trả về 400 Bad Request, báo lớp đã đầy.

Nguyên nhân lỗi: Dùng sai dấu so sánh >. Lớp có 2 người thì điều kiện 2 > 2 bị sai (False) nên bỏ qua chặn lỗi.

Đoạn code cần sửa: Sửa dấu > thành >=.
if classroom and len(current_students) >= classroom["max_students"]:
    """

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title = "QUẢN LÝ SINH VIÊN VÀ LỚP HỌC"
)

class StudentCreateDTO(BaseModel):
    student_code: str
    full_name: str
    class_id: int

classrooms = [
    {
        "id": 1,
        "name": "FastAPI Basic",
        "max_students": 2,
        "status": "OPEN"
    },
    {
        "id": 2,
        "name": "Python Foundation",
        "max_students": 3,
        "status": "CLOSED"
    }
]

students = [
    {
        "id": 1,
        "student_code": "SV001",
        "full_name": "Nguyễn Văn An",
        "class_id": 1
    },
    {
        "id": 2,
        "student_code": "SV002",
        "full_name": "Trần Minh Bình",
        "class_id": 1
    }
]

@app.get("/classrooms", tags=["Classrooms"], status_code=status.HTTP_200_OK)
def get_classrooms():
    return {
        "message": "Lấy danh sách lớp học thành công",
        "data": classrooms
    }

@app.get("/students", tags=["Students"], status_code=status.HTTP_200_OK)
def get_students():
    return {
        "message": "Lấy danh sách sinh viên thành công",
        "data": students
    }

@app.post("/students", tags=["Students"], status_code=status.HTTP_201_CREATED)
def create_student(student_data: StudentCreateDTO):
    duplicated_student = next(
        (
            student
            for student in students
            if student["student_code"] == student_data.student_code
        ),
        None
    )
    if duplicated_student:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Mã sinh viên đã tồn tại trong hệ thống"
        )

    classroom = next(
        (
            classroom
            for classroom in classrooms
            if classroom["id"] == student_data.class_id
        ),
        None
    )
    if not classroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lớp học không tồn tại"
        )

    if classroom["status"] == "CLOSED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đã đóng"
        )

    current_students = [
        student
        for student in students
        if student["class_id"] == student_data.class_id
    ]
    if len(current_students) >= classroom["max_students"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lớp học đã đủ số lượng sinh viên tối đa"
        )

    new_student = {
        "id": len(students) + 1,
        "student_code": student_data.student_code,
        "full_name": student_data.full_name,
        "class_id": student_data.class_id
    }
    students.append(new_student)
    
    return {
        "message": "Thêm sinh viên vào lớp thành công",
        "data": new_student
    }