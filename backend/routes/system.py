from fastapi import APIRouter
from services.metrics import get_cpu_metrics, get_gpu_metrics

# Create the composition router instance
router = APIRouter()

# Define your combined system tracking route
@router.get("/system")
def read_system_metrics():
    return {
        "cpu": get_cpu_metrics(),
        "gpu": get_gpu_metrics()
    }
