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
from multiprocessing import Process, Queue, Pipe
import numpy as np


class DataIter(object):
    def __init__(self, data_path, max_iters=512, batch_size=128, life=59):
        self.life = life
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
        ## the pipe for get batch task
        self.batch_queue = Queue(1)
        self.batch_queue.put_nowait('init')
        ## the pipe for get data task
        self.data_queue = Queue(1)
        self.data_queue.put_nowait('init')
#        self.data_queue.get_nowait()
        self.data = self.load_data()
#       self.batch = self.prepare_batch()
        return None

    def load_data(self):
        self.data_idx = self.data_idx % self.data_num 
        self.data_queue.get_nowait()
        self.data = None
        gc.collect()
        self.data = np.load(self.file_list[self.data_idx])
        self.data_queue.put_nowait('loaded')
        self.data_idx += 1
        return None

    def prepare_batch(self):
        self.data_queue.get(block=True, timeout=self.life)
        assert(batch_size < self.data.shape[0])
        idx = np.random.choice(self.data.shape[0], batch_size)
        self.batch = self.data[idx]
        self.counter = (self.counter + 1) % max_iters
        self.batch_queue.put_nowait('loaded')
        return None

    def next_batch(self):
        self.counter = self.counter % max_iters
        if self.counter == 0:
            Process(self.load_data).start()
        self.batch_queue.get(block=True, timeout=self.life)
        return ([self.batch, Process(self.prepare_batch).start()][0])




