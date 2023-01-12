import logging

logging.basicConfig(
    format="%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


from datetime import datetime
from diskcache import Index

import sys
from example import example

IS_FILE_INPUT = False
try:
    IS_FILE_INPUT = os.path.exists(example[0])
except:
    pass

from . import QUEUE_DIR, QUEUE_NAME

# En variable to configure allowed origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*")

PREDICTION_LOOP_SLEEP = float(os.getenv("PREDICTION_LOOP_SLEEP", "0.06"))
BATCH_COLLECTION_SLEEP_IF_EMPTY_FOR = float(
    os.getenv("BATCH_COLLECTION_SLEEP_IF_EMPTY_FOR", "60")
)
BATCH_COLLECTION_SLEEP_FOR_IF_EMPTY = float(
    os.getenv("BATCH_COLLECTION_SLEEP_FOR_IF_EMPTY", "1")
)
MANAGER_LOOP_SLEEP = float(os.getenv("MANAGER_LOOP_SLEEP", "8"))

RUNNING_TIME_PER_EXAMPLE_AVERAGE_OVER = int(
    os.getenv("RUNNING_TIME_PER_EXAMPLE_AVERAGE_OVER", "100")
)


"""
METRICS_INDEX[unique_id] = {
    "extras": [],
    "prediction_start": {0: time.time()},
    "prediction_end": {0: time.time()},
    "predicted_in_batch": {0: len(unique_ids)},
    "result": [],
    "received": time.time(),
    "in_data": [],
    "responded": time.time()
}
"""
# TODO: getting the request index results