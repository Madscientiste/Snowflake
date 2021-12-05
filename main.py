# import time

from snowflake.bits import Bits
from snowflake.snowflake import Snowflake

# from datetime import datetime
# from snowflake import setup_snowflake, Snowflake

# setup_snowflake(epoch=datetime(2020, 1, 1))

# id_generator = Snowflake()
# id_generator = Snowflake()
# id_generator = Snowflake()
# id_generator = Snowflake()
# id_generator = Snowflake()

# print(id_generator)
# print(id_generator.get_timestamp)
# print(id_generator.to_date())
# print(id_generator.get_epoch())

# id_generator2 = Snowflake()


def generate_snowflakes(x):
    snowflake = Snowflake()
    return snowflake.generate(10000)


# if __name__ == "__main__":
#     with multiprocessing.Pool(processes=8) as pool:
#         start = time.perf_counter()
#         result = pool.map(generate_snowflakes, range(100))
#         end = time.perf_counter()

#         result = np.concatenate(result).ravel().tolist()
#         unique_ids = np.unique(result)

#     print(len(result), len(unique_ids), end - start)
