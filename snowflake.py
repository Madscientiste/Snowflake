from datetime import datetime
from itertools import count
import time


class snowflake:
    increment_bits = 10
    increment_mask = -1 ^ (-1 << increment_bits)

    instance_id_bits = 5
    instance_id_mask = -1 ^ (-1 << instance_id_bits)
    instance_id = 0
    instance_id_shift = increment_bits

    process_id_bits = 10
    process_id_mask = -1 ^ (-1 << process_id_bits)
    process_id_shift = instance_id_bits

    timestamp_bits = 42
    timestamp_shift = instance_id_bits + process_id_bits
    timestamp_mask = -1 ^ (-1 << timestamp_bits)

    sleep = lambda x: time.sleep(x / 1000.0)

    def __init__(self, value=None, process_id=0) -> None:
        super().__init__()
        snowflake.instance_id = (snowflake.instance_id + 1) & self.instance_id_mask
        self.process_id = process_id & self.process_id_mask
        self.increment = 0

        self.__value = next(self) if not value else int(value)

    def __repr__(self):
        return f"snowflake('{self.__value}')"

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        self.increment = (self.increment + 1) & self.increment_mask
        return self.__generate__()

    def __generate__(self):
        last_timestamp = -1

        while True:
            self.increment = (self.increment + 1) & self.increment_mask
            timestamp = int(time.time() * 1000)

            if last_timestamp > timestamp:
                print("clock is moving backwards. waiting until {last_timestamp}")
                self.sleep(last_timestamp - timestamp)
                continue

            last_timestamp = timestamp

            b_timestamp = (timestamp - self.initial_epoch) << self.timestamp_shift
            b_process_id = (self.process_id & self.process_id_mask) << self.process_id_shift
            b_increment = self.increment & self.instance_id_bits
            b_instance_id = self.instance_id

            yield b_timestamp | b_process_id | b_instance_id | b_increment

    @property
    def timestamp(self):
        return float((self.__value >> 22) + self.initial_epoch) / 1000

    @property
    def date(self):
        return datetime.fromtimestamp(self.timestamp).strftime("%d-%m-%Y | %H:%M:%S")

    @property
    def to_binary(self):
        return format(self.__value, "08b")


tobin = lambda x: format(x, "08b")
# print(id.to_binary, len(id.to_binary))

for snow in snowflake():
    print(snow)


for x in range(50):
    id = snowflake()
    print("x", id, id.process_id)

    for y in range(10):
        id = snowflake(process_id=1)
        print("y", id, id.process_id)

        for z in range(10):
            id = snowflake(process_id=2)
            print("z", id, id.process_id)