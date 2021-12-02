from datetime import datetime
import time

EPOCH = datetime(2011, 1, 1)
INITIAL_EPOCHE = int(time.mktime(EPOCH.timetuple()))

mask = lambda x: -1 ^ (-1 << x)
sleep = lambda x: time.sleep(x / 1000)
get_timestamp = lambda x: int(time.time() * 1000)


class Bits:
    def __init__(self, bits, shift, name):
        self.bits = bits
        self.mask = mask(bits)
        self.name = name
        self.shift = shift
        self.value = 0

    def __str__(self):
        return f"{self.name}({self.value}/{self.mask})"

    def __add__(self, other):
        self.value = (self.value + other) & self.mask
        return self


class Snowflake:
    timestamp = Bits(41, 0, "timestamp")
    sequence = Bits(13, 41, "sequence")
    instance_id = Bits(5, 54, "instance_id")
    process_id = Bits(5, 59, "process_id")

    def __new__(cls, *args, **kwargs):
        cls.instance_id = cls.instance_id + 1
        return super(Snowflake, cls).__new__(cls)

    def __init__(self):
        self.instance_id = self.instance_id
        pass


snowflake = Snowflake()
snowflake1 = Snowflake()
snowflake2 = Snowflake()
snowflake3 = Snowflake()

# print all inst id
print(snowflake.instance_id)
print(snowflake1.instance_id)
print(snowflake2.instance_id)
print(snowflake3.instance_id)
