#!/usr/bin/python3

import os
import sys
import tempfile
import shutil
import json
from asterisk.agi import *

import optionTool

def main(agi,confnum, number,options):
    #load config file value
    basic = options.basic
    userOption = options.userOption
    bridgeOption = options.bridgeOption
    adminList = basic.get("Admin",list())
    markedList = basic.get("Marked",list())
    conf_name = basic.get("Name",'')
    conf_menu = basic.get("Menu",'')
    if conf_name == '':
        conf_name = confnum
    agi.set_variable("conf_name",conf_name)

    conf_number = agi.get_variable("conf_number")
    participant_number = agi.get_variable("participant_number")
    if participant_number:
        agi.set_variable("CALLERID(num)",participant_number)
    
    adminFlag = False
    if number in adminList:
        adminFlag = True
        agi.verbose(adminFlag)
        agi.set_variable("CONFBRIDGE(user,admin)","yes")
        agi.set_variable("CONFBRIDGE(user,marked)","yes")
        if basic["AdminPin"] != '':
            agi.set_variable("CONFBRIDGE(user,pin)",basic["AdminPin"])
    elif number in markedList:
        agi.set_variable("CONFBRIDGE(user,marked)","yes")
    if not adminFlag:
        if basic.get("Wait_For_Admin",False):
            agi.set_variable("CONFBRIDGE(user,wait_marked)","yes")
        if basic["UserPin"] != '':
            agi.set_variable("CONFBRIDGE(user,pin)",basic["UserPin"])

    for option,value in userOption.items():
        agi.set_variable("CONFBRIDGE(user,%s)" % option,value)
    for option,value in bridgeOption.items():
        agi.set_variable("CONFBRIDGE(bridge,%s)" % option,value)
    
    agi.appexec("CONFBRIDGE",options=",".join([conf_name,"","",conf_menu]))

if __name__ == '__main__':
    #init agi
    try:
        agi = AGI()
        #get vars
        confNum = agi.get_variable("EXTEN")
        number = agi.get_variable("participant_number")
        if optionTool.fileExists(confNum):
            #if the file exists, call main, otherwise it should be done, not creating file
            options = optionTool.Option(confNum)
            main(agi,confNum,number,options)
        #else:
            #optionTool.createDefaultFile(confNum)
    except AGIError:
        #this happened when the user hangup
        pass
