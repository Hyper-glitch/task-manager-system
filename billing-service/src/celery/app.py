import os  # isort:skip
import sys

from src.config import settings

os.environ.setdefault("SETTINGS_MODULE", "src.conf")  # noqa
sys.path.append(os.path.dirname(__file__))  # noqa

from celery import Celery


app = Celery("billing")

PROCESS_CYCLE_SCHEDULE = 5
CLOSE_CYCLE_SCHEDULE = 30
REFRESH_BALANCE_SCHEDULE = 5
DEFAULT_TASK_QUEUE = "default"
BASE_PATH = "src.tasks.{}"
TASK_ROUTES = {
    BASE_PATH.format("send_payment"): {
        "queue": "send_payment",
    }
}
SCHEDULE = {
    "process_cycle": {
        "task": BASE_PATH.format("process_cycle"),
        "schedule": PROCESS_CYCLE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
    "close_cycle": {
        "task": BASE_PATH.format("close_cycle"),
        "schedule": CLOSE_CYCLE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
    "refresh_balance": {
        "task": BASE_PATH.format("refresh_balance"),
        "schedule": REFRESH_BALANCE_SCHEDULE,
        "args": [],
        "kwargs": {},
    },
}

app.conf.update(
    broker_url=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    result_backend=f"redis://{settings.redis_host}:{settings.redis_port}/{settings.redis_db}",
    beat_schedule=SCHEDULE,
    task_default_queue=DEFAULT_TASK_QUEUE,
    task_routes=TASK_ROUTES,
)
app.autodiscover_tasks(["src"])
