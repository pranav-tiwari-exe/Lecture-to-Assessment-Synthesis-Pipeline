import os
from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery
from celery.result import AsyncResult

app = FastAPI(title="Dynamic Question Bank")

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery = Celery(broker=REDIS_URL, backend=REDIS_URL)

class EnqueueResponse(BaseModel):
    task_id: str

@app.get("/")
def root():
    return {"message": "Backend running"}

@app.post("/enqueue", response_model=EnqueueResponse)
def enqueue():
    task = celery.send_task("worker.transcribe_audio", args=["sample.mp3"])
    return EnqueueResponse(task_id=task.id)

@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    res = AsyncResult(task_id, app=celery)
    return {"task_id": task_id, "status": res.status, "result": res.result}
