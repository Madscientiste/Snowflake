from __future__ import annotations
from datetime import datetime
from typing import Union

import copy

from .bits import Bits
from .__functions import get_worker_id, get_timestamp, to_next_ms

from .__config import INITIAL_EPOCHE


# [Timestamp][42](64 to 22)
# Miliseconds since the epoch specified
# 00000 00000 00000 00000 00000 00000 00000 00000 00

# [Worker ID][5](22 to 17)
# Could be a CPU ID, or a PoolWorker ( multi-processing ) eg: CPU0, CPU1, CPU2, CPU3, ect..
# 00000

# [Instance ][5](17 to 12)
# Auto incremented for each new instance of the class
# 00000

# [Sequence ][12](12 to 0)
# Allow creation of multiple snowflakes in the same millisecond
# 00000 00000 000


class Snowflake:

    timestamp = Bits(42, 22, "timestamp")
    worker_id = Bits(5, 17, "worker_id")
    instance_id = Bits(5, 12, "instance_id")
    sequence = Bits(12, 0, "sequence")

    def __new__(cls, *args, **kwargs):
        instance = super(Snowflake, cls).__new__(cls)
        instance.instance_id = copy.deepcopy(cls.instance_id + 1)
        instance.worker_id = get_worker_id()
        return instance

    def __init__(self, snowflake: Union[str, int] = None):
        self.sequence = 0  # set the sequence to 0 so there is not mutation beween instances
        self.last_timestamp = 0
        self.snowflake = snowflake or int(next(self))

    def __str__(self):
        return f"{self.snowflake}"

    def __int__(self):
        return self.snowflake

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __next__(self):
        self.snowflake = next(iter(self))
        return self

    def __iter__(self):
        while True:
            timestamp = get_timestamp()

            if self.last_timestamp == timestamp:
                self.sequence = self.sequence + 1

                # if the sequence exhausted, wait for the next millisecond
                if self.sequence == 0:
                    timestamp = to_next_ms(self.last_timestamp)

            else:
                self.sequence = 0

            # this can happen with time changes
            if timestamp < self.last_timestamp:
                raise ValueError(f"Time went backwards from {self.last_timestamp} to {timestamp}")

            self.last_timestamp = timestamp
            bits_00 = (timestamp - INITIAL_EPOCHE) << self.timestamp.shift
            bits_01 = self.worker_id << self.worker_id.shift
            bits_02 = self.instance_id << self.instance_id.shift
            bits_03 = self.sequence << self.sequence.shift

            yield bits_00 | bits_01 | bits_02 | bits_03

    def generate(self, amount: int = 1) -> list:
        """Generate a list of snowflakes"""
        return [int(next(self)) for _ in range(amount)]

    def generate_v2(self, amount: int = 1) -> list:
        """Same as generate but using a while loop"""
        store = []
        while amount != len(store):
            store.append(int(next(self)))
        return store

    @staticmethod
    def get_epoch():
        return INITIAL_EPOCHE

    @property
    def get_timestamp(self):
        return ((int(self) >> self.timestamp.shift) + INITIAL_EPOCHE) / 1000

    @property
    def to_binary(self):
        return format(int(self), "08b")

    @property
    def get_worker_id(self):
        return self.worker_id

    def to_date(self, fmt="%d-%m-%Y | %H:%M:%S"):
        return datetime.fromtimestamp(self.get_timestamp).strftime(fmt)
