from __future__ import annotations
from datetime import datetime
from typing import Union
from datetime import datetime
import time

import copy

from .bits import Bits
from .__functions import get_worker_id, get_timestamp, to_next_ms, validate
from .exceptions import TimeWentBackward


class BaseSnowflake:
    _EPOCH = datetime(2020, 1, 1)
    timestamp = Bits(42, 22, "timestamp")
    sequence = Bits(22, 0, "sequence")

    def __init__(self, snowflake: int = 0):
        if hasattr(self, "timestamp") and self.timestamp is None:
            raise ValueError("Timestamp is None")

        if hasattr(self, "sequence") and self.sequence is None:
            raise ValueError("Sequence is None")

        if hasattr(self, "_EPOCH") and self._EPOCH is None:
            raise ValueError("Epoch is None")

        if not isinstance(self.timestamp, Bits):
            raise ValueError("Timestamp must be a bit")

        if not isinstance(self.sequence, Bits):
            raise ValueError("Sequence must be a bit")

        if not isinstance(self._EPOCH, datetime):
            raise ValueError("Epoch must be a datetime")

        # snowflake must be an int, if its str, convert to int
        if isinstance(snowflake, str):
            snowflake = int(snowflake)

        self.sequence = self.unshift(snowflake, self.sequence)
        self.timestamp = (snowflake >> self.timestamp.shift) + self.epoch_ts
        self.last_timestamp = 0

        self.snowflake = snowflake or int(next(self))

    def __get__(self, instance, cls):
        return self.snowflake if instance is None else self

    def __str__(self):
        return f"{self.snowflake}"

    def __int__(self):
        return self.snowflake

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

            if timestamp < self.last_timestamp:
                raise TimeWentBackward(f"Time went backwards from {self.last_timestamp} to {timestamp}")

            self.last_timestamp = timestamp
            bits_00 = (timestamp - self.epoch_ts) << self.timestamp.shift
            bits_01 = self.sequence << self.sequence.shift

            yield bits_00 | bits_01

    @validate
    def __xor__(self, other):
        return self.snowflake ^ other

    @validate
    def __and__(self, other):
        return self.snowflake & other

    @validate
    def __or__(self, other):
        return self.snowflake | other

    @validate
    def __lshift__(self, other):
        return self.snowflake << other

    @validate
    def __rshift__(self, other):
        return self.snowflake >> other

    @property
    def epoch_ts(self):
        return int(time.mktime(self._EPOCH.timetuple()))

    @property
    def get_timestamp(self):
        return float(((self >> self.timestamp.shift) + self.epoch_ts)) / 1000

    @property
    def to_binary(self):
        return format(int(self), "08b")

    def to_date(self, fmt="%d-%m-%Y | %H:%M:%S"):
        return datetime.fromtimestamp(self.get_timestamp).strftime(fmt)

    @staticmethod
    def unshift(value, bits: Bits):
        return value & ((-1 ^ (-1 << bits.bits)) << bits.shift)

    def generate(self, amount: int = 1) -> list:
        """Generate a list of snowflakes"""
        return [int(next(self)) for _ in range(amount)]

    def generate_v2(self, amount: int = 1) -> list:
        """Same as generate but using a while loop"""
        store = []
        while amount != len(store):
            store.append(int(next(self)))
        return store


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


class Snowflake(BaseSnowflake):
    _EPOCH = datetime(2011, 1, 1)

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

            if timestamp < self.last_timestamp:
                raise TimeWentBackward(f"Time went backwards from {self.last_timestamp} to {timestamp}")

            self.last_timestamp = timestamp
            bits_00 = (timestamp - self.epoch_ts) << self.timestamp.shift

            bits_01 = self.worker_id << self.worker_id.shift
            bits_02 = self.instance_id << self.instance_id.shift
            bits_03 = self.sequence << self.sequence.shift

            yield bits_00 | bits_01 | bits_02 | bits_03
