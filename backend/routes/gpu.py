from fastapi import APIRouter, Depends
from services.metrics import get_gpu_metrics
from models.metrics import GpuMetrics

# Create the router instance
router = APIRouter()

# Use @router.get instead of @app.get
@router.get("/gpu", response_model=GpuMetrics)
def read_gpu_metrics(gpu_data: GpuMetrics = Depends(get_gpu_metrics)):
    return gpu_data