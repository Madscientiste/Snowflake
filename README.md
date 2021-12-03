# Snowflake

```py
snowflake0 = Snowflake()  # => 123456789, inst n°1
snowflake1 = Snowflake()  # => 123451235, inst n°2
snowflake2 = Snowflake()  # => 124576759, inst n°3
snowflake3 = Snowflake()  # => 123454561, inst n°4
```

since its instances are limited to 5 bits (which gives us a maximum of 31 instances), its better to create one instance for a usecase.



---

a real life example would be:



```py
snowflake0 = Snowflake()  # => 123456789, inst n°1
snowflake1 = Snowflake()  # => 123451235, inst n°2
snowflake2 = Snowflake()  # => 124576759, inst n°3
snowflake3 = Snowflake()  # => 123454561, inst n°4
```
