from fastapi import FastAPI
from app.api import endpoints
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="A AI Writing System",
    description="Using AI to Write",
    version="0.1.01"
)

origins = [
    "http://localhost:5173",
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许访问的源
    allow_credentials=True,  # 支持 cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

app.include_router(endpoints.router, prefix="/api/v1")
app.include_router(endpoints.outline_router, prefix="/api/v1")
app.include_router(endpoints.settings_router, prefix="/api/v1")

@app.get("/")
def get_root():
    return "Hi"
