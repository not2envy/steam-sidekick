import os
import logging
import time
from fastapi import FastAPI

logger = logging.getLogger("uvicorn")

app = FastAPI(title="Steam Sidekick API")


def read_temp(path):
    try:
        with open(path, "r") as f:
            return round(int(f.read().strip()) / 1000, 1)
    except Exception:
        return None


def find_hwmon(sensor_name):
    hwmon_root = "/sys/class/hwmon"

    for entry in os.listdir(hwmon_root):
        name_file = os.path.join(hwmon_root, entry, "name")

        try:
            with open(name_file, "r") as f:
                if f.read().strip() == sensor_name:
                    return os.path.join(hwmon_root, entry)
        except Exception:
            continue

    return None

def get_cpu_temperature():
    cpu_hwmon = find_hwmon("k10temp")

    if cpu_hwmon is None:
        return {
            "error": "CPU sensor not found"
        }

    return { 
        "cpu_temperature": read_temp(f"{cpu_hwmon}/temp1_input")
            
        }

def read_cpu_times():
        path = "/proc/stat"
        try:
            with open(path, "r") as f:
                line = f.readline().strip()
                return line.split()
        except Exception:
            return None
        return None

def get_cpu_usage():
    # 1. Read raw string data and immediately convert values to integers (skipping "cpu")
    first = [int(x) for x in read_cpu_times()[1:]]
    
    # Wait for the sample interval
    time.sleep(0.1)
    
    # 2. Read second sample and immediately convert to integers (skipping "cpu")
    second = [int(x) for x in read_cpu_times()[1:]]
    
    # 3. Perform calculations using pure integer arrays
    # Note: Index 3 corresponds to the original index 4 ("idle") because we sliced off "cpu"
    idle_diff = second[3] - first[3]
    
    # Calculate differences element-by-element
    diffs = [b - a for a, b in zip(first, second)]
    grand_total = sum(diffs)
    
    # 4. Prevent division-by-zero error
    if grand_total:
        cpu_usage = (grand_total - idle_diff) / grand_total * 100
    else:
        cpu_usage = 0.0
        
    return {
        "cpu_usage": round(cpu_usage, 1)
    }

def get_gpu_temperature():
    gpu_hwmon = find_hwmon("amdgpu")
    
    if gpu_hwmon is None:
        return {
            "error": "GPU sensor not found"
        }
    
    return { 
        "gpu_temperature": read_temp(f"{gpu_hwmon}/temp1_input")
            
        }

@app.get("/")
def root():
    usage = get_cpu_usage()
    cpu_temp = get_cpu_temperature()
    gpu_temp = get_gpu_temperature()

    return {
        "cpu": {
            "usage":usage["cpu_usage"],
            "temperature":cpu_temp["cpu_temperature"]
        },
        "gpu": {
            "temperature": gpu_temp["gpu_temperature"]
        }
    } 

    # return {
        
    #     "cpu": {
    #         "temperature": read_temp(f"{cpu_hwmon}/temp1_input")
    #     },
    #     "gpu": {
 	#    "edge": read_temp(f"{gpu_hwmon}/temp1_input"),
   	#    "junction": read_temp(f"{gpu_hwmon}/temp2_input"),
    #    "memory": read_temp(f"{gpu_hwmon}/temp3_input")

    #     }
    # }
