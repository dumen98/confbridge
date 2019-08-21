#!/bin/bash

confName=$1
curl -s -c cookie.tmp "http://127.0.0.1:8088/rawman?Action=Login&Username=for-confbridge&Secret=for-confbridge"
#channel=${`curl -v --digest -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeList&Conference=$1"` > grep SIP/$2}
curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeList&Conference=$confName" > confbridgeList.tmp 
echo > result.tmp

case $2 in
    mute)
        echo mute $3
        numbers=(${3//,/ })
        for num in ${numbers[@]};
        do
            channel=`cat confbridgeList.tmp|grep Channel:\ SIP/$num`
            channel=${channel##Channel: }
            curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeMute&Conference=$confName&Channel=${channel%?}" > result.tmp
        done
        ;;
    unmute)
        echo unmute $3
        numbers=(${3//,/ })
        for num in ${numbers[@]};
        do
            channel=`cat confbridgeList.tmp|grep Channel:\ SIP/$num`
            channel=${channel##Channel: }
            curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeUnmute&Conference=$confName&Channel=${channel%?}" > result.tmp
        done
        ;;
    kick)
        echo unmute $3
        numbers=(${3//,/ })
        for num in ${numbers[@]};
        do
            channel=`cat confbridgeList.tmp|grep Channel:\ SIP/$num`
            channel=${channel##Channel: }
            curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeKick&Conference=$confName&Channel=${channel%?}" > result.tmp
        done
        ;;
    lock)
        echo lock $confName
        curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeLock&Conference=$confName" > result.tmp
        ;;
    unlock)
        echo unlock $confName 
        curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeUnlock&Conference=$confName" > result.tmp
        ;;
    startRecord)
        echo start record $confName
        curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeStartRecord&Conference=$confName" > result.tmp
        ;;
    stopRecord)
        echo start record $confName
        curl -b @cookie.tmp "http://127.0.0.1:8088/rawman?Action=ConfbridgeStopRecord&Conference=$confName" > result.tmp
        ;;
esac
rm *.tmp -f

