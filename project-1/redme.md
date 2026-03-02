# Python Cron Job Automation & Monitoring Framework

## Step 1 — Install Python and pip

```text
sudo apt install python3 python3-venv python3-pip -y
```

- `python3-venv` → needed for virtual environments
- `pip3` → for Python packages

## Step 2 — Create Project Structure

```text
mkdir -p ~/cron-framework/{jobs,logs}
cd ~/cron-framework
```
- folder will look like:
```text
cron-framework/
    jobs/   # Python job scripts
    logs/   # Log files
    wrapper.py   # Monitoring wrapper
```

## Step 3 — Create Virtual Environment

```text
python3 -m venv venv
source venv/bin/activate
```
- Now your prompt should start with (venv)
- All Python packages installed now will stay inside this environment

## Step 4 — Install Dependencies

```text
pip install psutil
```
- `psutil` → CPU, memory, disk stats

## Step 5 — Create Health Check Python Job

```text
jobs/health_check.py
```
```text
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
```


## Step 6 — Create Wrapper Python Script

```text
wrapper.py
```
```text
import subprocess
import sys
import datetime

LOG_FILE = "/home/ubuntu/cron-framework/logs/wrapper.log"

def run_job(job_path):
    start_time = datetime.datetime.now()
    result = subprocess.run(["/home/ubuntu/cron-framework/venv/bin/python", job_path])
    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()

    with open(LOG_FILE, "a") as log:
        log.write(f"{start_time} | {job_path} | Exit: {result.returncode} | Duration: {duration}s\n")

    if result.returncode != 0:
        print(f"ALERT: {job_path} failed!")

if __name__ == "__main__":
    job = sys.argv[1]
    run_job(job)
```

## Step 7 — Create Backup Job

```text
jobs/backup.py
```
```text
import tarfile
import datetime
import sys
import os
import json

logs_dir = "/home/ubuntu/cron-framework/logs"
os.makedirs(logs_dir, exist_ok=True)
log_file = f"{logs_dir}/backup_log.json"

backup_name = f"/tmp/etc_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M')}.tar.gz"

try:
    def safe_add(tar, path):
        try:
            tar.add(path)
        except PermissionError:
            pass  # skip locked files

    with tarfile.open(backup_name, "w:gz") as tar:
        for item in os.listdir("/etc"):
            full_path = os.path.join("/etc", item)
            safe_add(tar, full_path)

    data = {"timestamp": str(datetime.datetime.now()), "backup_file": backup_name, "status": "SUCCESS"}
    exit_code = 0

except Exception as e:
    data = {"timestamp": str(datetime.datetime.now()), "status": "ERROR", "error": str(e)}
    exit_code = 1

with open(log_file, "a") as f:
    f.write(json.dumps(data) + "\n")

sys.exit(exit_code)
```
