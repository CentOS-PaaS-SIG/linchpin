#!/usr/bin/env python


def map_results(results, attr, subattr):
    output = []
    print("Inside filter")
    print(attr)
    print(subattr)
    print("results")
    print(results)
    for task_result in results:
        output.append(task_result[attr][subattr])
    print("Output")
    print(output)
    return output


class FilterModule(object):
    ''' A filter to fix network format '''
    def filters(self):
        return {
            'map_results': map_results
        }
