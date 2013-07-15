#!/usr/bin/env python
import subprocess
import sys
import os
currentDir = os.path.dirname(os.path.realpath(__file__))

# input comes from stdin
for line in sys.stdin:

    line = line.strip()
    print line

    out = subprocess.Popen('python sqlmap.py --flush-session --batch --passwords -u "%s"' % line, cwd = currentDir, shell=True, stdin = subprocess.PIPE, stdout = subprocess.PIPE).communicate()[0]

    f = open('sqlmap-out', 'a')
    f.write(out)
    f.close()
    print out
