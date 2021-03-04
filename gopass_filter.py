#!/usr/bin/env python

import os
import sys
import logging
import subprocess
import json
import re

logging.basicConfig(filename='/tmp/gopassalfred.log', level=logging.DEBUG)
logging.debug('Debug log started, called with {}'.format(sys.argv))

my_env = os.environ.copy()
my_env['PATH'] = '/opt/homebrew/bin:{}'.format(my_env['PATH'])

process = subprocess.Popen(['/opt/homebrew/bin/gopass', 'list', '-f'], stdout=subprocess.PIPE, env=my_env)
stdout, stderr = process.communicate()

outlist = [
    {
        "uid": result,
        "title": result.split('/')[-1],
        "subtitle": '/'.join(result.split('/')[:-1]),
        "arg": result,
        "match": " ".join(set(re.split('[. /\-]', result))) + ' ' + result,
        "autocomplete": result
    } for result in stdout.decode('utf8').splitlines()
]

print(json.dumps({'items': outlist}))