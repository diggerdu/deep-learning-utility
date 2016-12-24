import gc
import os
import psutil
import time

proc = psutil.Process(os.getpid())
gc.collect()
mem0 = proc.memory_info().rss

# create approx. 10**7 int objects and pointers
foo = ['abc' for x in range(10**7)]
mem1 = proc.memory_info().rss


start = time.time()

# unreference, including x == 9999999
#del foo, x
foo = None
x = None
mem2 = proc.memory_info().rss
print  (time.time()-start)
# collect() calls PyInt_ClearFreeList()
# or use ctypes: pythonapi.PyInt_ClearFreeList()
gc.collect()
mem3 = proc.memory_info().rss

pd = lambda x2, x1: 100.0 * (x2 - x1) / mem0
print "Allocation: %0.2f%%" % pd(mem1, mem0)
print "Unreference: %0.2f%%" % pd(mem2, mem1)
print "Collect: %0.2f%%" % pd(mem3, mem2)
print "Overall: %0.2f%%" % pd(mem3, mem0)

