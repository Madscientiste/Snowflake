from datetime import datetime
import time


# TODO : safe mod, where it make sure the id generated is safe ( slower )
class Snowflake:

    # Saturday, 1 January 2011 12:00:00 GMT+01:00
    initial_epoch = 1293879600000
    mask = lambda x: -1 ^ (-1 << x)
    sleep = lambda x: time.sleep(x / 1000)
    get_timestamp = lambda x: int(time.time() * 1000)

    sequence_bits = 10
    sequence_mask = mask(sequence_bits)

    instance_bits = 6
    instance_mask = mask(instance_bits)
    instance_shift = sequence_bits
    instance_id = 0

    process_bits = 6
    process_mask = mask(instance_bits)
    process_shift = sequence_bits + instance_bits
    process_id = 0

    timestamp_bits = 42
    timestamp_mask = mask(timestamp_bits)
    timestamp_shift = process_bits + sequence_bits + instance_bits
    timestamp = -1

    def __new__(cls, *args, **kwds):
        cls.instance_id = (cls.instance_id + 1) & cls.instance_mask
        return super(Snowflake, cls).__new__(cls)

    def __init__(self, snowflake=0, process_id=0):
        self.sequence = 0
        self.last_timestamp = 0

        self.process_id = process_id
        self.snowflake = snowflake

        if snowflake == 0:
            next(self)

    def __int__(self):
        return self.snowflake

    def __str__(self):
        return f"{self.snowflake}"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self)})"

    def __next__(self):
        self.snowflake = next(iter(self))
        return self

    def __iter__(self):
        while True:
            timestamp = self.get_timestamp()

            if self.last_timestamp == timestamp:
                timestamp = self.get_timestamp()
                self.sequence = (self.sequence + 1) & self.sequence_mask
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            b_timestamp = (timestamp - self.initial_epoch) << self.timestamp_shift
            b_process = (self.process_id & self.process_mask) << self.process_shift
            b_instance = (self.instance_id & self.instance_mask) << self.instance_shift
            b_sequence = self.sequence & self.sequence_mask

            yield b_timestamp | b_process | b_instance | b_sequence

    @property
    def timestamp(self):
        return float((int(self) >> 22) + self.initial_epoch) / 1000

    @property
    def to_date(self, format="%d-%m-%Y | %H:%M:%S"):
        return datetime.fromtimestamp(self.timestamp).strftime(format)

    @property
    def to_binary(self):
        return format(int(self), "08b")

    @property
    def to_hex(self):
        return "%16x" % int(self)
