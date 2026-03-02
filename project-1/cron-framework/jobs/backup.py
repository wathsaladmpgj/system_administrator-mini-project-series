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