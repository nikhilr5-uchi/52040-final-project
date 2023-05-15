import uuid
import redis
import argparse
from multiprocessing import Pool
import codecs
import dill
import json
import zmq
import subprocess
import random
import os


r = redis.Redis('localhost', 6379)

def serialize(obj) -> str:
    return codecs.encode(dill.dumps(obj), "base64").decode()

def deserialize(obj: str):
    return dill.loads(codecs.decode(obj.encode(), "base64"))

def execute_task(obj, task_id):
    print("YOOOO: ", obj)
    ser_func = obj['function']
    ser_params = obj['args']
    func = deserialize(ser_func)
    args = deserialize(ser_params)
    print(func)
    results = func(args)
    ser_result = serialize(results)
    new_obj = {
        "status" : "COMPLETE",
        "result_payload" : ser_result
    }
    print(new_obj)
    r.mset({task_id: json.dumps(new_obj)})
    return results

def local(uuidT, obj, num_pool):
    param = ""
    with Pool(num_pool) as p:
        p.starmap(execute_task, [(obj, uuidT)])

def push(uuidT, obj, client, worker_list):
    obj2 = serialize(obj)
    ident = bytes(random.choice(worker_list), 'UTF-8')
    client.send_multipart([ident, obj2.encode('UTF-8')])
    res = client.recv()
    results = res.decode('UTF-8')
    new_obj = {
        "status" : "COMPLETED",
        "result_payload" : results
    }
    r.mset({uuidT: json.dumps(new_obj)})
    print(new_obj)
    return

def pull(uuidT, obj,s):
    obj2 = serialize(obj)
    s.send_string(obj2)
    results = s.recv_string()
    ser_result = serialize(results)
    new_obj = {
        "status" : "COMPLETED",
        "result_payload" : ser_result
    }
    print(new_obj)
    r.mset({uuidT: json.dumps(new_obj)})
    return 

def run(port, mode, num_pool):
    r = redis.Redis(host='localhost', port=port )
    if mode == 'pull':
        context = zmq.Context()
        s = context.socket(zmq.REP)
        bind_spot = "tcp://127.0.0.1:5555"
        s.bind(bind_spot)
        print('binded')
        cmd = 'python pull_worker.py ' +  ' tcp://127.0.0.1:5555 ' + str(1)
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                shell=True, preexec_fn=os.setsid) 
        m = s.recv_string()
    elif mode == 'push':
        context = zmq.Context.instance()
        client = context.socket(zmq.ROUTER)
        client.bind("tcp://127.0.0.1:5555")
        ## create number of workers
        worker_list = []
        for i in range(num_pool):
            worker_list.append(str(i))
            cmd = 'python push_worker.py ' +  ' tcp://127.0.0.1:5555 ' + str(i)
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
    while True:
        sub = r.pubsub()
        sub.subscribe('tasks')
        for message in sub.listen():
            print("MESSAGE: ", message)
            if message is not None:
                print('message is not None')
                uuidT = message.get('data')
                print("uuidT: ", uuidT)
                if uuidT == 1:
                    continue
                obj_j = r.get(uuidT)
                obj = json.loads(obj_j.decode('utf-8'))
                print("obj: ", obj)
                if mode == 'local':
                    local(uuidT, obj, num_pool)
                elif mode == 'pull':
                    print('pull')
                    pull(uuidT, obj,s )
                    print("done")
                elif mode == 'push':
                    push(uuidT, obj, client, worker_list)
                else:
                    print("Incorrect mode")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("-m")
    parser.add_argument("-p")
    parser.add_argument("-w")

    args = vars(parser.parse_args())

    mode = args['m']
    port = args['p']
    num_worker_processors = int(args['w'])


    print(mode, port, num_worker_processors)

    run(port, mode, num_worker_processors)