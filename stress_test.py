import multiprocessing
from pprint import pprint
from timeit import default_timer as timer
from datetime import timedelta
import numpy as np

from snowflake import Snowflake


def generate_snowflakes(size):
    ids = []
    snowflake = Snowflake(process_id=0)

    for i in range(size):
        id = next(snowflake)
        ids.append(int(id))

    return ids


def mp_generate_snowflakes(*args):
    process_name = multiprocessing.current_process().name
    process_id = int(process_name.split("-")[-1])

    ids = []
    snowflake = Snowflake(process_id=process_id)

    for i in range(1000):
        id = next(snowflake)
        ids.append(int(id))

    return ids


# not the best test ever, but works to get an idea if it works well or doesn't
if __name__ == "__main__":
    start = timer()

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    result = pool.map(mp_generate_snowflakes, range(1000))
    end = timer()

    result_flat = [id for ids in result for id in ids]

    pool.close()
    pool.join()

    unique_ids = []
    unique_ids.sort()

    pprint(f"{(np.unique(result_flat).size):,}")
    print(timedelta(seconds=end - start))
    print("With multi-processing \n")

    start = timer()
    generated = [id for id in generate_snowflakes(100000)]
    end = timer()

    pprint(f"{(np.unique(generated).size):,}")
    print(timedelta(seconds=end - start))
    print("For a regular instance")
