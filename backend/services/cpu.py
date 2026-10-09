import time
from models.metrics import CpuMetrics
from exceptions import SensorReadingError
from services.hardware import get_hardware_temperature


def _get_cpu_temperature():
    return get_hardware_temperature(
        sensor_name="k10temp",
        temperature_key="cpu_temperature",
        device_name="CPU"
    )


def _read_cpu_times():
    path = "/proc/stat"
    try:
        with open(path, "r") as f:
            line = f.readline().strip()
            return line.split()
    except Exception:
        return None


def _get_cpu_time_readings():
    cpu_times = _read_cpu_times()

    if cpu_times is None:
        raise SensorReadingError("CPU times could not be read")
    return cpu_times


def _get_cpu_usage():
    cpu_times = _get_cpu_time_readings()

    # Read raw string data and immediately convert values to integers (skipping "cpu")
    first = [int(x) for x in cpu_times[1:]]

    # Wait for the sample interval
    time.sleep(0.1)

    cpu_times = _get_cpu_time_readings()

    # Read second sample and immediately convert to integers (skipping "cpu")
    second = [int(x) for x in cpu_times[1:]]

    # Perform calculations using pure integer arrays
    # Note: Index 3 corresponds to the original index 4 ("idle") because we sliced off "cpu"
    idle_diff = second[3] - first[3]

    # Calculate differences element-by-element
    diffs = [b - a for a, b in zip(first, second)]
    grand_total = sum(diffs)

    # Prevent division-by-zero error
    if grand_total:
        cpu_usage = (grand_total - idle_diff) / grand_total * 100
    else:
        cpu_usage = 0.0

    return {
        "cpu_usage": round(cpu_usage, 1)
    }


def get_cpu_metrics() -> CpuMetrics:
    usage = _get_cpu_usage()
    cpu_temp = _get_cpu_temperature()
    return CpuMetrics(
        usage=usage["cpu_usage"],
        temperature=cpu_temp["cpu_temperature"]
        )