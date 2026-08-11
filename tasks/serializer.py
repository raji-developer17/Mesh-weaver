import cloudpickle, base64
def serialize_task(func, args, kwargs, task_id):
    payload = {"func": base64.b64encode(cloudpickle.dumps(func)).decode(), "args": args, "kwargs": kwargs, "task_id": task_id}
    return payload
def deserialize_task(payload):
    func = cloudpickle.loads(base64.b64decode(payload["func"]))
    return func, payload["args"], payload["kwargs"], payload["task_id"]