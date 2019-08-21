#!/usr/bin/python3

import os
import sys
import tempfile
import shutil
import json
from time import mktime,strptime,strftime,localtime

import optionTool

def main(confnum, number,options,time,date):
    basic = options.basic
    #create call file
    tempFile = tempfile.mktemp()
    f = open(tempFile, mode='w')
    CALLOUT_TEMPLATE = """Channel: SIP/%(number)s
Context: %(context)s
Extension: %(confnum)s
Priority: 1
CallerID: %(confname)s <%(confnum)s>
MaxRetries: 0
RetryTime: 15
WaitTime: 300
Set: participant_number=%(number)s
Set: conf_number=%(confnum)s
Set: conf_name=%(confname)s
"""
    ASTERISK_SPOOL_DIR = basic["ASTERISK_SPOOL_DIR"]
    f.write(CALLOUT_TEMPLATE % {'number': number,
								'context': basic["Context"],
                                'confname': basic["Name"],
                                'confnum': confnum})
                                    
    f.write('\n')

    f.flush()
    f.close()
    #end create
    #set time
    if time:
        if time.count(":") == 1:
            time += ":00"
        timestamp = ""
        if date:
            #times = time.split(":")
            #dates = date.split("-")
            #datetimes = dates + times
            #datetime = " ".join(datetimes)
            date = date.replace(r"/","-")
            datetime = " ".join((date,time))
            timestamp = mktime(strptime(datetime,"%Y-%m-%d %H:%M:%S"))
        else:
            datetime = " ".join((strftime("%Y-%m-%d",localtime()),time))
            timestamp = mktime(strptime(datetime,"%Y-%m-%d %H:%M:%S"))
        os.utime(tempFile,(timestamp,timestamp))
    #end set time

    '''
    #for ssh asterisk,copy from astconfman. if you need it, change it yourself
    if config['ASTERISK_SSH_ENABLED']:
        ssh_cmd_prefix = 'ssh -p%s %s@%s "%%s"' % (config['ASTERISK_SSH_PORT'],
                                             config['ASTERISK_SSH_USER'],
                                             config['ASTERISK_SSH_HOST'])
        scp_cmd_prefix = 'scp -P%s %%s %s@%s:%%s' % (config['ASTERISK_SSH_PORT'],
                                             config['ASTERISK_SSH_USER'],
                                             config['ASTERISK_SSH_HOST'])
        remote_tmp_file = commands.getoutput(ssh_cmd_prefix % 'mktemp')
        scp_tmp_file = commands.getoutput(scp_cmd_prefix % (tempname,
                                                            remote_tmp_file))
        commands.getoutput(ssh_cmd_prefix % 'mv %s %s' % (remote_tmp_file,
                                                config['ASTERISK_SPOOL_DIR']))
    else:
        # Move it to Asterisk outgoing calls queue.
        try:
            shutil.move(tempname, os.path.join(
                config['ASTERISK_SPOOL_DIR'],
                        '%s.%s' % (confnum, number)))
            raise OSError
        except OSError:
            # This happends that Asterisk immediately deleted call file
			pass
    '''
    #move file
    try:
        shutil.move(tempFile, os.path.join(
            ASTERISK_SPOOL_DIR,
                    '%s.%s' % (confnum, number)))
        raise OSError
    except OSError:
        # This happends that Asterisk immediately deleted call file
        pass

if __name__ == '__main__':
    #load argvs from command
    confNum = sys.argv[1]
    number = sys.argv[2]
    numbers = number.split(',')
    time = None
    date = None
    if len(sys.argv) == 4:
        time = sys.argv[3]
    elif len(sys.argv) == 5:
        time = sys.argv[3]
        date = sys.argv[4]
    if not optionTool.fileExists(confNum):
        optionTool.createDefaultFile(confNum)
    options = optionTool.Option(confNum)
    for num in numbers:
        #call main
        main(confNum,num,options,time,date)
