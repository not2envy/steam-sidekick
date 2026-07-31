from fastapi.testclient import TestClient
from app import app
from services.metrics import get_cpu_metrics, get_gpu_metrics
from models.metrics import CpuMetrics, GpuMetrics, SystemMetrics

client = TestClient(app)

def test_get_cpu_route_returns_cpu_metrics():
    # Arrange
    def mock_get_cpu_metrics():
        return CpuMetrics(
             usage=49,
             temperature=43
         )
        
    app.dependency_overrides[get_cpu_metrics] = mock_get_cpu_metrics

    try:
        # Act
        response = client.get("/cpu")

        # Assert
        assert response.status_code == 200

        data = response.json()

        assert "usage" in data
        assert "temperature" in data

        assert data["usage"] == 49
        assert data["temperature"] == 43
    finally:
        app.dependency_overrides.clear()


def test_get_gpu_route_returns_gpu_metrics():
    # Arrange
    def mock_get_gpu_metrics():
        return GpuMetrics(
            usage=49,
            temperature=43,
            memory=24
        )
    
    app.dependency_overrides[get_gpu_metrics] = mock_get_gpu_metrics
    
    try:
        # Act
        response = client.get("/gpu")

        # Assert
        assert response.status_code == 200

        data = response.json()

        assert "usage" in data
        assert "temperature" in data
        assert "memory" in data

        assert data["usage"] == 49
        assert data["temperature"] == 43
        assert data["memory"] == 24
    finally:
        app.dependency_overrides.clear()

def test_get_system_route_returns_system_metrics():
    # Arrange
    def mock_get_cpu_metrics():
            return CpuMetrics(
                 usage=49,
                 temperature=43
             )
    def mock_get_gpu_metrics():
            return GpuMetrics(
                usage=49,
                temperature=43,
                memory=24
            )

    app.dependency_overrides[get_cpu_metrics] = mock_get_cpu_metrics
    app.dependency_overrides[get_gpu_metrics] = mock_get_gpu_metrics

    try:
        # Act
        response = client.get("/system")
        
        # Assert
        assert response.status_code == 200
        data = response.json()

        assert "usage" in data["cpu"]
        assert "temperature" in data["cpu"]

        assert "usage" in data["gpu"]
        assert "temperature" in data["gpu"]
        assert "memory" in data["gpu"]

        assert data["cpu"]["usage"] == 49
        assert data["cpu"]["temperature"] == 43

        assert data["gpu"]["usage"] == 49
        assert data["gpu"]["temperature"] == 43
        assert data["gpu"]["memory"] == 24

    finally:
        app.dependency_overrides.clear()