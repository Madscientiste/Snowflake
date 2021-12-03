from __future__ import annotations
from datetime import datetime
from typing import Union

import multiprocessing
import copy
import time

EPOCH = datetime(2011, 1, 1)
INITIAL_EPOCHE = int(time.mktime(EPOCH.timetuple()))

mask = lambda x: -1 ^ (-1 << x)
sleep = lambda x: time.sleep(x / 1000)
get_timestamp = lambda: int(time.time() * 1000)


def get_worker_id():
    name = multiprocessing.current_process().name
    return int(name.split("-")[-1]) if "PoolWorker" in name else 0


def validate(func):
    def wrapper(*args, **kwargs):
        other = kwargs.get("other", None)
        if other is not None and type(other) != int:
            raise TypeError(f"{other} must be an int")

        return func(*args, **kwargs)

    return wrapper


class Bits:
    def __init__(self, bits: int, shift: int, name: str):
        self.bits = bits
        self.mask = mask(bits)
        self.name = name
        self.shift = shift
        self.value = 0

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __str__(self):
        return f"{self.value}"

    def __int__(self):
        return self.value

    def __get__(self, instance, cls):
        return self.value if instance is None else self

    def __set__(self, instance, other):
        if isinstance(other, int):
            self.value = other & self.mask
        elif isinstance(other, Bits):
            self.value = other.value & self.mask
        else:
            raise TypeError(f"{other} is not an int")
        return self

    def __radd__(self, other):
        return self.value + other

    def __add__(self, other):
        self.value = (self.value + other) & self.mask
        return self

    @validate
    def __xor__(self, other):
        return self.value ^ other

    @validate
    def __and__(self, other):
        return self.value & other

    @validate
    def __or__(self, other):
        return self.value | other

    @validate
    def __lshift__(self, other):
        return self.value << other

    @validate
    def __rshift__(self, other):
        return self.value << other


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


def to_next_ms(prev_timestamp: int) -> int:
    timestamp = get_timestamp()

    while timestamp <= prev_timestamp:
        timestamp = get_timestamp()

    return timestamp


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
        self.snowflake = snowflake
        # set the sequence to 0 so there is not mutation beween instances
        self.sequence = 0
        self.last_timestamp = 0

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
