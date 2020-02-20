from __future__ import print_function
import sys
import json


prev_hooks = sys.argv[-2]
pipe_path = sys.argv[-1]
print("input: {0}".format(prev_hooks))

prev_hooks = json.loads(prev_hooks)
respipe = open(pipe_path, 'w')

# return successfully if the PinFile is in the list of files
for hook in prev_hooks:
    print(hook['data'])
    if type(hook['data']) is list and 'PinFile' in hook['data']:
        print('Found PinFile')
        sys.exit(0)

error = {'error': 'could not find \'PinFile\''}
print(error, file=respipe)
sys.exit(1)
