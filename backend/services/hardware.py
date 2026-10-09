import os
from exceptions import (
    SensorNotFoundError,
    SensorReadingError
)


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


def get_hardware_temperature(sensor_name, temperature_key, device_name):
    sensor_path = find_hwmon(sensor_name)
    if sensor_path is None:
        raise SensorNotFoundError(f"{device_name} sensor not found")

    temperature = read_temp(f"{sensor_path}/temp1_input")
    if temperature is None:
        raise SensorReadingError(f"{device_name} temperature could not be read")
    return {temperature_key: temperature}