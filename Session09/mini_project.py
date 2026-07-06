from fastapi import FastAPI, Request, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Any, Optional

app = FastAPI()

tasks_db = [
    {
        "id": 1, 
        "title": "Thiet ke database Shop AI", 
        "description": "Xay dung bang va toi uu index", 
        "assignee": "QuyDev", 
        "priority": 1, 
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2, 
        "title": "Code bo API Authen", 
        "description": "Trien khai filter verify JWT token", 
        "assignee": "FixerQ", 
        "priority": 2, 
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

class taskadd(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=1)
    assignee: str = Field(min_length=1)
    priority: int = Field(ge=1, le=5)

class taskup(BaseModel):
    status: str = Field(min_length=1)

class apiresponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[Any] = None
    timestamp: str
    path: str

def success_response(data: Any, message: str, request: Request, status_code: int = 200) -> apiresponse:
    return apiresponse(
        statusCode=status_code,
        message=message,
        data=data,
        timestamp=datetime.utcnow().isoformat() + "Z",
        path=request.url.path
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=apiresponse(
            statusCode=422,
            message="Lỗi: Dữ liệu đầu vào không hợp lệ hoặc sai định dạng quy định!",
            error="ERR-VAL-422: Validation error at Request Body fields constraint layout.",
            timestamp=datetime.utcnow().isoformat() + "Z",
            path=request.url.path
        ).dict()
    )

@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    err_code = "ERR-TASK-03" if exc.status_code == 404 else "ERR-TASK-01" if exc.detail.startswith("Lỗi: Tiêu đề") else "ERR-TASK-04"
    err_desc = "Task not found with the given ID." if exc.status_code == 404 else "Task conflict: Title field duplicates an existing record." if err_code == "ERR-TASK-01" else "Cannot update status because the task is already done."
    return JSONResponse(
        status_code=exc.status_code,
        content=apiresponse(
            statusCode=exc.status_code,
            message=exc.detail,
            error=f"{err_code}: {err_desc}",
            timestamp=datetime.utcnow().isoformat() + "Z",
            path=request.url.path
        ).dict()
    )

@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=apiresponse(
            statusCode=500,
            message="Lỗi hệ thống nghiêm trọng!",
            error=f"ERR-SYS-500: {str(exc)}",
            timestamp=datetime.utcnow().isoformat() + "Z",
            path=request.url.path
        ).dict()
    )

def calculate_team_metrics() -> tuple[int, int, float]:
    total = len(tasks_db)
    if total == 0:
        return 0, 0, 0.0
    completed = sum(1 for t in tasks_db if t["status"] == "done")
    rate = round((completed / total) * 100, 1)
    return total, completed, rate

@app.get("/tasks")
def get_all_tasks(request: Request, status: Optional[str] = None):
    if status:
        filtered = [t for t in tasks_db if t["status"].lower() == status.lower()]
        return success_response(data=filtered, message="Lấy danh sách công việc thành công!", request=request)
    return success_response(data=tasks_db, message="Lấy danh sách công việc thành công!", request=request)

@app.post("/tasks")
def create_task(request: Request, task_in: taskadd):
    for t in tasks_db:
        if t["title"].strip().lower() == task_in.title.strip().lower():
            raise HTTPException(status_code=400, detail="Lỗi: Tiêu đề công việc này đã tồn tại trong nhóm!")
            
    max_id = max([t["id"] for t in tasks_db]) if tasks_db else 0
    new_task = {
        "id": max_id + 1,
        "title": task_in.title,
        "description": task_in.description,
        "assignee": task_in.assignee,
        "priority": task_in.priority,
        "status": "todo",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    tasks_db.append(new_task)
    return success_response(data=new_task, message="Khởi tạo công việc mới thành công!", request=request, status_code=201)

@app.put("/tasks/{task_id}")
def update_task_status(request: Request, task_id: int, status_in: taskup):
    target_task = None
    for t in tasks_db:
        if t["id"] == task_id:
            target_task = t
            break
            
    if not target_task:
        raise HTTPException(status_code=404, detail="Lỗi: Không tìm thấy công việc tương ứng với ID cung cấp!")
        
    if target_task["status"] == "done":
        raise HTTPException(status_code=400, detail="Lỗi: Không thể cập nhật trạng thái lùi khi công việc đã hoàn thành!")
        
    target_task["status"] = status_in.status
    return success_response(data=target_task, message="Cập nhật tiến độ công việc thành công!", request=request)

@app.get("/tasks/analytics/dashboard")
def get_dashboard_analytics(request: Request):
    total, completed, rate = calculate_team_metrics()
    metrics_data = {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_rate_percentage": rate
    }
    return success_response(data=metrics_data, message="Lấy số liệu thống kê hiệu suất nhóm thành công!", request=request)