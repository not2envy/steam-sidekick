from fastapi import APIRouter, Depends
from services.metrics import get_cpu_metrics, get_gpu_metrics
from models.metrics import CpuMetrics, GpuMetrics, SystemMetrics

# Create the composition router instance
router = APIRouter()

# Define your combined system tracking route
@router.get("/system", response_model=SystemMetrics)
def read_system_metrics(cpu_data: CpuMetrics = Depends(get_cpu_metrics),
                        gpu_data: GpuMetrics = Depends(get_gpu_metrics)):
    return SystemMetrics(
            cpu = cpu_data,
            gpu = gpu_data
        )
