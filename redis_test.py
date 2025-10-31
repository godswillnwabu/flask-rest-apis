from redis import from_url
from rq import Queue

r = from_url("redis://127.0.0.1:6379/0")
q = Queue(connection=r)

def add(x,y):
    return x + y

job = q.enqueue(add, 3, 4)
print("Job enqueued with ID:", job.id)