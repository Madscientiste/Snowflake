import time
import multiprocessing


mask = lambda x: -1 ^ (-1 << x)
sleep = lambda x: time.sleep(x / 1000)
get_timestamp = lambda: int(time.time() * 1000)


def get_worker_id():
    name = multiprocessing.current_process().name
    return int(name.split("-")[-1]) if "PoolWorker" in name else 0


def to_next_ms(prev_timestamp: int) -> int:
    timestamp = get_timestamp()
    while timestamp <= prev_timestamp:
        timestamp = get_timestamp()
    return timestamp


def validate(func):
    def wrapper(*args, **kwargs):
        other = kwargs.get("other", None)
        if other is not None and type(other) != int:
            raise TypeError(f"{other} must be an int")
        return func(*args, **kwargs)

    return wrapper
