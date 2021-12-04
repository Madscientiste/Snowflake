from .bits import Bits
from .snowflake import Snowflake

from datetime import datetime
import time

from . import __config


def setup_snowflake(epoch: datetime):
    __config.EPOCH = epoch
    __config.INITIAL_EPOCHE = int(time.mktime(__config.EPOCH.timetuple()))

    print("setting config")
    print("EPOCH:", __config.EPOCH)
    print("INITIAL_EPOCHE:", __config.INITIAL_EPOCHE)
    print("")

    from .bits import Bits
    from .snowflake import Snowflake
