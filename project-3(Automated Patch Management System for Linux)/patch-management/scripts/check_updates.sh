#!/bin/bash

LOG="../logs/patch.log"

echo "Checking updates: $(date)" >> $LOG

apt-get list --upgradable >> $LOG