from fastapi import FastAPI, Request
import uuid
import redis
import codecs
import dill
import json

r = redis.Redis('localhost', 6379)
app = FastAPI()

def deserialize(obj: str):
    return dill.loads(codecs.decode(obj.encode(), "base64"))

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post('/register_function')
async def handle_registering(request: Request):
    body_j = await request.body()
    body = json.loads(body_j.decode('utf-8'))
    uuidV = str(uuid.uuid4())
    obj = {}
    obj['function'] = body
    r.mset({uuidV: json.dumps(obj)})
    return {"function_id" : uuidV, "function": body}

@app.post('/execute_function')
async def handle_executing(request: Request):
    body_j = await request.body()
    body = json.loads(body_j.decode('utf-8'))
    uuidP = body['function_id']
    json_obj = r.get(uuidP)
    obj = json.loads(json_obj)
    function = obj['function']
    func = function['payload']
    new_obj = {
        "status" : "QUEUED",
        "function" : func,
        "args" : body['payload']    
    }
    new_uuid = str(uuid.uuid4())
    r.mset({new_uuid: json.dumps(new_obj)})
    r.publish('tasks', new_uuid)
    return {"task_id" : new_uuid, "obj": new_obj}

@app.get('/status/{uuidT}')
async def get_status(uuidT):
    try:
        json_obj = r.get(uuidT)
        obj = json.loads(json_obj)
        return {"task_id" : uuidT, "status" : obj['status']}
    except:
        return {"message" : "No task exists in Redis DB for inputed uuid."}


@app.get('/result/{uuidV}')
async def handle_get(uuidV):
    res  = r.get(uuidV)
    body = json.loads(res.decode('utf-8'))
    return {"task_id": uuidV, "status" : body['status']}