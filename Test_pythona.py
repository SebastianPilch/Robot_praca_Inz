import time
import os

start = time.time()
print(start)
i = 0
pin_state = True
while i < 1000:
    stop = time.time()
    if stop - start > 0.1:
        start = stop
        if pin_state:
            os.system(f'gpio write 3 1')
            print(1)
        else:
            os.system(f'gpio write 3 0')
        pin_state = not pin_state 
        i += 1
print('DUPA')