import multiprocessing
from snowflake import Snowflake, Bits

id_generator = Snowflake()


def generate_snowflakes(x):
    id_generator = Snowflake()
    # print("MP: instance id: -> ", id_generator.sequence)
    return x * x * 100
    # print("multiprocessing: ", id_generator.instance_id)


if __name__ == "__main__":
    with multiprocessing.Pool(processes=8) as pool:
        pool.map(generate_snowflakes, range(8))

    for snowflake in id_generator:
        print(snowflake)
