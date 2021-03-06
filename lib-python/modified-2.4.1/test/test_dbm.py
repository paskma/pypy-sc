#! /usr/bin/env python
"""Test script for the dbm module
   Roger E. Masse
"""
import os
import random
import dbm
from dbm import error
from test.test_support import verbose, verify, TestSkipped

# make filename unique to allow multiple concurrent tests
# and to minimize the likelihood of a problem from an old file
filename = '/tmp/delete_me_' + str(random.random())[-6:]

def cleanup():
    for suffix in ['', '.pag', '.dir', '.db']:
        try:
            os.unlink(filename + suffix)
        except OSError, (errno, strerror):
            # if we can't delete the file because of permissions,
            # nothing will work, so skip the test
            if errno == 1:
                raise TestSkipped, 'unable to remove: ' + filename + suffix

def test_keys():
    d = dbm.open(filename, 'c')
    verify(d.keys() == [])
    d['a'] = 'b'
    d['12345678910'] = '019237410982340912840198242'
    verify(d.keys() == ['12345678910', 'a'])
    verify(d.get('a') == 'b')
    verify(d.get('b', None) == None)
    try:
        d.get('b')
    except KeyError, e:
        pass
    try:
        d['b']
    except KeyError,e :
        pass

    if d.has_key('a'):
        if verbose:
            print 'Test dbm keys: ', d.keys()

    d.close()
    try:
        d.keys()
    except dbm.error:
        pass

def test_modes():
    d = dbm.open(filename, 'r')
    d.close()
    d = dbm.open(filename, 'rw')
    d.close()
    d = dbm.open(filename, 'w')
    d.close()
    d = dbm.open(filename, 'n')
    d.close()

cleanup()
try:
    test_keys()
    test_modes()
except:
    cleanup()
    raise

cleanup()
