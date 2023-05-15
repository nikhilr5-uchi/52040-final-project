import zmq
import time
import sys
import random
import codecs
import dill
from multiprocessing import Pool

context = zmq.Context()
s = context.socket(zmq.REQ)


def serialize(obj) -> str:
    return codecs.encode(dill.dumps(obj), "base64").decode()

def deserialize(obj: str):
    return dill.loads(codecs.decode(obj.encode(), "base64"))


def execute_task(func, args):
    res = func(args)
    print(res)
    time.sleep(1 * random.random())
    s.send_string(str(res))
    return


def pull_worker(dispatch_url, workerId):
    res = -1
    s.connect(dispatch_url)
    s.send_string("Ready")
    while True:
        workload = s.recv_string()
        body = deserialize(workload)
        func = deserialize(body['function'])
        args = deserialize(body['args'])
        
        execute_task(func, args)
        





if __name__ == '__main__':
    dispatch_url = sys.argv[1]
    workerId = sys.argv[2]
    pull_worker(dispatch_url, workerId)
