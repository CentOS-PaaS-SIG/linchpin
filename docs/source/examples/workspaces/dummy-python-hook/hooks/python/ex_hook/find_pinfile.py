from __future__ import print_function
import sys
import json


prev_hooks = sys.argv[-1]
print("input: {0}".format(prev_hooks))

prev_hooks = json.loads(prev_hooks)


# return successfully if the PinFile is in the list of files
for hook in prev_hooks:
    if type(hook['data']) is list and 'PinFile' in hook['data']:
        print('found PinFile')
        sys.exit(0)

error = {'error': 'could not find \'PinFile\'', 'files': files}
print(error, file=sys.stderr)
sys.exit(1)
