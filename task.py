import os
from rq import Queue
from redis import from_url
from utilities.mail_utils import send_email

redis_conn = from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))
queue = Queue(connection=redis_conn)

def enqueue_welcome_email(to_email, username):
    job = queue.enqueue(send_email, to_email, username)
    return job

# from rq import Queue
# from redis import from_url
# from utilities.mail_utils import send_email
# import os


# redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# redis_conn = from_url(redis_url)
# q = Queue(connection=redis_conn)

# def enqueue_welcome_email(to_email, username):
#     print("Debug: Enqueuing welcome email task", to_email, username)
    
#     try:
#         job = q.enqueue(send_email, to_email, username)
#         print(f"Debug: Job {job.id} enqueued successfully")
#         return job.id

#     except Exception as e:
#         print(f"Error enqueuing job: {e}")
#         return None
