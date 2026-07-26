from fastapi import FastAPI

app = FastAPI(title="Steam Sidekick API")


def read_temp(path):
    try:
        with open(path, "r") as f:
            return round(int(f.read().strip()) / 1000, 1)
    except Exception:
        return None


@app.get("/")
def root():
    return {
        "cpu": {
            "temperature": read_temp("/sys/class/hwmon/hwmon1/temp1_input")
        },
        "gpu": {
            "edge": read_temp("/sys/class/drm/card1/device/hwmon/hwmon5/temp1_input"),
            "junction": read_temp("/sys/class/drm/card1/device/hwmon/hwmon5/temp2_input"),
            "memory": read_temp("/sys/class/drm/card1/device/hwmon/hwmon5/temp3_input")
        }
    }
