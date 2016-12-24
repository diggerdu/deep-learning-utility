from DataIO import *

testObject = DataIter('test/')

for i in xrange(10000):
    print testObject.next_batch().shape
