from __future__ import print_function
import os
import json
import sys

workspace = os.listdir(".")

print("output to stderr: {0}".format(json.dumps(workspace)))
print(json.dumps(workspace), file=sys.stderr)

