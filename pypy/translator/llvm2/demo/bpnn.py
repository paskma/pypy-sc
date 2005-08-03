#!/usr/bin/python
"""
    Translator Demo

    Run this file -- over regular Python! -- to analyse and type-annotate
    the functions and class defined in this module, starting from the
    entry point function demo().

    Requires Pygame.
"""
# Back-Propagation Neural Networks
# 
# Written in Python.  See http://www.python.org/
#
# Neil Schemenauer <nascheme@enme.ucalgary.ca>
#
# Modifications to the original (Armin Rigo):
#   * import random from PyPy's lib, which is Python 2.2's plain
#     Python implementation
#   * starts the Translator instead of the demo by default.

import sys
import math
import time
import os, time

# XXX the Translator needs the plain Python version of random.py:
from pypy.lib import random

PRINT_IT = False

random.seed(0)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

# Make a matrix (we could use NumPy to speed this up)
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill]*J)
    return m

class NN:
    
    def __init__(self, ni, nh, no):
        # number of input, hidden, and output nodes
        self.ni = ni + 1 # +1 for bias node
        self.nh = nh
        self.no = no

        # activations for nodes
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no
        
        # create weights
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # set them to random vaules
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-2.0, 2.0)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2.0, 2.0)

        # last change in weights for momentum   
        self.ci = makeMatrix(self.ni, self.nh)
        self.co = makeMatrix(self.nh, self.no)

    def update(self, inputs):
        if len(inputs) != self.ni-1:
            raise ValueError, 'wrong number of inputs'

        # input activations
        i = 0
        while i < self.ni-1:
            #self.ai[i] = 1.0/(1.0+math.exp(-inputs[i]))
            self.ai[i] = inputs[i]
            i += 1
            
        # hidden activations
        j = 0
        while j < self.nh:
            sum = 0.0
            i = 0
            while i < self.ni:
                sum = sum + self.ai[i] * self.wi[i][j]
                i += 1
            self.ah[j] = 1.0/(1.0+math.exp(-sum))
            j += 1
            
        # output activations
        k = 0
        while k < self.no:
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = 1.0/(1.0+math.exp(-sum))
            k += 1
            
        return self.ao[:]

    def backPropagate(self, targets, N, M):
        if len(targets) != self.no:
            raise ValueError, 'wrong number of target values'

        # calculate error terms for output
        output_deltas = [0.0] * self.no
        k = 0
        while k < self.no:
            ao = self.ao[k]
            output_deltas[k] = ao*(1-ao)*(targets[k]-ao)
            k += 1

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.nh
        j = 0
        while j < self.nh:
            sum = 0.0
            k = 0
            while k < self.no:
                sum = sum + output_deltas[k]*self.wo[j][k]
                k += 1
            hidden_deltas[j] = self.ah[j]*(1-self.ah[j])*sum
            j += 1
            
        # update output weights
        j = 0
        while j < self.nh:
            k = 0
            while k < self.no:
                change = output_deltas[k]*self.ah[j]
                self.wo[j][k] = self.wo[j][k] + N*change + M*self.co[j][k]
                self.co[j][k] = change
                k += 1
            j += 1
                #print N*change, M*self.co[j][k]

        # update input weights
        i = 0
        while i < self.ni:
            j = 0
            while j < self.nh:
                change = hidden_deltas[j]*self.ai[i]
                self.wi[i][j] = self.wi[i][j] + N*change + M*self.ci[i][j]
                self.ci[i][j] = change
                j += 1
            i += 1
            
        # calculate error
        error = 0.0
        k = 0
        while k < len(targets):
            error = error + 0.5*(targets[k]-self.ao[k])**2
            k += 1
        return error


    def xtest(self, patterns):
        for p in patterns:
            #if PRINT_IT:
            os.write(1, "[%d, %d] '->' " % (p[0][0], p[0][1]))
            for ii in self.update(p[0]):
                os.write(1, "%d " % int(ii * 1000))
            os.write(1, " \n")
            
    def weights(self):
        if PRINT_IT:
            print 'Input weights:'
            for i in range(self.ni):
                print self.wi[i]
            print
            print 'Output weights:'
            for j in range(self.nh):
                print self.wo[j]

    def train(self, patterns, iterations=2000, N=0.5, M=0.1):
        # N: learning rate
        # M: momentum factor
        i = 0
        while i < iterations:
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
            if PRINT_IT and i % 100 == 0:
                print 'error %f' % error
            i += 1

def demo():
    # Teach network XOR function
    pat = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and two output nodes
    n = NN(2, 3, 1)
    # train it with some patterns
    n.train(pat, 2000)
    # test it
    n.xtest(pat)
    return 0
#_________________________________________________________

from pypy.translator.llvm2.genllvm import compile_function
import py

def test_demo():
    py.log.setconsumer("genllvm", py.log.STDOUT)
    py.log.setconsumer("genllvm database prepare", None)
    f = compile_function(demo, [])

    print 'Running...'
    T = time.time()
    for i in range(10):
        f()
    t1 = time.time() - T
    print "that took", t1

    T = time.time()
    for i in range(10):
        demo()
    t2 = time.time() - T
    print "compared to", t2
    print "a speed-up of", t2/t1
    
def main():
    T = time.time()
    os.write(1, 'Running...\n')

    for i in range(50):
        demo()

    t1 = time.time() - T
    os.write(1, 'That took... %d msecs \n' % int(t1 * 1000))
    return 0
    
if __name__ == "__main__":
    from pypy.translator.llvm2.genllvm import compile_function
    import py

    import sys
    compile_llvm = True
    if len(sys.argv) > 1:
        if sys.argv[1] == "p":
            main()
            compile_llvm = False
        elif sys.argv[1] == "c":

            from pypy.translator.translator import Translator
            t = Translator(main)    
            a = t.annotate([])            
            t.specialize()    
            f = t.ccompile()
            f()

            compile_llvm = False

    if compile_llvm:
        compile_function(main, [])    

        # run with the following command
        "llvmc -Tasm=-enable-correct-eh-support -v -L /usr/lib/ -lm -lgc main_optimized.bc -o go"
