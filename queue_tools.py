from lightqueue.queue import Queue as lightQueue
from test_module import myfunc
import Queue
import os
import redis

class TaskQueue(object):
    def __init__(self, queue_name, host_name='localhost'):
        r = redis.StrictRedis(host=host_name, port=6379, db=0)
        r.delete(queue_name)
        self.queue_name = queue_name
        self.host_name = host_name
        self.q = lightQueue(host=host_name, db=0, queue_name=queue_name)
        self.py_queue = Queue.Queue()

    def add_task(self, func, *args, **kwargs):
        self.q.enqueue(func, *args, **kwargs)
        self.py_queue.put((func, args, kwargs))

    def execute(self, workers = 1):
        if workers == 1:
            while True:
                task = self.py_queue.get()
                if not task:
                    break
                else:
                    print '### Executing Task ###'
                    apply(task[0], task[1], task[2])
        else:
            os.system(('lightqueue start -e parallel -workers {workers} '
                       '-qname {qname} -host {host_name} -t 1').
                      format(qname=self.queue_name,
                             host_name=self.host_name,
                             **locals()))
