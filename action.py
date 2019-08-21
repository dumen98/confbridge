#!/usr/bin/python3

import os
import sys
import time
import json
from asterisk.ami import AMIClient,AMIClientAdapter,EventListener

import optionTool

channel = ""
canfName = ""
def getChannel(event,**kwargs):
    global channel,canfName
    channel = event.keys["Channel"]
    print(channel)

def main(client,number,command):
    global channel
    def actionMute():
        result = adapter.ConfbridgeMute(
            Conference=confName,
            Channel="%s" % channel
        )
        print(result.response)
    def actionUnmute():
        result = adapter.ConfbridgeUnmute(
            Conference=confName,
            Channel="%s" % channel
        )
        print(result.response)
    def actionKick():
        #print(channel)
        result = adapter.ConfbridgeKick(
            Conference=confName,
            Channel="%s" % channel
        )
        print(result.response)
    def actionLock():
        result = adapter.ConfbridgeLock(
            Conference=confName,
        )
        print(result.response)
    def actionUnlock():
        result = adapter.ConfbridgeUnlock(
            Conference=confName,
        )
        print(result.response)
    def actionStartRecord():
        result = adapter.ConfbridgeStartRecord(
            Conference=confName,
            Channel="%s" % channel
        )
        print(result.response)
        #the record file should be /var/spool/asterisk/monitor/confbridge-confName-queId.wav
    def actionStopRecord():
        result = adapter.ConfbridgeStopRecord(
            Conference=confName,
            Channel="%s" % channel
        )
        print(result.response)
    command_option = {
        "mute":actionMute,
        "unmute":actionUnmute,
        "kick":actionKick,
        "lock":actionLock,
        "unlock":actionUnlock,
        "startRecord":actionStartRecord,
        "stopRecord":actionStopRecord
        }
    adapter = AMIClientAdapter(client)
    result = adapter.ConfbridgeList(Conference=confName)
    future = result.response
    time.sleep(0.01)
    command_option[command]()



if __name__ == '__main__':
    #init ami client
    client = AMIClient(address='127.0.0.1',port=5038)
    client.login(username='for-confbridge',secret='for-confbridge')
    #get vars
    confNum = sys.argv[1]
    command = sys.argv[2]
    numbers = []
    if len(sys.argv) == 4:
        number = sys.argv[3]
        numbers = number.split(',')
    else:
        numbers.append(confNum)
    adapter = AMIClientAdapter(client)
    options = optionTool.Option(confNum)
    confName = options.basic["Name"]
    
    #print(future)
    for num in numbers:
        #get channel from event
        event = EventListener(getChannel, white_list=['ConfbridgeList'],CallerIDNum=num)
        client.add_event_listener(event)
        #call main
        main(client,num,command)
        client.remove_event_listener(event)
