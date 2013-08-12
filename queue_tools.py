from lightqueue.queue import Queue
from test_module import myfunc
import os
import redis

class TaskQueue(object):
    def __init__(self, queue_name):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.delete(queue_name)
        self.queue_name = queue_name
        self.q = Queue(db=0, queue_name=queue_name)

    def add_task(self, func, *args, **kwargs):
        self.q.enqueue(func, *args, **kwargs)

    def execute(self, workers):
        os.system(('lightqueue start -e parallel -workers {workers} '
                   '-qname {qname} -t 1').
                  format(qname=self.queue_name, **locals()))
