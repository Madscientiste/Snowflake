from datetime import datetime
import time

from snowflake import Bits
from snowflake import BaseSnowflake

from snowflake.__functions import get_worker_id, get_timestamp, to_next_ms, validate, mask


_EPOCH = datetime(2020, 1, 1)
epoch_ts = int(time.mktime(_EPOCH.timetuple()))

last_timestamp = -1
sequence = 0

lis = []

start = time.time()
while len(lis) < 1000000:
    timestamp = get_timestamp()

    if last_timestamp == timestamp:
        sequence = (sequence + 1) & mask(22)

        # if the sequence exhausted, wait for the next millisecond
        if sequence == 0:
            timestamp = to_next_ms(last_timestamp)
    else:
        sequence = 0

    if timestamp < last_timestamp:
        raise Exception(f"Time went backwards from {last_timestamp} to {timestamp}")

    last_timestamp = timestamp
    bits_00 = (timestamp - epoch_ts) << 22
    bits_01 = sequence

    lis.append(bits_00 | bits_01)


print(f"Time taken: {time.time() - start}")

print(len(lis))
