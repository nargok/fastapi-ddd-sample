from fastapi import FastAPI
from .presentation.routers import attendance_router


app = FastAPI(
    title="Attendance Management API",
    version="1.0.0"
)

app.include_router(attendance_router.router)


@app.get("/ping")
def ping():
    return { "message": "pong" }

