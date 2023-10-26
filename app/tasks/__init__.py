import ctypes
import time


from app.worker import taskq


@taskq.task(bind=True)
def add_one(self, x):
    time.sleep(1)
    ctypes.string_at(0)
    return x + 1, self.request.id
