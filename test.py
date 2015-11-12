# coding: utf-8
from sprotoparser import *

text = open("test.sproto", "r").read()
sp = parse(text)

import json
print(json.dumps(sp, indent=4))
