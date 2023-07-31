import time

import uvicorn
from celery import Celery
from celery.result import AsyncResult
from fastapi import FastAPI, HTTPException, Body
from kombu import Queue
from redis import Redis
from starlette.responses import JSONResponse

app = FastAPI()

if __name__ == "__main__":
    uvicorn.run("tasks:app", port=8000, log_level="debug")

# make a redis url with password
broker_url = "redis://default:abc123123@redis-19090.c258.us-east-1-4.ec2.cloud.redislabs.com:19090"
backend_url = "redis://default:abc123123@redis-19090.c258.us-east-1-4.ec2.cloud.redislabs.com:19090"


class Settings:
    """CELERY SETTINGS"""

    broker_url: Redis = broker_url
    result_backend: Redis = backend_url
    # beat_scheduler: str = "redbeat.RedBeatScheduler"
    beat_max_loop_interval: int = 5
    worker_max_tasks_per_child: int = 200
    worker_max_memory_per_child: int = 16384
    broker_transport_options: object = {"visibility_timeout": 43200}
    enable_utc: bool = False
    result_extended: bool = True
    timezone: str = "Europe/London"
    task_default_queue: str = "default"
    task_queues: tuple = (
        Queue("default", routing_key="task.#"),
        Queue("high_priority", routing_key="high_priority.#"),
        Queue("low_priority", routing_key="low_priority.#"),
    )
    task_default_exchange: str = "tasks"
    task_default_exchange_type: str = "topic"
    task_default_routing_key: str = "task.default"
    # expire task results after 7 days
    result_expires: int = 604800


def create_celery_app() -> Celery:
    _app = Celery(__name__, broker=broker_url, backend=backend_url)
    _app.config_from_object(Settings)
    _app.autodiscover_tasks(["tasks"])
    _app.set_default()

    return _app


celery = create_celery_app()



@app.post("/tasks", status_code=201)
def run_task(payload=Body(...)):
    task_type = payload["type"]
    task = create_task.delay(int(task_type))
    return JSONResponse({"task_id": task.id})


@app.get("/tasks/{task_id}")
def get_status(task_id):
    try:
        task_result = AsyncResult(task_id)
        result = {
            "task_id": task_id,
            "task_status": task_result.status,
            "task_result": task_result.result,
        }
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@app.get("/ml-data")
async def ocr(data: int):
    try:
        task = ocr_task.delay()
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@celery.task(bind=True)
def ocr_task(self, data: int):
    for iteration in range(0, data):
        progress = (iteration + 1) / data * 100
        time.sleep(3)
        self.update_state(state='PROCESS', meta={'current': iteration, "total": data, 'progress': progress})
    return {"content": "return content"}


@app.get("/result/{task_id}")
async def ocr_result(task_id):
    result = ocr_task.AsyncResult(task_id)
    response = {}
    if result.state == "PENDING":
        response = result.info
    elif result.state == "PROCESS":
        response = result.info
    else:
        response = {
            "state": result.state,
            "current": 1,
            "total": 1,
            "status": str(result.info)
        }
    if result.ready():
        data = result.get(Exception)
        return {"status": "COMPLETED", "data": data}
    elif result.failed():
        raise HTTPException(status_code=422, detail="process failed")
    return {"status": "PROCESS", "response": response}


# celery -A tasks:celery worker -l info -c 2