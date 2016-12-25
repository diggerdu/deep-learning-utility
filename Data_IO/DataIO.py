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
import threading
import numpy as np
import time
from multiprocessing import Pipe

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
        self.alter_data = None
        self.batch = None
        self.batch_thread = threading.Thread(target=self.prepare_batch)
        self.data_thread = threading.Thread(target=self.load_data)
        self.safe_flag = True
        self.data_thread.start()
        self.data_thread.join()
        
        self.batch_thread.start()
        return None

    def load_data(self):
        self.data_idx = self.data_idx % self.data_num 
        self.alter_data = np.load(self.file_list[self.data_idx])
        self.safe_flag = False
        self.data = self.alter_data
        self.safe_flag = True
        self.alter_data = None
        gc.collect()
        self.data_idx += 1
        return None

    def prepare_batch(self):
        while not self.safe_flag:
            pass
        assert(self.batch_size < self.data.shape[0])
        idx = np.random.choice(self.data.shape[0], self.batch_size)
        self.batch = self.data[idx]
        return None

    def next_batch(self):
        self.counter = (self.counter + 1) 
        if self.counter == 0:
            self.data_thread.join()
            self.data_thread = threading.Thread(target=self.load_data)
            self.data_thread.start()

        self.batch_thread.join()
        self.batch_thread = threading.Thread(target=self.prepare_batch)
        return ([self.batch, self.batch_thread.start()][0])



if __name__ == '__main__':
    s = time.time()
    t = DataIter('./test/')
    for i in range(1000):
        tmp = t.next_batch()
        time.sleep(0.1)
    print time.time() - s
