from services.metrics import get_cpu_metrics, get_gpu_metrics
from models.metrics import CpuMetrics, GpuMetrics


def test_get_cpu_metrics_returns_cpu_metrics(mocker):
    # Arrange
    # Pretend the CPU usage is 42.5%
    mocker.patch(
        "services.metrics.get_cpu_usage",
          return_value={"cpu_usage": 49}
          )
    # Pretend the CPU temperature is 58.0°C
    mocker.patch(
        "services.metrics.get_cpu_temperature",
          return_value={"cpu_temperature": 43}
          )

    # Act
    result = get_cpu_metrics()

    # Assert
    # Is result a CpuMetrics object?
    assert isinstance(result, CpuMetrics)
    assert result.usage == 49
    assert result.temperature == 43

def test_get_gpu_metrics_returns_gpu_metrics(mocker):
    # Arrange
    mocker.patch(
        "services.metrics.get_gpu_usage",
            return_value={"gpu_usage": 49}
            )
    mocker.patch(
        "services.metrics.get_gpu_temperature",
            return_value={"gpu_temperature": 43}
            )
    mocker.patch(
        "services.metrics.get_gpu_memory_usage",
            return_value={"gpu_memory_usage": 60}
            )

    # Act
    result = get_gpu_metrics()

    # Assert
    # Is result a GpuMetrics object?
    assert isinstance(result, GpuMetrics)
    assert result.usage == 49
    assert result.temperature == 43
    assert result.memory == 60