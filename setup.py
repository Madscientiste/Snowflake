import pathlib
from .snowflake import __version__
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="snowflake",
    version=__version__,
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
