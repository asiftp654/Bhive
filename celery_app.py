from celery import Celery
from config import settings

# Build Redis URLs using settings
redis_broker_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"
redis_backend_url = f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}"

celery = Celery(
    "worker",
    broker=redis_broker_url,  # Redis as broker
    backend=redis_backend_url 
)

# Configure Celery to autodiscover tasks
celery.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)
celery.autodiscover_tasks(['tasks'])
import tasks

celery.conf.beat_schedule = {
    "update-prices-every-hour": {
        "task": "tasks.update_latest_prices",
        "schedule": 600.0,  # run every hour
    },
}
celery.conf.timezone = "UTC"
