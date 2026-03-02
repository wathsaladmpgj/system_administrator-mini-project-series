import psutil
import shutil
import datetime
import sys
import json
import os

log_file = "/home/ubuntu/cron-framework/logs/health_log.json"
os.makedirs("/home/ubuntu/cron-framework/logs", exist_ok=True)

try:
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = shutil.disk_usage("/").used / shutil.disk_usage("/").total * 100

    data = {
        "timestamp": str(datetime.datetime.now()),
        "cpu_percent": cpu,
        "memory_percent": memory,
        "disk_percent": disk,
    }

    if disk > 80:
        data["status"] = "FAILED"
        exit_code = 1
    else:
        data["status"] = "SUCCESS"
        exit_code = 0

except Exception as e:
    data = {
        "timestamp": str(datetime.datetime.now()),
        "status": "ERROR",
        "error": str(e)
    }
    exit_code = 1

with open(log_file, "a") as f:
    f.write(json.dumps(data) + "\n")

sys.exit(exit_code)