import logging

from fastapi import FastAPI

from routes.cpu import router as cpu_router
from routes.gpu import router as gpu_router
from routes.system import router as system_router

logger = logging.getLogger("uvicorn")
app = FastAPI(title="Steam Sidekick API")

app.include_router(cpu_router)
app.include_router(gpu_router)
app.include_router(system_router)

@app.get("/")
def root():
    return {
        "message": "Steam Sidekick API",
        "version": "0.1.0"
    }