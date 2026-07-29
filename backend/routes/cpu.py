from fastapi import APIRouter
from services.metrics import get_cpu_metrics
from models.metrics import CpuMetrics

router = APIRouter()

@router.get("/cpu", response_model=CpuMetrics)
def read_cpu_metrics():
    return get_cpu_metrics()
