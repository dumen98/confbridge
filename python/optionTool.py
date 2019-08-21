#!/usr/bin/python3

import os
import sys
import json
import shutil
import tempfile

class Option:
    def __init__(self,confNum):
        self.optionFilePath = getDefaultPath(confNum)
        if fileExists(confNum) is False:
            createDefaultFile(confNum)
            self.optionFilePath = getDefaultPath(confNum)
            print("Config file not exits, create default config file")
        with open(self.optionFilePath,'r') as of:
            options = json.load(of)
        self.basic = options["Basic"]
        self.userOption = options["UserOption"]
        self.bridgeOption = options["BridgeOption"] 

def getDefaultPath(confNum):
    defaultPath = os.path.join(os.path.split(os.path.realpath(__file__))[0],
                                                "confbridgeConf_%s.json" % confNum)
    return defaultPath
    
def fileExists(confNum):
    filePath = getDefaultPath(confNum)
    return os.path.exists(filePath)

def createDefaultFile(confNum):
    defaultPath = getDefaultPath(confNum)
    tempFile = tempfile.mktemp()
    tf = open(tempFile,'w')
    tf.write("""{
    "Basic": {
        "Context": "script-test",
        "Name": "OpenVox",
        "Admin": [],
        "AdminPin": "",
        "Marked": [],
        "UserPin": "",
        "Wait_For_Admin": false,
        "ASTERISK_SPOOL_DIR": "/var/spool/asterisk/outgoing/"
        }, 
    "UserOption":{
        "music_on_hold_when_empty": "yes",
        "announce_only_user": "yes",
        "dsp_talking_threshold": 160,
        "dsp_silence_threshold": 2500
        }, 
    "BridgeOption":{
        "mixing_interval": 20
        }
}
""")
    tf.flush()
    tf.close()
    shutil.move(tempFile,defaultPath)
    return tempFile
