from fastapi import APIRouter
from services.metrics import get_cpu_metrics, get_gpu_metrics
from models.metrics import SystemMetrics

# Create the composition router instance
router = APIRouter()

# Define your combined system tracking route
@router.get("/system", response_model=SystemMetrics)
def read_system_metrics():
    return {
        "cpu": get_cpu_metrics(),
        "gpu": get_gpu_metrics()
    }
