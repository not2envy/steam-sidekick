import os
import logging
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

@app.get("/")
def root():
    cpu_hwmon = find_hwmon("k10temp")
    gpu_hwmon = find_hwmon("amdgpu")

    return {
        "cpu": {
            "temperature": read_temp(f"{cpu_hwmon}/temp1_input")
        },
        "gpu": {
 	   "edge": read_temp(f"{gpu_hwmon}/temp1_input"),
   	   "junction": read_temp(f"{gpu_hwmon}/temp2_input"),
    	   "memory": read_temp(f"{gpu_hwmon}/temp3_input")

        }
    }
