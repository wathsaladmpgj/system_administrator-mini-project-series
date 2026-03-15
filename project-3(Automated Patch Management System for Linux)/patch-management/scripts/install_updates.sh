#!/bin/bash

LOG="/home/ubuntu/patch-management/logs/patch.log"

echo "Checking updates: $(date)" >> $LOG

sudo apt-get update >> $LOG
sudo apt-get -s upgrade >> $LOG