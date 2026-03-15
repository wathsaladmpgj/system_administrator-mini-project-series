#!/bin/bash

LOG="/home/ubuntu/patch-management/logs/patch.log"

echo "===== Patch Job Started =====" >> $LOG
date >> $LOG

# Update repository info
sudo apt-get update > /dev/null

# Check if updates exist
UPDATES=$(apt-get -s upgrade | grep -P '^\d+ upgraded')

echo "Checking updates: $(date)" >> $LOG

if [[ $UPDATES != "0 upgraded"* ]]; then

    echo "Updates available. Installing patches..." >> $LOG
    
    sudo apt-get upgrade -y >> $LOG
    
    echo "Updates installed successfully: $(date)" >> $LOG

else

    echo "No updates available. Skipping patch installation." >> $LOG

fi

echo "===== Patch Job Completed =====" >> $LOG
echo "" >> $LOG