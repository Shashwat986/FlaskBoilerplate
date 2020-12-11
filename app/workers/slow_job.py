from time import sleep
from app import rq


@rq.job
def slow_job(s):
    sleep(s)
    return True
