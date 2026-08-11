from tasks.serializer import deserialize_task
def execute_task(payload):
    func, args, kwargs, task_id = deserialize_task(payload)
    print(f"Executing task {task_id}")
    return func(*args, **kwargs)