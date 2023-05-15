import zmq
import time
import sys
import random
import codecs
import dill

def serialize(obj) -> str:
    return codecs.encode(dill.dumps(obj), "base64").decode()

def deserialize(obj: str):
    return dill.loads(codecs.decode(obj.encode(), "base64"))


def push_worker(dispatch_url, identity):
    context = zmq.Context.instance()
    worker = context.socket(zmq.DEALER)
    id_bytes = bytes(identity, 'UTF-8')
    worker.setsockopt(zmq.IDENTITY, id_bytes)
    worker.connect(dispatch_url)
    print('worker number ' + identity + ' is connected')
    while True:
        request = worker.recv()
        body = deserialize(request.decode('UTF-8'))

        func = deserialize(body['function'])
        args = deserialize(body['args'])
        res = func(args)
        print(res)
        time.sleep(1 * random.random())
        worker.send(serialize(res).encode('UTF-8'))





if __name__ == '__main__':
    dispatch_url = sys.argv[1]
    identity = sys.argv[2]
    push_worker( dispatch_url, identity)
