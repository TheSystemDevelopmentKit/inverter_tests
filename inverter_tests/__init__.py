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
from  inverter_testbench import *

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

    def init(self):
        pass #Currently nothing to add

    def parallel(self):
        '''Runs parallel simulation

        '''
        tb=inverter_testbench()
        tb.models=['py','sv','vhdl','eldo','spectre']
        tb.configuration='parallel'
        tb.run()

    def serial(self):
        '''Runs parallel simulation

        '''
        tb=inverter_testbench()
        tb.models=['py','sv','vhdl','eldo','spectre']
        tb.configuration='serial'
        tb.run()

    def all(self):
        '''Runs both parallel and serial simulation, executed in parallel

        '''
        tb1=inverter_testbench()
        tb1.models=['py','sv','vhdl','eldo','spectre']
        tb1.configuration='parallel'
        tb2=inverter_testbench()
        tb2.models=['py','sv','vhdl','eldo','spectre']
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
    import pdb
    from inverter_tests import *
    
    # Implement argument parser. See configure and Makefile for how it is used.
    parser = argparse.ArgumentParser(description='Parse selectors')
    parser.add_argument('--test', dest='test', type=str, nargs='?', const = True, 
            default='all' ,help='Test to execute all | serial | parallel')
    args=parser.parse_args()

    tests=inverter_tests()
    print(args.test)
    pdb.set_trace()
    tests.test=args.test
    tests.run()

