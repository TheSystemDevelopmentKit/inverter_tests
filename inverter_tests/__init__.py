"""
==============
Inverter tests
==============

Inverter tests class to demostrate how to create various tests with a testbench.
There are not that many parameters to change in this example, but the idea is this:

Generate a set of test cases that verifies your chip, and enable their execution so that you do 
not need to alter the parameters.

Initially written by Marko Kosunen, marko.kosunen@aalto.fi, 2022

"""

import os
import sys
if not (os.path.abspath('../../thesdk') in sys.path):
    sys.path.append(os.path.abspath('../../thesdk'))

from thesdk import *
from inverter_testbench import *

import numpy as np

class inverter_tests(thesdk):
    @property
    def _classfile(self):
        return os.path.dirname(os.path.realpath(__file__)) + "/"+__name__

    def __init__(self,*arg): 
        self.print_log(type='I', msg='Inititalizing %s' %(__name__)) 
        self.Rs =  100e6;            # Sampling frequency
        self.model='py';             # Can be set externally, but is not propagated
        self.par= False              # By default, no parallel processing
        self.queue= []               # By default, no parallel processing

        self.test = 'all'

        if len(arg)>=1:
            parent=arg[0]
            self.copy_propval(parent,self.proplist)
            self.parent =parent;

        self.init()

    @property
    def tools(self):
        if not hasattr(self,'_tools'):
            self._tools = 'open'
        return self._tools
    @tools.setter
    def tools(self,value):
            self._tools = value

    def init(self):
        pass #Currently nothing to add

    def parallel(self):
        '''Runs parallel simulation

        '''
        tb=inverter_testbench()
        if self.tools == 'open':
            tb.models=['py','icarus', 'ghdl', 'ngspice']
        elif self.tools == 'proprietary':
            tb.models=['sv']
        tb.configuration='parallel'
        tb.run()

    def serial(self):
        '''Runs parallel simulation

        '''
        tb=inverter_testbench()
        if self.tools == 'open':
            tb.models=['py','icarus', 'ghdl', 'ngspice']
        elif self.tools == 'proprietary':
            tb.models=['sv']
        tb.configuration='serial'
        tb.run()

    def all(self):
        '''Runs both parallel and serial simulation, executed in parallel

        '''
        # Firsttestbench
        tb1=inverter_testbench()
        if self.tools == 'open':
            tb1.models=['py','icarus', 'ghdl', 'ngspice']
        elif self.tools == 'proprietary':
            tb1.models=['sv']
        tb1.configuration='parallel'

        # Second testbench
        tb2=inverter_testbench()
        if self.tools == 'open':
            tb2.models=['py','icarus', 'ghdl', 'ngspice']
        elif self.tools == 'proprietary':
            tb2.models=['sv']
        tb2.configuration='serial'

        self.run_parallel(duts=[tb1, tb2], method='run')

    def run(self,*arg):
        '''Guideline: Define model depencies of executions in `run` method.

        '''
        if self.test=='all':
            self.all()
        elif self.test=='parallel':
            self.parallel()
        elif self.test=='serial':
            self.serial()
        else:
            self.print_log(type='E', msg="Test %s not defined. %(self.test)")
        self.print_log(type='I', msg="See inv*.eps figures for results")

if __name__=="__main__":
    import argparse
    from inverter_tests import *
    
    # Implement argument parser. See configure and Makefile for how it is used.
    parser = argparse.ArgumentParser(description='Parse selectors')
    parser.add_argument('--test', dest='test', type=str, nargs='?', const = True, 
            default='all' ,help='Test to execute all | serial | parallel')
    parser.add_argument('--tools', dest='tools', type=str, nargs='?', const = True, 
            default='all' ,help='Tools to use open | proprietary')
    args=parser.parse_args()

    tests=inverter_tests()
    tests.test=args.test
    tests.tools=args.tools
    tests.run()

