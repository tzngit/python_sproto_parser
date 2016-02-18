# coding: utf-8
from sprotoparser import *
import sys

text = open(sys.argv[1], "r").read()
sp = parse(text)

import json
print(json.dumps(sp, indent=4))
