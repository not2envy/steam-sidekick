from fastapi import APIRouter
from services.metrics import get_gpu_metrics

# Create the router instance
router = APIRouter()

# Use @router.get instead of @app.get
@router.get("/gpu")
def read_gpu_metrics():
    return get_gpu_metrics()