##################################
#   Author:diggerdu
#   Name:DataIter.py
#
#
#
#
##################################

import os
import gc
from multiprocessing import Process
from Queue import Queue
import numpy as np


class DataIter(object):
    def __init__(self, data_path, max_iters=512, batch_size=128, life=59):
        self.life = life
        self.batch_size = batch_size
        self.data_path = data_path
        self.file_list = [data_path + f for f in \
                os.listdir(data_path) \
                if f.endswith('.npy')]
        self.data_num = len(self.file_list)
        assert(self.data_num > 0)
        self.counter = 0
        self.max_iters = max_iters
        self.data_idx = 0
        self.data = None
        self.batch = None
        ## the queue for get batch task
        self.batch_queue = Queue(1)
        self.batch_queue.put_nowait('init')
        ## the queue for get data task
        self.data_queue = Queue(1)
        self.data_queue.put_nowait('init')
        self.load_data()
        self.prepare_batch()
        return None

    def load_data(self):
        self.data_idx = self.data_idx % self.data_num 
        self.data_queue.get(False)
        self.data = None
        gc.collect()
        self.data = np.load(self.file_list[self.data_idx])
        self.data_queue.put_nowait('loaded')
        self.data_idx += 1
        return None

    def prepare_batch(self):
        print 'OK'
        self.data_queue.get(block=True, timeout=self.life)
        print 'check'
        assert(self.batch_size < self.data.shape[0])
        idx = np.random.choice(self.data.shape[0], self.batch_size)
        self.batch_queue.get_nowait()
        self.batch = self.data[idx]
        self.counter = (self.counter + 1) % self.max_iters
        self.batch_queue.put_nowait('loaded')
        self.data_queue.put_nowait('xuming')
        return None

    def next_batch(self):
        self.counter = (self.counter + 1) % self.max_iters
        self.batch_queue.get(block=True, timeout=self.life) 
        if self.counter == 0:
            Process(target=self.load_data).start()
        return ([self.batch, Process(target=self.prepare_batch).start()][0])




