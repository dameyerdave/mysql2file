#!/usr/bin/env python

### Description
# mysql2file is a script to query a mysql database and write the 
# results into a file. You need a cursor row mostly the id column
# in addition to a timestamp row that is used as the timestamp of
# the "event". The log output is leaned to the syslog format.

### Hints
# To run the script on a regular basis please use cron.

### Information
# Version : 1.0
# Author  : David Meyer
# Date    : 2018-09-19    

import MySQLdb
import sys, os
import configparser
import socket
from datetime import datetime as dt 

sys.path.append(os.path.dirname(__file__) + '/lib')
from pwhelper import PWHelper

configfile = os.path.dirname(__file__) + '/mysql2file.cfg'
cursorfile = os.path.dirname(__file__) + '/.cursor'

config = configparser.ConfigParser()
config.read(configfile)
host = socket.gethostname()
proc = config['Logging']['Proc']
timeformat = config['Database']['TimeFormat']

db = MySQLdb.connect(
        host=config['Database']['Host'], 
        user=config['Database']['User'], 
        passwd=PWHelper.decode(config['Database']['Password']), 
        db=config['Database']['Name'])

with open(config['Logging']['File'], "a") as logfile:
    cur = db.cursor()
    cursorval = '0'
    if os.path.isfile(cursorfile):
        with open(cursorfile, "r") as curfile:
            cursorval = curfile.read()
    query = config['Database']['Query'].replace('_C_', cursorval)
    cur.execute(query)

    fields = [desc[0] for desc in cur.description]
    for curcol in range(0, len(fields)):
        if fields[curcol] == config['Database']['CursorCol']:
            break
    for timecol in range(0, len(fields)):
        if fields[timecol] == config['Database']['TimeCol']:
            break
    for row in cur.fetchall():
        ts = dt.strptime(str(row[timecol]), timeformat)
        logfile.write(ts.isoformat() + ' ')
        logfile.write(host + ' ')
        logfile.write(proc + '[0]: ')
        for col in range(0, len(row)):
            logfile.write(fields[col] + '=' + str(row[col]))
            if col < (len(row) - 1):
                logfile.write(", ")
        logfile.write("\n")
        cursorval = row[curcol]
    with open(cursorfile, "w") as curfile:
        curfile.write(str(cursorval))
    db.close()
