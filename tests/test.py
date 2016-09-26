#!/usr/bin/env python
print "Linchpin Testing Initiating..."

print "Testing Linchpin TestClass: TestLinchpinInvocation" 
from TestLinchPinInvocation import TestLinchPinInvocation

print "Testing Linchpin TestClass: TestLinchpinCredentials"
from TestLinchPinCredentials import TestLinchPinCredentials

print "Testing Linchpin TestClass: TestLinchpinEnv"
from TestLinchPinEnv import TestLinchPinEnv

import nose
nose.run()
