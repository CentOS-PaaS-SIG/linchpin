#!/usr/bin/env python


def format_rules(rules, rule_type):
    rules_output = []
    for rule in rules:
        if rule["rule_type"] == rule_type:
            rule_output = {}
            rule_output['from_port'] = rule['from_port']
            rule_output['to_port'] = rule['to_port']
            rule_output['cidr_ip'] = rule['cidr_ip']
            rule_output['proto'] = rule['proto']
            rules_output.append(rule_output)
    return rules_output


class FilterModule(object):
    ''' A filter to format AWS EC2 security group rules '''
    def filters(self):
        return {
            'aws_sg_rules': format_rules
        }
