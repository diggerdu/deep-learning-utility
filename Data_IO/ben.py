import numpy as np
import os
import time

s = time.time()
file_list = os.listdir('./test/')

v = None
for i in range(2):
    data = np.load('./test/'+file_list[i%len(file_list)])
    for j in range(512):
        idx = np.random.choice(data.shape[0], 128)
        time.sleep(0.1)
        v = data[idx]

print time.time() - s



