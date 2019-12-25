#!/usr/bin/env python
from string import digits, ascii_letters

def cpu_to_int(cpu):
    amount = ''.join(c for c in cpu if c in digits)
    amount = float(amount)
    size = ''.join(c for c in cpu if c in ascii_letters)
    if size == 'm':
        amount = amount / 1000
    return amount

class FilterModule(object):
    ''' A filter to add_res_data '''
    def filters(self):
        return {
            'cpu_to_int': cpu_to_int
        }
