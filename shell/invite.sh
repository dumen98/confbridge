#!/usr/bin/bash

ASTERISK_SPOOL_DIR=/var/spool/asterisk/outgoing/
time=$4
date=$5

numbers=(${3//,/ })
for num in "${numbers[@]}";
do
CALLOUT_TEMPLATE="
Channel: SIP/$num
Extension: $2
Context: conferences-join
Priority: 1
CallerID: $1 <$2>
MaxRetries: 0
RetryTime: 15
WaitTime: 300
Set: participant_number=$num
Set: conf_number=$2
Set: conf_name=$1
"
echo "$CALLOUT_TEMPLATE" > .tmp
if [ -n "$time" ]; then
    if [ -n "$date" ];then
        datetime=$time" "${date//\//-}
    else
        datetime=$time
    fi
    touch -d "$datetime" .tmp
fi
mv .tmp $ASTERISK_SPOOL_DIR$2.$num
done


