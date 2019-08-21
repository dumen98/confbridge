#!/usr/bin/bash

time=$1
dayOfWeek=$2
dayOfMonth=$3
args=$4

scriptShell=/root/script/confbridge/shell/invite.sh
scriptPython=/root/script/confbridge/invite.py

times=${time//:/ }
if [ "$dayOfWeek" -eq "0" ]; then
    dayOfWeek="*"
else
    dayOfWeek="*/"$dayOfWeek
fi
if [ "$dayOfMonth" -eq "0" ]; then
    dayOfMonth="*"
else
    dayOfMonth="*/"$dayOfMonth
fi

arr_args=(${args})
count=${#arr_args[@]}
if [ $count -eq 3 ]; then
    echo "$times $dayOfMonth * $dayOfWeek $scriptPython $args > /dev/null 2>&1" >> /var/spool/cron/$USER
elif [ $count -eq 4]; then
    echo "$times $dayOfMonth * $dayOfWeek $scriptShell $args > /dev/null 2>&1" >> /var/spool/cron/$USER 
fi
