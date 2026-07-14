"""Lỗi: Kiểm tra sai khóa liên kết dẫn đến việc một người dùng tạo được nhiều hồ sơ
Dữ liệu test: Gửi yêu cầu tạo hồ sơ lần 2 cho người dùng user_id: 1 (đã có sẵn hồ sơ trong danh sách với id: 10).
URL: /users/1/profile
Body:
{
    "full_name": "Nguyễn Văn An",
    "phone": "0901000005",
    "address": "Đà Nẵng"
}
Kết quả thực tế: Hệ thống trả về mã 201 Created và vẫn tiếp tục tạo thêm một hồ sơ mới cho người dùng này.

Kết quả mong đợi: Hệ thống phải chặn lại, trả về mã lỗi 409 Conflict báo lỗi "Người dùng đã có hồ sơ".

Nguyên nhân lỗi: Đoạn code kiểm tra trùng đang so sánh nhầm trường: if profile["id"] == user_id. Hệ thống lại lấy trường id của chính cái hồ sơ (ví dụ số 10) đi so sánh với mã người dùng user_id (số 1), làm cho điều kiện chặn luôn bị bỏ qua.

Đoạn code cần sửa: Sửa trường so sánh từ profile["id"] thành profile["user_id"].
    """
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(
    title = "QUẢN LÝ HỒ SƠ NGƯỜI DÙNG"
)

class UserProfileCreateDTO(BaseModel):
    full_name: str
    phone: str
    address: str | None = None

users = [
    {
        "id": 1,
        "username": "nguyenvanan",
        "email": "an@gmail.com"
    },
    {
        "id": 2,
        "username": "tranthibinh",
        "email": "binh@gmail.com"
    }
]

profiles = [
    {
        "id": 10,
        "full_name": "Nguyễn Văn An",
        "phone": "0901000001",
        "address": "Hà Nội",
        "user_id": 1
    }
]

@app.get("/users", tags=["Users"], status_code=status.HTTP_200_OK)
def get_users():
    return {
        "message": "Lấy danh sách người dùng thành công",
        "data": users
    }

@app.get("/profiles", tags=["Profiles"], status_code=status.HTTP_200_OK)
def get_profiles():
    return {
        "message": "Lấy danh sách hồ sơ thành công",
        "data": profiles
    }

@app.post("/users/{user_id}/profile", tags=["Profiles"], status_code=status.HTTP_201_CREATED)
def create_profile(user_id: int, profile_data: UserProfileCreateDTO):
    user_exists = next(
        (
            user 
            for user in users 
            if user["id"] == user_id
        ), 
        None
    )
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )

    existing_profile = next(
        (
            profile
            for profile in profiles
            if profile["user_id"] == user_id
        ),
        None
    )
    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Người dùng đã có hồ sơ"
        )

    duplicated_phone = next(
        (
            profile
            for profile in profiles
            if profile["phone"] == profile_data.phone
        ),
        None
    )
    if duplicated_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Số điện thoại đã được sử dụng"
        )

    new_profile = {
        "id": len(profiles) + 1,
        "full_name": profile_data.full_name,
        "phone": profile_data.phone,
        "address": profile_data.address,
        "user_id": user_id
    }
    profiles.append(new_profile)
    
    return {
        "message": "Tạo hồ sơ người dùng thành công",
        "data": new_profile
    }