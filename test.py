# coding: utf-8
from sprotoparser import *
from sprotodump import dump
import sys
import codecs

text = codecs.open(sys.argv[1], "r", "utf-8").read()
sp = parse(text, "=text")

import json
print(json.dumps(sp, indent=4))

dump(sp, "test.spb")
