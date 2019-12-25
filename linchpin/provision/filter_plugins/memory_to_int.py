#!/usr/bin/env python
from string import digits, ascii_letters

def memory_to_int(memory):
    amount = ''.join(c for c in memory if c in digits)
    amount = int(amount)
    size = ''.join(c for c in memory if c in ascii_letters)
    if size == 'Gi':
        amount = amount * 1000
    return amount

class FilterModule(object):
    ''' A filter to add_res_data '''
    def filters(self):
        return {
            'memory_to_int': memory_to_int
        }
