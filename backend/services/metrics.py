import os

from exceptions import (
    SensorNotFoundError,
    SensorReadingError
)
from models.metrics import GpuMetrics

from services.hardware import get_hardware_temperature

def get_vendor_id(vendor_path):
    with open(vendor_path, "r") as f:
            # Strip whitespace and normalize to lowercase for clean matching
            vendor_id = f.read().strip().lower()
    return vendor_id

def find_amd_gpu_card():
    """
    Dynamically scans /sys/class/drm to locate the correct AMD GPU card index.
    Returns the base path string (e.g., '/sys/class/drm/card0') or None if not found.
    """
    base_drm_path = "/sys/class/drm"
    amd_vendor_id = "0x1002"
    
    # 1. Safety check to ensure the DRM directory exists on the system
    if not os.path.isdir(base_drm_path):
        return None

    try:
        # 2. List all items in the DRM directory
        for entry in os.listdir(base_drm_path):
            # Target only entries that look exactly like 'card0', 'card1', etc.
            # This ignores 'card1-DP-1', 'renderD128', and display interfaces.
            if entry.startswith("card") and "-" not in entry:
                vendor_path = os.path.join(base_drm_path, entry, "device/vendor")
                
                # 3. Check if this card entry has a device/vendor hardware file
                if os.path.isfile(vendor_path):
                    try:
                        vendor_id =get_vendor_id(vendor_path)
                            
                        # 4. If it matches the AMD Vendor ID, we found our GPU
                        if vendor_id == amd_vendor_id:
                            return os.path.join(base_drm_path, entry)
                    except Exception:
                        continue  # Skip to the next card if a file is unreadable (e.g., permission issue)
                        
    except Exception:
        return None
        
    return None  # Return None if no AMD GPU card was discovered

# Run the discovery once at startup.
_AMD_GPU_BASE = find_amd_gpu_card()

def find_gpu_info(sensor_name):
    # Seamlessly build the path using the cached base path
    if _AMD_GPU_BASE is None:
        return None

    return os.path.join(_AMD_GPU_BASE, "device", sensor_name)


def get_gpu_temperature():
    return get_hardware_temperature(
        sensor_name="amdgpu",
        temperature_key="gpu_temperature",
        device_name="GPU"
    )


def read_gpu_stats(path):
    if path is None:
        return None

    try:
        with open(path, "r") as f:
            return int(f.read().strip())
    except Exception:
        return None


def get_gpu_metric(sensor_name, metric_key, error_message):
    """
    Reads a GPU metric from the Linux sysfs interface.
    Returns:
        A dictionary containing the requested GPU metric.
    Raises:
        SensorNotFoundError: If the GPU metric cannot be found.
        SensorReadingError: If the GPU metric could not be read.
    """
    # 1. Generate the string path
    path = find_gpu_info(sensor_name)
    if path is None:
        raise SensorNotFoundError(f"{sensor_name} sensor not found")
    
    # 2. Attempt to read and parse the file contents
    value = read_gpu_stats(path)
    
    # 3. Handle errors based purely on the returned value
    if value is None:
        raise SensorReadingError(error_message)
        
    # 4. Success path returning a structured dictionary
    return {metric_key: value}


def get_gpu_usage():
    return get_gpu_metric(
        sensor_name="gpu_busy_percent",
        metric_key="gpu_usage",
        error_message="GPU sensor statistic could not be read"
    )


def get_gpu_memory_usage():
    return get_gpu_metric(
        sensor_name="mem_busy_percent",
        metric_key="gpu_memory_usage",
        error_message="GPU memory statistic could not be read"
    )


def get_gpu_metrics() -> GpuMetrics:
    gpu_temp = get_gpu_temperature()
    gpu_usage = get_gpu_usage()
    gpu_memory = get_gpu_memory_usage()
    return GpuMetrics(
        temperature=gpu_temp["gpu_temperature"],
        usage=gpu_usage["gpu_usage"],
        memory=gpu_memory["gpu_memory_usage"]
    )
