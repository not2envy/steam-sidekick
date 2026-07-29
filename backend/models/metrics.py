from pydantic import BaseModel


class CpuMetrics(BaseModel):
    usage: float
    temperature: float


class GpuMetrics(BaseModel):
    temperature: float
    usage: float
    memory: float


class SystemMetrics(BaseModel):
    cpu: CpuMetrics
    gpu: GpuMetrics