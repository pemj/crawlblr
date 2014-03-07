#!/usr/bin/python3
import subprocess
import re

output, error= subprocess.Popen(["ls"], stdout=subprocess.PIPE).communicate()
filePattern = re.compile('^[a-z0-9A-Z_]+(\.db)+$')
li = [x.decode('utf-8') for x in output.split(b'\n')]
dbFiles = [x for x in li if filePattern.match(x)]

print(dbFiles)
