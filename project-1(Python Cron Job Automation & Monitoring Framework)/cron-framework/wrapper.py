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