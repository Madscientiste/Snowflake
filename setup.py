import pathlib

from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="snowflake",
    version="3.0.0",
    description="Generate snowflakes",
    long_description=README,
    url="https://github.com/Madscientiste/Snowflake",
    author="Madscientiste",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["snowflake"],
)
