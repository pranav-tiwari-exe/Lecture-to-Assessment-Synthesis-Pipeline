import os
import time
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
celery_app = Celery("worker", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(name="worker.transcribe_audio")
def transcribe_audio(file_path: str):
    print(f"[worker] Transcribing {file_path}")
    time.sleep(3)
    return {"text": "This is a dummy transcription."}
