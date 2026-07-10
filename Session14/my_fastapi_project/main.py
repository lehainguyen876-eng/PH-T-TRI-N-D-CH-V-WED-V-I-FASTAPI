import uvicorn
from fastapi import FastAPI
from app.routers.product import router as product_router

app = FastAPI(
    title="Product Management API",
    description="Hệ thống API CRUD Quản lý Sản phẩm bài tập tổng hợp 1",
    version="1.0.0"
)

# Đăng ký router
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Welcome to Product Management API. Go to /docs for API documentation."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)