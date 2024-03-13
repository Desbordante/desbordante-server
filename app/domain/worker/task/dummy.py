import ctypes
import random
import time

from app.worker import worker


@worker.task(bind=True)
def dummy_task(self, x):
    time.sleep(1)
    if random.random() < 0.5:
        ctypes.string_at(0)
    return x + 1, self.request.id
