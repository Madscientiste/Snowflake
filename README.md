
# Snowflake

Python implementation of Twitter's [Snowflake](https://github.com/twitter-archive/snowflake/tree/scala_28).

#### NOTE  : This is not a 1:1 implementation, it has been altered to fit my needs.



## Explainations

Each time you create a `Snowflake()` instance, you increment its counter by 1
which decrease the chance of collisions if you just call it a bunch in your program

the maximum you can reach is 63 instances at once.

----

you can also use the `process_id` argument when (or if) you are using multiprocessing
this one is manual you need to specifie it `Snowflake(process_id=1)` for each process

the maximum value is also 63.

---

Currently you _should_ be able to generate: 
- **1023 ids** per instance per process on the same **millisecond**. 

so ... (1023 * 1000) = 1 023 000 ~ id/s

however the stress_test.py gives me:
- 1M   ids **in less than a second** on multiprocessing ( i5-9400 6 cores )
- 500K ids **in approx a second** on juste one instance 

they are things that need improvements, but for my use case it does work perfectly.

### Current Structure

currently using 64 bits to store:
-  timestamp   -> 42 bits -> maximum : 4398046511103
-  process_id  -> 6  bits -> maximum : 63
-  instance_id -> 6  bits -> maximum : 63
-  sequences   -> 10 bits -> maximum : 1023


## Usage

### Generating ids

let say the current timestamp is `1631090820684`

```python
from snowflake import Snowflake

# will generate a snowflake -> 1414366371759784960
snowflake = Snowflake()

snowflake.timestamp     # -> 1631090820.684
snowflake.to_date       # -> 08-09-2021 | 10:47:00
snowflake.to_binary     # -> 1001110100000110101101011100010110011000000000000010000000000
snowflake.to_hex        # -> 13a0d6b8b3000400
```

You can also use an existing snowflake

```python
from snowflake import Snowflake

snowflake = Snowflake(1414424474358383616)

snowflake.timestamp     # -> 1631104673.423
snowflake.to_date       # -> 08-09-2021 | 14:37:53
snowflake.to_binary     # -> 1001110100001000010111001000011000011110000000000010000000000
snowflake.to_hex        # -> 13a10b90c3c00400
```

Iterating

```python
from snowflake import Snowflake

for snowflake in Snowflake():
    snowflake  # int -> 1414425848173299712, 1414425848173299713, 1414425848173299714, ...

```

## Optimizations

There is currently no checking if the time went backward ( timezones )
this will surely be a problem if you are generating a lot of ids per day

also, im not a pro python (even tho im currently working)
doesn't mean its perfect, things are maybe done the wrong way..

don't hesitate to do a pull request if you found something wrong !

## Installation

To come.
