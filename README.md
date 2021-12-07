# Snowflake

Python implementation of Twitter's [Snowflake](https://github.com/twitter-archive/snowflake/tree/scala_28).

> **NOTE** : This is not a 1:1 implementation, it has been customized to fit my needs.

---

Currently this version does less than my previous version because i wanted it to be reusable, and customisable..

Working on a light version where its not an object but a fonction and implemented in Cython for speed.

for the time being:

-   if you need something for a small project, where you need to generate unique ids that is also sortable but don't care about its perf ( you still get at least 100K+ ids /s ), then you can use this version.

-   if you need something that can scale, but keep the same idea of the snowflake, then ... you need to learn how does it work first, so you can implement it with your language of choice, Or improuve the one made in Python.

If you wish to use this package, you can install it with this command:

```
pip install git+https://github.com/Madscientiste/Snowflake.git@experimental#egg=Snowflake

[or, get the main branch]
pip install git+https://github.com/Madscientiste/Snowflake.git#egg=Snowflake
```

> WIP
