from __future__ import print_function
import os
import json
import sys

output_path = sys.argv[-1]
print(output_path)
try:
    workspace = os.listdir(".")
    print("output to stderr: {0}".format(json.dumps(workspace)))
    out = open(output_path, 'w')
    out.write(json.dumps(workspace))
    out.close()
except OSError as e:
    print(e)
