import timeit
import requests
import logging
import time
import random
import dill
import codecs
import subprocess
import os


def serialize(obj) -> str:
    return codecs.encode(dill.dumps(obj), "base64").decode()


def deserialize(obj: str):
    return dill.loads(codecs.decode(obj.encode(), "base64"))



base_url = "http://127.0.0.1:8000/"

def double(x):
    return x * 2

def evaluate(tasks):
    for i in range(tasks):
        resp = requests.post(base_url + "register_function",
                            json={"name": "hello",
                                "payload": serialize(double)})
        fn_info = resp.json()

        resp = requests.post(base_url + "execute_function",
                            json={"function_id": fn_info['function_id'],
                                "payload": serialize(((i,), {}))})

    print("resp")

    task_id = resp.json()["task_id"]

    resp = requests.get(f"{base_url}status/{task_id}")
    print(resp.json())
if __name__ == '__main__':
    ## evaluate push
    workers_task = {
        1:5,
        2:10,
        4:20,
        8:40
    }
    print(os.listdir())
    runtime_workers = {}
    type_of_worker = ['local', 'push', 'pull']
    for worker in type_of_worker:
        runtime = []
        for k,v in workers_task.items():
            if v == 40 and worker == 'local':
                continue
            cmd = 'python task_dispatcher.py -m ' + worker + ' -p 6379 -w ' + str(k)
            pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                        shell=True, preexec_fn=os.setsid) 
            start = timeit.default_timer()
            evaluate(v)
            runtime.append(timeit.default_timer() - start)
            pro.kill()
            #time.sleep(5)
        runtime_workers[worker] = runtime
    

    print(runtime_workers)