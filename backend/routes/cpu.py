from fastapi import APIRouter
from services.metrics import get_cpu_metrics

router = APIRouter()

@router.get("/cpu")
def read_cpu_metrics():
    return get_cpu_metrics()