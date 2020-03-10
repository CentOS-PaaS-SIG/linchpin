#!/usr/bin/env python
import linchpin.FilterUtils.FilterUtils as filter_utils


class FilterModule(object):
    ''' A filter to fetch jobids from topology outputs '''
    def filters(self):
        return {
            'fetch_beaker_job_ids': filter_utils.fetch_beaker_job_ids
        }
